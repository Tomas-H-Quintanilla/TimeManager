/*jshint esversion: 8 */
function downloadTasks() {

    const option = document.getElementsByClassName('ui-btn-active')[0].textContent;

    fetch("/download_tasks", {
            method: 'POST',
            body: JSON.stringify({
                date: option

            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRF()
            }
        }).then(response => response.json())
        .then(data => {
            let csv = 'Project name,Task content,Date,Hours,Minutes,Manger\n';

            if (data.data.length > 0) {
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