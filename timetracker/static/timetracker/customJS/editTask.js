/*jshint esversion: 8 */
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