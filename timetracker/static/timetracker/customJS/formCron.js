/*jshint esversion: 8 */

class Cronometer {
    constructor() {
        this.run = false;

    }

    get runState() {
        return this.run;
    }
    set runState(state) {
        this.run = state;
        if (this.run) {}
    }
    static addCron(cron) {
        if (cron.runState) {
            const currentValue = parseInt(document.getElementById("clock").dataset.time) + 1;
            const hours = parseInt(currentValue / 3600);
            const minutes = parseInt((currentValue - hours * 3600) / 60);
            const seconds = parseInt((currentValue - hours * 3600 - minutes * 60));

            let string_time = "";

            if (hours < 10) {
                string_time = "0";
            }
            string_time = string_time + hours.toString() + ":";
            if (minutes < 10) {
                string_time = string_time + "0";
            }
            string_time = string_time + minutes.toString() + ":";
            if (seconds < 10) {
                string_time = string_time + "0";
            }
            string_time = string_time + seconds.toString();
            document.getElementById("clock").dataset.time = currentValue;
            document.getElementById("clock").textContent = string_time;
        }
    }
    reset() {
        if (this.runState) {
            this.runState = false;
        }
        document.getElementById("clock").dataset.time = 0;
        document.getElementById("clock").textContent = "00:00:00";
    }

}
const cron = new Cronometer(false);



async function timer() {
    while (cron.runState) {
        await resolveAfter(0, 1000);
        Cronometer.addCron(cron);
    }
}

function changeCron() {

    let parent = event.target;

    if (!parent.dataset.action) {
        while (parent.tagName != 'BUTTON') {
            parent = parent.parentNode;

        }
    }


    switch (parent.dataset.action) {
        case "play":
            if (!cron.runState) {
                cron.runState = true;
                timer();
            }
            break;
        case "pause":
            cron.runState = false;
            break;
        case "reset":
            cron.reset();
            cron.runState = false;
            break;
        case "change":
            const state = !cron.runState;
            console.log(state);
            if (state) {
                cron.runState = true;
                timer();
            } else {
                cron.runState = false;
            }

            break;

    }
}