/*jshint esversion: 8 */
function getCSRF() {
    name = "csrftoken";
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




function saveTask() {
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
    data.type = 'Regular';
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

function resolveAfter(x, mili) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(x);
        }, mili);
    });
}