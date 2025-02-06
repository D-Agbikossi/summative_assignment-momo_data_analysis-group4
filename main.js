// script.js

// Fetch data from the backend API
async function fetchData() {
  const response = await fetch('/api/transactions'); // Replace with your API endpoint
  const data = await response.json();
  return data;
}

// Render charts
function renderCharts(data) {
  const ctx1 = document.getElementById('transactionVolumeChart').getContext('2d');
  const ctx2 = document.getElementById('paymentDistributionChart').getContext('2d');

  // Group data by transaction type
  const transactionCounts = {};
  data.forEach(transaction => {
    if (!transactionCounts[transaction.type]) {
      transactionCounts[transaction.type] = 0;
    }
    transactionCounts[transaction.type]++;
  });

  // Transaction Volume Chart (Bar Chart)
  new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: Object.keys(transactionCounts),
      datasets: [{
        label: 'Transaction Volume',
        data: Object.values(transactionCounts),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  // Payment Distribution Chart (Pie Chart)
  new Chart(ctx2, {
    type: 'pie',
    data: {
      labels: Object.keys(transactionCounts),
      datasets: [{
        label: 'Payment Distribution',
        data: Object.values(transactionCounts),
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    }
  });
}

// Render transaction details table
function renderTable(data) {
  const tableBody = document.querySelector('#transactionTable tbody');
  tableBody.innerHTML = ''; // Clear existing rows

  data.forEach(transaction => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${transaction.transaction_id}</td>
      <td>${transaction.type}</td>
      <td>${transaction.amount}</td>
      <td>${transaction.date}</td>
      <td>${transaction.sender}</td>
      <td>${transaction.receiver}</td>
    `;
    tableBody.appendChild(row);
  });
}

// Apply filters
async function applyFilters() {
  const search = document.getElementById('search').value;
  const type = document.getElementById('typeFilter').value;
  const date = document.getElementById('dateFilter').value;

  const data = await fetchData();
  const filteredData = data.filter(transaction => {
    return (
      (search === '' || transaction.transaction_id.includes(search)) &&
      (type === '' || transaction.type === type) &&
      (date === '' || transaction.date.startsWith(date))
    );
  });

  renderCharts(filteredData);
  renderTable(filteredData);
}

// Initialize dashboard
async function initDashboard() {
  const data = await fetchData();
  renderCharts(data);
  renderTable(data);
}

// Load dashboard on page load
window.onload = initDashboard;
