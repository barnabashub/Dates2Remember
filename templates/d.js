// Get the user ID from the URL
const userId = window.location.pathname.split('/').pop();

// Fetch data from the backend using the user-specific API endpoint
fetch(`/api/data/${userId}/getsaveddatas`)
    .then(response => {
        // Log the response JSON
        console.log('Response JSON:', response.json());
        return response.json();
    })
    .then(data => {
        // Function to create and populate table rows
        function createTableRow(date, event) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${date}</td>
                <td>${event}</td>
            `;
            return tr;
        }

        // Get the table body element
        const tableBody = document.getElementById('table-body');

        // Iterate through the data and add rows to the table
        data.forEach(item => {
            const row = createTableRow(item.date, item.event);
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching data:', error));
