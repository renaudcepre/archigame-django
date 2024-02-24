document.addEventListener('DOMContentLoaded', function () {

    const elements = document.querySelectorAll('.leaderboard-main');
    loginLink()
    const data = fetchGames()
    console.log(data)
    //
    fetchGames().then(() => {

    })

    fetchLeaderboard(1);

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

function fetchLeaderboard(gameId) {
    fetch(`/api/leaderboard/${gameId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else {
                updateLeaderboardUI('leaderboard-all-time', data.leaderboard_all_time);
                updateLeaderboardUI('leaderboard-year', data.leaderboard_year);
                updateLeaderboardUI('leaderboard-month', data.leaderboard_month);
                updateGameInfoUI(data.game, data.extensions);
            }
        })
        .catch(error => console.error('Erreur lors de la récupération du leaderboard:', error));
}

function fetchGames() {
    return fetch(`/api/gameconfigurations/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des données.');
            }
            return response.json(); // Retourne les données JSON
        })
        .then(data => {
            if (data.error) {
                console.error(data.error);
                throw new Error('Erreur lors de la récupération des données.');
            } else {
                return data; // Retourne les données si elles sont disponibles
            }
        })
        .catch(error => {
            console.error(error);
            throw error; // Propage l'erreur pour la gérer à l'extérieur de la fonction
        });
}


function updateLeaderboardUI(containerId, leaderboard) {
    const leaderboardContainer = document.getElementById(containerId);
    leaderboardContainer.innerHTML = ''; // Vide le conteneur avant de le remplir

    leaderboard.forEach((entry, index) => {
        const div = document.createElement('div');
        div.className = 'lb-entry';
        div.innerHTML = `<div>${index + 1}. ${entry.player__username}</div><div>${entry.total_score}</div>`;
        leaderboardContainer.appendChild(div);
    });
}


function updateGameInfoUI(game, extensions) {
    const gameNameContainer = document.getElementById("game");
    gameNameContainer.textContent = game;

    const extensionsContainer = document.getElementById("extensions");
    extensionsContainer.innerHTML = ""; // Clear previous content

    const extensionsList = JSON.parse(extensions);
    extensionsList.forEach(extension => {
        const extensionDiv = document.createElement('div');
        extensionDiv.classList.add('lb-title')
        extensionDiv.classList.add('is-size-3')
        extensionDiv.textContent = extension.fields.name;
        extensionsContainer.appendChild(extensionDiv);
    });
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
        timer = setTimeout(hideLoginLink, 5000);  // 10 secondes
    }

    document.addEventListener('mousemove', resetTimer);
    document.addEventListener('keydown', resetTimer);

    startTimer();
}