document.addEventListener('DOMContentLoaded', function () {

    loginLink()

})
;

function generateRandomColor(maxVal = 100) {
    const randomNumber = Math.random() * maxVal;
    const red = Math.floor(Math.random() * maxVal);
    const green = Math.floor(Math.random() * maxVal);
    const blue = Math.floor(Math.random() * maxVal);
    return `rgb(${red}, ${green}, ${blue})`;

}

function loginLink() {
    let loginLink = document.querySelector('.login-link');

    function showLoginLink() {
        document.querySelector('.login-link').classList.add('show');
    }

    function hideLoginLink() {
        document.querySelector('.login-link').classList.remove('show');
    }

    document.addEventListener('mousemove', resetTimer);

    function resetTimer() {
        showLoginLink();
        clearTimeout(timer);
        startTimer();
    }

    let timer;

    function startTimer() {
        timer = setTimeout(hideLoginLink, 2000);  // 10 secondes
    }

    document.addEventListener('mousemove', resetTimer);
    document.addEventListener('keydown', resetTimer);

    startTimer();
}