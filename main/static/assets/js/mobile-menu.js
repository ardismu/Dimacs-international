const nav-button = document.querySelector('.nav-icon');
const nav-menu = document.querySelector('.nav');
nav-button.addEventListener('click', () => {
    nav-menu.classList.add('nav-toggle');
})