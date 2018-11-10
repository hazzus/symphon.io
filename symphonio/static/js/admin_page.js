$("#photoField").change(function () {
    form.submit();
});

const form = $("#form");

function frameLoad() {
    const iFrameID = document.getElementById('adminFrame');
    if (iFrameID) {
        iFrameID.height = "";
        iFrameID.height = iFrameID.contentWindow.document.body.scrollHeight + "px";
    }
}