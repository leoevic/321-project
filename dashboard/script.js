console.log(mqtt);

const distanceSensorValue = document.querySelector('#distance-sensor-value');

const broker = `ws://${window.location.host}:9001`
const mqttClient = mqtt.connect(broker, {});

const gameNotRunningLabel = document.querySelector('#game_not_running');
const gameRunningLabel = document.querySelector('#game_running');
const youDiedLabel = document.querySelector('#you_died');
const scoreInformation = document.querySelector('#score_information');
const scoreValue = document.querySelector('#score_value');

mqttClient.on('connect', () => {
    console.log('connected');
    mqttClient.subscribe('leonardoevic/#', err => {
        if (err) console.error(err);
    });
});

mqttClient.on('message', (topic, message) => {
    console.log(`got message from topic ${topic}: ${message}`);
    switch (topic) {
        case 'leonardoevic/game/running':
            handleGameState(message);
            break;

        case 'leonardoevic/game/score':
            handleGameScore(message);
            break;
    }
});


/**
 * Handle whether the game is running or not
 * @param {number} state 
 */
function handleGameState(state) {
    if (state == 1) {
        gameNotRunningLabel.classList.add('hidden');
        youDiedLabel.classList.add('hidden');
        gameRunningLabel.classList.remove('hidden');
        scoreInformation.classList.remove('hidden');
    }
    else {
        youDiedLabel.classList.remove('hidden');
        gameNotRunningLabel.classList.add('hidden');
        gameRunningLabel.classList.add('hidden');
        scoreInformation.classList.add('hidden');
    }
}



/**
 * Handle the game score display
 * @param {*} score 
 */
function handleGameScore(score) {
    scoreValue.textContent = score;
}