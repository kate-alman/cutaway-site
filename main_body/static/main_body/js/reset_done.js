function reset_done(event) {
    const form  = document.getElementById("form");
    if (form.checkValidity()) {
        alert("We've emailed you instructions for setting your password. If you don't receive an email, please make sure you've entered the address you registered with.");
        }
   console.log(event);
   window.location.href = '/accounts/login';
}
