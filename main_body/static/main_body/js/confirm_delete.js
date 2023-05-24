function confirm_delete(event) {
    console.log(event);
    if (!confirm('Are you sure? This action can\'t be undone')) {
        event.preventDefault();
        console.log(event);
        return false;
   }
}