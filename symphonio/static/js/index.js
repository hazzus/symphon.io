
const form = $("#form");
$("#photoField").change(function () {
    form.submit();
});


takeShot.click(function () {
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

const cam = $("#cameraThings");


$('#camera').tooltip('show');
$("#camera").click(function () {
    $('#camera').tooltip('hide');
    $("#showCameraButton").hide();
    $("#cameraSelect").show();
    cam.slideDown();
    $("#takeShot").slideDown();
    getStream();
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