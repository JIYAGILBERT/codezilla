document.addEventListener('DOMContentLoaded', function() {
    let startTime = Date.now() / 1000;
    let startTimeInput = document.getElementById('start-time');
    startTimeInput.value = startTime;
    console.log('start_time set to:', startTimeInput.value);

    let timerDisplay = document.getElementById('time');
    function updateTimer() {
        let elapsed = Math.floor(Date.now() / 1000 - startTime);
        let minutes = Math.floor(elapsed / 60);
        let seconds = elapsed % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    setInterval(updateTimer, 1000);
});