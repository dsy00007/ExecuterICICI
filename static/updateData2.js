// document.addEventListener('DOMContentLoaded', function () {
//     setInterval(function () {
//         fetchDataAndUpdate();
//     }, 3000);

    function fetchDataAndUpdate() {
        fetch('/refreshData')
            .then(response => response.json())
            .then(data => {
                // Update the DOM with the latest data
                document.getElementById('user-name').innerText = 'User Name: ' + data.userName;
                document.getElementById('order-details').innerText = 'Order Details: ' + data.currentOrder;
                document.getElementById('profit-n-loss').innerText = 'Profit and Loss: Rs. ' + data.totalProfit.toFixed(2);
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    function setSessionKey() {
        // Get the value from the text box
        var inputValue = document.getElementById('textInput').value;
    
        // Make an AJAX request to the server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/setSessionKey/', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    
        // Send the data to the server
        xhr.send(JSON.stringify({ input_value: inputValue }));
    
        // Handle the response from the server (you can customize this part)
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert('Response from server: ' + xhr.responseText);
            }
        };
    }
// });