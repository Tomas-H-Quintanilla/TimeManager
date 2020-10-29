/*jshint esversion: 8 */



let filesToBeSent = [];



let previousElement = null;

function changePosition() {

    if (event.target.dataset.buttonid && event.target.parentNode != previousElement) {

        if (previousElement) {
            const currentElement = event.target;

            const parent1 = previousElement.parentNode;

            event.target.parentNode.parentNode.replaceChild(previousElement, currentElement.parentNode);
            parent1.appendChild(currentElement.parentNode);

            previousElement.style.backgroundColor = "";
            previousElement = null;

        } else {
            previousElement = event.target.parentNode;
            previousElement.style.backgroundColor = "rgba(39, 209, 39, 1)";

        }

    } else {
        if (previousElement) {
            previousElement.style.backgroundColor = "";
        }

        previousElement = null;
    }


}

function intBytes( /*long*/ long) {
    // we want to represent the input as a 8-bytes array

    arrayUnits = ['B', 'KB', 'MB', 'GB', 'TB'];
    count = 0;
    let divider = 1000;
    console.log(long);
    while (long > divider != 0) {
        divider = divider * 1000;
        count++;
    }

    const result = parseFloat((long * 1000) / divider).toFixed(2) + " " + arrayUnits[count];

    return result;
}

function dropHandler(ev) {
    console.log('File(s) dropped');

    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();


    if (ev.dataTransfer.items) {
        let reader = new FileReader();

        reader.onload = function(event) {

            if (filesToBeSent.indexOf([event.target.result]) > -1) {
                alert("File already uploaded");
            } else {
                filesToBeSent.push(event.target.result);
            }


        };
        // Use DataTransferItemList interface to access the file(s)
        let check = false;
        for (let i = 0; i < ev.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (ev.dataTransfer.items[i].kind === 'file') {
                let file = ev.dataTransfer.items[i].getAsFile();
                console.log(file);
                if (file.type == "text/csv") {
                    reader.readAsBinaryString(ev.dataTransfer.files[i]);
                    addFile(file);
                    check = true;
                }


            }
        }
        if (!check) {
            console.log("Invalid files");
        }
    }
}

function addFile(fileAdd) {
    const li_element = document.createElement("li");
    const text = document.createElement("a");
    const button = document.createElement("a");
    const size = document.createElement("p");
    text.disabled = true;
    text.textContent = fileAdd.name;
    size.textContent = "Size: " + intBytes(fileAdd.size);
    text.append(size)
    button.classList.add("ui-icon-delete");
    button.setAttribute("data-position", filesToBeSent.length);
    // button.setAttribute("data-icon", "delete");

    li_element.append(text);
    li_element.append(button);

    button.addEventListener("click", deleteFile);

    $("#inputFilesList").append(li_element);
    $("#inputFilesList").listview("refresh");
}

function deleteFile(event) {

    filesToBeSent[parseInt(event.target.dataset.position)] = null;
    document.querySelector("#inputFilesList").removeChild(event.target.parentNode);
    $("#inputFilesList").listview("refresh");
}


function sendFilesData() {

    const c = document.getElementById("inputsOrder").children;
    let orderHeads = [];
    for (let i = 0; i < c.length; i++) {
        orderHeads.push(c[i].children[0].children[0].dataset.buttonid);
    }

    data = {};
    data['type'] = "csv";
    data.order = orderHeads;
    data.content = filesToBeSent;

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


            }


        })
        .catch(error => {
            console.log('Error:', error);

        });

}



function dragOverHandler(ev) {
    console.log('File(s) in drop zone');

    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
}

document.addEventListener('DOMContentLoaded', function() {
    // document.getElementById('input-file-now').parentElement.style.opacity = 0;
    document.getElementsByTagName('body')[0].addEventListener('click', changePosition);
}, false);