document.addEventListener('DOMContentLoaded', function () {

    setTimeout(function () {


        window.location.reload(true);
    }, 7000);

    const elements = document.querySelectorAll('.leaderboard-main');

    elements.forEach(element => {
        const color1 = generateRandomColor(150);
        const color2 = generateRandomColor(50);
        const gradient = `linear-gradient(135deg, ${color1}, ${color2})`;

        element.style.background = gradient;
    });
});

function generateRandomColor(maxVal = 100) {
    const randomNumber = Math.random() * maxVal;
    const red = Math.floor(Math.random() * maxVal);
    const green = Math.floor(Math.random() * maxVal);
    const blue = Math.floor(Math.random() * maxVal);
    return `rgb(${red}, ${green}, ${blue})`;

}

document.addEventListener('DOMContentLoaded', function () {


});
