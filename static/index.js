function getChain() {
    fetch('/get_chain')
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerHTML = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function mineBlock(difficulty) {
    fetch(`/mining/${difficulty}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerHTML = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function checkValidity() {
    fetch('/is_valid')
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerHTML = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}