function reset_done(event) {
   alert("We've emailed you instructions for setting your password. If you don't receive an email, please make sure you've entered the address you registered with.");
   console.log(event);
   event.preventDefault();
   window.location.href = '/accounts/login';
}