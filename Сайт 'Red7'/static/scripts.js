const header_short = document.querySelector(".header_short");  // укороченная шапка
const header_full = document.querySelector(".header_full");  // полная шапка
const header_logos = document.querySelectorAll(".header_logo");

header_logos.forEach(logo => {
    logo.addEventListener('click', () => {
        header_full.classList.toggle('hidden');
        header_short.classList.toggle('hidden');
    });
});
// header_logo.addEventListener('click', () => {
    
// })

// header_logo.addEventListener('click', () => {
//     header_full.classList.toggle('hidden');
//     header_short.classList.toggle('hidden');
// })


