document.addEventListener('DOMContentLoaded', () => {
    const musicCard = document.querySelector('.music-card');

    musicCard.addEventListener('click', () => {
        musicCard.classList.toggle('expanded');
    });
});