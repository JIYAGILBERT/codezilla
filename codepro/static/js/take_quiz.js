// static/js/take_quiz.js
function startTimer(duration, display) {
    let timer = duration, minutes, seconds;
    const interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        display.textContent = minutes + ":" + seconds;
        if (--timer < 0) {
            clearInterval(interval);
            const form = document.getElementById('quiz-form');
            if (form) {
                console.log("Timer expired, submitting form"); // Debug
                form.submit(); // Ensure form submission
            } else {
                console.error("Quiz form not found");
            }
        }
    }, 1000);
}

function initializeTimer(difficulty) {
    console.log("Difficulty: " + difficulty);
    let duration;
    if (difficulty === "medium") {
        duration = 180; // 3 minutes
    } else if (difficulty === "hard") {
        duration = 120; // 2 minutes
    } else {
        console.error("Invalid difficulty: " + difficulty);
        return;
    }
    const display = document.querySelector('#time');
    if (!display) {
        console.error("Timer display element (#time) not found");
        return;
    }
    startTimer(duration, display);
}