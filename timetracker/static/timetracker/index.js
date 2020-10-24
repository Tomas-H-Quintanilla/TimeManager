/*jshint esversion: 8 */
function getCSRF() {
    name = "csrftoken"
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function getCSRF() {

//     return document.querySelector('[name=csrfmiddlewaretoken]').value;
// }


function save_project() {
    const members = document.getElementById("project_members").children;
    let data = {};
    let project_members = [];
    let i;
    for (i = 0; i < members.length; i++) {
        if (members[i].dataset.role != "list-divider") {
            if (members[i].dataset.manager) {
                data.manager = members[i].textContent;
            } else {
                project_members.push(members[i].textContent);
            }
        }
    }
    data.members = project_members;
    data.name = document.querySelector("#project_name").value;
    if (document.querySelector("#project_name").value.trim() === "") {

        alert("One of the required fields is empty.");
    } else {
        fetch("projectSave", {
                method: 'POST',
                body: JSON.stringify({
                    body: data

                }), // data can be `string` or {object}!
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRF()
                }
            })
            .then(response => response.json())
            .then(data => {

                if (data.status === 200) {

                    window.location.reload();
                }


            })
            .catch(error => {
                console.log('Error:', error);

            });
    }



}

function delete_member() {

    const id_name = event.target.dataset.member;
    document.getElementById(id_name).disabled = false;
    event.target.parentNode.parentNode.removeChild(event.target.parentNode);
}

function choosen() {
    event.target.disabled = true;
    // class = "ui-btn ui-shadow ui-corner-all ui-btn-icon-right ui-icon-delete"
    const li_element = document.createElement("li");
    const text = document.createElement("a");
    const button = document.createElement("a");
    text.disabled = true;
    text.textContent = event.target.value;
    button.classList.add("ui-icon-delete");
    button.setAttribute("data-member", event.target.id);
    // button.setAttribute("data-icon", "delete");

    li_element.append(text);
    li_element.append(button);

    button.addEventListener("click", delete_member);

    $("#project_members").append(li_element);
    $("#project_members").listview("refresh");
}


function getTasks() {
    const option = event.target.textContent;
    fetch("/task_list", {
            method: 'POST',
            body: JSON.stringify({
                body: option

            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRF()
            }
        }).then(response => response.json())
        .then(data => {

            document.getElementById("listview_tasks").innerHTML = "";
            data.data.forEach(element => {

                const project_name = document.createElement("h1");
                const contentWrap = document.createElement("p");
                const content = document.createElement("strong");
                const list_element = document.createElement("li");

                const wrapper = document.createElement("a");
                wrapper.href = "/edit_task/" + element.id;

                const list_split = document.createElement("div");
                list_split.classList.add("ui-grid-a");

                const list_split1 = document.createElement("div");
                const list_split2 = document.createElement("div");
                list_split1.classList.add("ui-block-a");
                list_split2.classList.add("ui-block-b");

                const date_h1 = document.createElement("p");
                const time_h1 = document.createElement("p");

                date_h1.textContent = element.date;
                time_h1.textContent = element.time_used;
                project_name.textContent = element.project_name;
                content.textContent = element.task_content;

                list_split1.append(date_h1);
                list_split2.append(time_h1);

                list_split.append(list_split1);
                list_split.append(list_split2);

                contentWrap.append(content);

                wrapper.append(project_name);

                wrapper.append(contentWrap);
                wrapper.append(list_split);

                list_element.appendChild(wrapper);

                $("#listview_tasks").append(list_element);
                $("#listview_tasks").listview("refresh");
                console.log($("#listview_tasks"));

            });
        }).catch(error => {
            console.log('Error:', error);

        });
}

function changeCron() {

    switch (event.target.dataset.action) {
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
            break;
        case "change":
            const state = !cron.runState;
            if (!cron.runState && state) {
                cron.runState = true;
                timer();
            } else {
                cron.runState = false;
            }

            break;

    }
}

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

function resolveAfter(x, mili) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(x);
        }, mili);
    });
}

async function timer() {
    while (cron.runState) {
        await resolveAfter(0, 1000);
        Cronometer.addCron(cron);
    }
}


function saveTask() {
    console.log("HOLA");
    let data = {};
    data["task_content"] = document.getElementsByName("task_content")[0].value.trim();

    data.project_name = document.getElementsByName("project_name")[0].value.trim();
    if (event.target.dataset.operation == "manual") {
        data.date = document.getElementsByName("date")[0].value.trim();
        data.minutes = parseInt(document.getElementsByName("hours")[0].value.trim()) * 60 + parseInt(document.getElementsByName("minutes")[0].value.trim());
    } else if (event.target.dataset.operation == "cron") {
        const today = new Date();
        data.date = today.getFullYear() + "-" + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
        data.minutes = parseInt(parseInt(document.getElementById("clock").dataset.time) / 60);
        console.log(data);
    }

    if (data.task_content == "" || data.project_name == "" || data.date == "" || data.minutes == "" || data.minutes == 0) {
        alert("One of the required fields is empty.");
    } else {
        fetch("/insert_task", {
                method: 'POST',
                body: JSON.stringify({
                    body: data

                }), // data can be `string` or {object}!
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRF()
                }
            })
            .then(data => {
                if (data.status === 200) {
                    window.location.reload();

                }


            })
            .catch(error => {
                console.log('Error:', error);

            });
    }
}


function editTask() {

    let data = {};
    data["task_content"] = document.getElementsByName("task_content")[document.getElementsByName("task_content").length - 1].value.trim();

    data.option = event.target.dataset.option;
    data.taskid = event.target.dataset.taskid;
    data.project_name = document.getElementsByName("project_name")[document.getElementsByName("project_name").length - 1].value.trim();

    data.date = document.getElementsByName("date")[0].value.trim();
    data.minutes = parseInt(document.getElementsByName("hours")[0].value.trim()) * 60 + parseInt(document.getElementsByName("minutes")[0].value.trim());


    if ((data.task_content == "" || data.project_name == "" || data.date == "" || data.minutes == "" || data.minutes == 0) && data.option != "delete") {
        console.log(data);
        alert("One of the required fields is empty.");
    } else {
        fetch("/manage_task", {
                method: 'POST',
                body: JSON.stringify({
                    body: data

                }), // data can be `string` or {object}!
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRF()
                }
            })
            .then(data => {
                if (data.status === 200) {
                    window.open("/", "_top");

                }


            })
            .catch(error => {
                console.log('Error:', error);

            });
    }
}

function editProject() {
    const members = document.getElementById("project_members").children;
    let data = {};
    let project_members = [];
    let i;
    for (i = 0; i < members.length; i++) {
        if (members[i].dataset.role != "list-divider") {
            if (members[i].dataset.manager) {
                data.manager = members[i].textContent.trim();
            } else {
                project_members.push(members[i].textContent);
            }
        }
    }
    data.members = project_members;
    data.name = document.querySelector("#project_name").value;
    data.projectid = event.target.dataset.projectid;
    data.option = event.target.dataset.option;


    if (document.querySelector("#project_name").value.trim() === "" && event.target.dataset.option != "delete") {

        alert("One of the required fields is empty.");
    } else {
        fetch("/manage_project", {
                method: 'POST',
                body: JSON.stringify({
                    body: data

                }), // data can be `string` or {object}!
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRF()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 200) {

                    window.location.reload();
                }


            })
            .catch(error => {
                console.log('Error:', error);

            });
    }

}