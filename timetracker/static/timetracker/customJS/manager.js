/*jshint esversion: 8 */



function choosen() {



    if (event.target.dataset.choosen == 'True') {
        event.target.style.backgroundColor = 'white';
        event.target.style.color = 'black';
        event.target.dataset.choosen = 'False';
    } else {
        event.target.dataset.choosen = 'True';
        event.target.style.backgroundColor = '#007bff';
        event.target.style.color = 'white';
    }



    $(event.target.parentNode).listview("refresh");


}

function downloadTasks() {

    const date1 = document.getElementsByName('date1')[0].value;
    const date2 = document.getElementsByName('date2')[0].value;
    const option = document.getElementsByClassName('ui-btn-active')[0].textContent;

    let option_date = true;
    if (date2 && date1) {
        if (date2.value < date1.value) {
            document.getElementById('dateMessage').textContent = "* Invalid date values.";
            document.getElementById('dateMessage').style.display = 'block';
            option_date = false;
        }
    }

    const workers_list = document.getElementById('workers').children;
    const projects_list = document.getElementById('projects').children;

    let counter = 0;
    let workers_send = [];
    let projects_send = [];

    while (counter < workers_list.length) {
        if (workers_list[counter].dataset.choosen === 'True') {
            workers_send.push(workers_list[counter].textContent.trim());
        }
        counter++;
    }
    counter = 0;
    while (counter < projects_list.length) {
        if (projects_list[counter].dataset.choosen === 'True') {
            projects_send.push(projects_list[counter].textContent.trim());
        }
        counter++;
    }
    if (workers_send.length == 0 && projects_send.length == 0) {
        option_date = false;
        document.getElementById('dateMessage').textContent = "* Choose at least a project or a worker.";
        document.getElementById('dateMessage').style.display = 'block';
    }

    if (option_date) {
        document.getElementById('dateMessage').style.display = 'none';
        fetch("/download_tasks", {
                method: 'POST',
                body: JSON.stringify({
                    date: option,
                    date1: date1,
                    date2: date2,
                    workers: workers_send,
                    projects: projects_send

                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRF()
                }
            }).then(response => response.json())
            .then(data => {

                if (data.workers.length == 0 && data.projects.length == 0) {
                    document.getElementById('dateMessage').textContent = "* There were not tasks with the choosen options";
                    document.getElementById('dateMessage').style.display = 'block';
                } else {
                    if (data.workers.length != 0) {
                        let csv = '';
                        data.workers.forEach(element => {

                            csv = csv + element;
                        });
                        const hiddenElement = document.createElement('a');
                        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
                        hiddenElement.target = '_blank';
                        hiddenElement.download = data.title_workers;
                        hiddenElement.click();
                    }
                    if (data.projects.length != 0) {
                        let csv = '';
                        data.projects.forEach(element => {

                            csv = csv + element;
                        });
                        const hiddenElement = document.createElement('a');
                        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
                        hiddenElement.target = '_blank';
                        hiddenElement.download = data.title_projects;
                        hiddenElement.click();
                    }


                }

            });
    }


}