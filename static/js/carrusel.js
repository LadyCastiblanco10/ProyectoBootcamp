/* ---- HERO SLIDER ---- */
let heroIndex = 0;
const heroSlides = document.querySelector('.hero-slides');
const heroTotal = document.querySelectorAll('.hero-slide').length;

document.querySelector('.next').onclick = () => {
    heroIndex = (heroIndex + 1) % heroTotal;
    heroSlides.style.transform = `translateX(-${heroIndex * 100}%)`;
};

document.querySelector('.prev').onclick = () => {
    heroIndex = (heroIndex - 1 + heroTotal) % heroTotal;
    heroSlides.style.transform = `translateX(-${heroIndex * 100}%)`;
};

/* ---- HIPOTESIS CAROUSEL ---- */
let hipoIndex = 0;
const hipoTrack = document.querySelector('.hipo-track');
const hipoCards = document.querySelectorAll('.hipo-card').length;
const cardWidth = 260;

document.querySelector('.hipo-next').onclick = () => {
    if (hipoIndex < hipoCards - 1) hipoIndex++;
    hipoTrack.style.transform = `translateX(-${hipoIndex * cardWidth}px)`;
};

document.querySelector('.hipo-prev').onclick = () => {
    if (hipoIndex > 0) hipoIndex--;
    hipoTrack.style.transform = `translateX(-${hipoIndex * cardWidth}px)`;
};
