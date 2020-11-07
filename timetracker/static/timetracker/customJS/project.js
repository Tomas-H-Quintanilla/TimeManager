/*jshint esversion: 8 */
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

function saveProject() {
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



function downloadTasks() {

    const option = document.getElementsByClassName('ui-btn-active')[0].textContent;
    const projectid = event.target.dataset.projectid;
    fetch("/download_tasks", {
            method: 'POST',
            body: JSON.stringify({
                date: option,
                projectid: projectid

            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRF()
            }
        }).then(response => response.json())
        .then(data => {
            if (data.data.length > 0) {
                let csv = 'Project name,Task content,Date,Hours,Minutes,Manger\n';
                data.data.forEach(element => {

                    csv = csv + element;
                });
                const hiddenElement = document.createElement('a');
                hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
                hiddenElement.target = '_blank';
                hiddenElement.download = data.title;
                hiddenElement.click();
            } else {
                alert('There are no tasks by the parameters choosen.');
            }
        });
}