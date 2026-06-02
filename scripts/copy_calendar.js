const copyButton = document.getElementById("copy-calendar-url");
const copyFeedback = document.getElementById("copy-feedback");

function calendarUrl() {
    return new URL("stadtbibliothek.ics", window.location.href).href;
}

async function copyCalendarUrl() {
    try {
        await navigator.clipboard.writeText(calendarUrl());
        copyFeedback.textContent = "Kalender-URL kopiert.";
    } catch {
        copyFeedback.textContent = "Kopieren nicht möglich. Verwende diesen Link: " + calendarUrl();
    }
}

copyButton.addEventListener("click", copyCalendarUrl);
