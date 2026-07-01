// static/js/script.js
// Small UX enhancement: auto-dismiss flash alerts after a few seconds.

document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Use Bootstrap's Alert API to fade it out gracefully
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 3000);
    });
});
