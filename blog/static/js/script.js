document.addEventListener('DOMContentLoaded', function() {
    var messages = document.querySelector('.messages');
    if (messages) {
        setTimeout(function() {
            messages.style.display = 'none';
        }, 3000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const paginatorLinks = document.querySelectorAll('.paginator .page-link');
    paginatorLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const url = this.href;
            window.scrollTo({ top: 0, behavior: 'smooth' });
            setTimeout(() => {
                window.location.href = url;
            }, 500);
        });
    });
});