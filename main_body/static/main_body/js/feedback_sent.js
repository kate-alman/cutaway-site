function feedback_sent(event) {
    const form  = document.getElementById("form");
    if (form.checkValidity()) {
        alert("Your feedback has been sent");
        }
    console.log(event);
}