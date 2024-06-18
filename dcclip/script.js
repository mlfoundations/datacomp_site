document.getElementById('csvFile').addEventListener('change', handleFileSelect);

function handleFileSelect(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
        const csvData = event.target.result;
        processData(csvData);
    };

    reader.readAsText(file);
}

function processData(csvData) {
    const rows = csvData.split('\n');
    const data = rows.map(row => row.split(','));

    // Sort the data array based on a particular value (column)
    const columnIndexToSortBy = 1; // Change this to the desired column index
    data.sort((a, b) => a[columnIndexToSortBy].localeCompare(b[columnIndexToSortBy]));

    populateTable(data);
}

function populateTable(data) {
    const tableBody = document.querySelector('#dataTable tbody');
    
    data.forEach(rowData => {
        const row = document.createElement('tr');

        rowData.forEach(cellData => {
            const cell = document.createElement('td');
            cell.textContent = cellData;
            row.appendChild(cell);
        });

        tableBody.appendChild(row);
    });
}