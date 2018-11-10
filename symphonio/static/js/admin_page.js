$("#photoField").change(function () {
    form.submit();
});

const form = $("#form");

function frameLoad() {
    const frame = document.getElementById('adminFrame');
    if (frame.contentWindow.location.href.split('/')[3] !== "admin") {
        frame.contentWindow.location.replace(frame.src);
    }
    if (frame) {
        frame.height = "";
        frame.height = frame.contentWindow.document.body.scrollHeight + "px";
    }
}

function loader() {
    $("#loader").show();
}