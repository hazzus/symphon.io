
const form = $("#form");
$("#photoField").change(function () {
    form.submit();
});



cameraButton = $('#takeShot');
cameraButton.click(function () {
    let canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d')
        .drawImage(video, 0, 0, canvas.width, canvas.height);
    let data = canvas.toDataURL("image/jpeg", 0.25);
    console.log(data);
    document.getElementById("id_data").value = data;
    form.submit();
});

const cameraStuff = $('#cameraThings');
const cameraHolder = $('#cameraHolder');
const camera = $('#camera');
const cameraSelect = $('#cameraSelect');
is_clicked = 0;
$("#camera_holder").click(function () {
    if (is_clicked === 0) {
        cameraHolder.fadeOut();
        cameraSelect.show();
        takeShot.show();
        cameraSelect.show();
        $('#info').slideUp();
        cameraStuff.fadeIn();
        camera.slideDown(duration = 900);
        cameraButton.show();
        getStream();
        is_clicked++;
    } else {
        cameraButton.click()
    }
});

const video = document.querySelector("#camera");
const videoSelect = document.querySelector('select#cameraSelect');

navigator.mediaDevices.enumerateDevices()
    .then(gotDevices);

videoSelect.onchange = getStream;

function gotDevices(deviceInfos) {
    for (let i = 0; i !== deviceInfos.length; ++i) {
        const deviceInfo = deviceInfos[i];
        const option = document.createElement('option');
        option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === 'videoinput') {
            option.text = deviceInfo.label || 'camera ' +
                (videoSelect.length + 1);
            videoSelect.appendChild(option);
        } else {
            console.log('Found another kind of device: ', deviceInfo);
        }
    }
}

function getStream() {
    if (window.stream) {
        window.stream.getTracks().forEach(function (track) {
            track.stop();
        });
    }

    const constraints = {
        video: {
            deviceId: {exact: videoSelect.value}
        }
    };

    navigator.mediaDevices.getUserMedia(constraints).then(gotStream).catch(handleError);
}

function gotStream(stream) {
    window.stream = stream; // make stream available to console
    video.srcObject = stream;
}

function handleError(error) {
    console.error('Error: ', error);
}

