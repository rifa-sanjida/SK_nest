document.addEventListener('DOMContentLoaded', function () {
    console.log('Skill Nest charcoal theme loaded successfully.');

    const navbar = document.querySelector('.skillnest-navbar');

    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 20) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
});