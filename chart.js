// script.js

document.addEventListener("DOMContentLoaded", function () {
    // Fetch data from the backend
    fetch('/api/transactions') // Update with your actual API endpoint
        .then(response => response.json())
        .then(data => {
            // Data fetched from API (should be in JSON format)
            const smsData = data.sms_date; // Assuming this is an array
            const amounts = data.amounts; // Assuming this is an array
            const categories = data.categories; // Assuming this is an array

            // Generate the Scatter Plot
            const scatterCtx = document.getElementById('scatterChart').getContext('2d');
            new Chart(scatterCtx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Transactions Over Time',
                        data: smsData.map((date, index) => ({
                            x: new Date(date), // Convert string to date
                            y: amounts[index]
                        })),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'month',
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Transaction Amount (RWF)'
                            }
                        }
                    }
                }
            });

            // Generate the Bar Chart
            const barCtx = document.getElementById('barChart').getContext('2d');
            new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels: categories,
                    datasets: [{
                        label: 'Total Transaction Amount (RWF)',
                        data: amounts,
                        backgroundColor: [
                            'green', 'red', 'blue', 'orange', 'purple', 'brown', 
                            'pink', 'black', 'yellow', 'cyan'
                        ],
                        borderColor: 'black',
                        borderWidth: 1,
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Amount (RWF)'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
