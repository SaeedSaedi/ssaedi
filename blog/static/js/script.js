document.addEventListener('DOMContentLoaded', function() {
    var messages = document.querySelector('.messages');
    if (messages) {
        setTimeout(function() {
            messages.style.display = 'none';
        }, 3000);
    }
});