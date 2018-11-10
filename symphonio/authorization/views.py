import datetime

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Profile
from .models import MALE, FEMALE, NON_DISCLOSED

from .vk_api import get_authorization_url, get_auth_info, get_bdate_and_sex


def request_token(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        return render(request, 'index.html')  # TODO: already exists
    url = get_authorization_url()
    return redirect(url)


def receive_token(request: HttpRequest):
    assert not request.user.is_authenticated
    assert request.method == 'GET'
    code = request.GET.get('code')
    if code is None:
        raise NotImplementedError("implement error when code is not present")
    data = get_auth_info(code)
    token = data.get('access_token')
    expires_in = data.get('expires_in')
    vk_id = data.get('user_id')
    email = data.get('email')
    assert token is not None
    assert expires_in is not None
    assert vk_id is not None
    if email is None:
        return render(request, 'index.html') # TODO: message
    bdate, sex = get_bdate_and_sex(token, vk_id)
    if bdate is None:
        return render(request, 'index.html') # TODO: message
    if sex is None:
        sex = 0
    result_set = User.objects.filter(profile__vk_id=vk_id)
    if result_set:
        return render(request, 'index.html') # TODO: message
    age = make_age(bdate)
    gender = make_gender(sex)
    user = User()
    user.username = vk_id
    user.email = email
    user.save()
    user.profile.vk_id = vk_id
    user.profile.age = age
    user.profile.gender = gender
    user.profile.save()
    user.save()
    request.user = user
    return render(request, 'index.html')


def make_age(bdate: str) -> int:  # format of bdate is D.M.YYYY
    day, month, year = map(int, bdate.split('.'))
    date = datetime.date(year, month, day)
    today = datetime.date.today()
    delta = datetime.timedelta() + today - date
    return int(delta.days // 365.2425)


def make_gender(sex: int) -> str:
    if sex == 0:
        return NON_DISCLOSED
    elif sex == 1:
        return FEMALE
    elif sex == 2:
        return MALE
    else:
        assert False, 'unknown sex: ' % sex