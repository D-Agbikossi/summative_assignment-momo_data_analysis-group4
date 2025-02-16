function filterTransactions() {
    let input = document.getElementById("searchInput").value.toUpperCase();
    let table = document.querySelector(".table-content table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) { 
        let tds = tr[i].getElementsByTagName("td");
        let found = false;

        for (let j = 0; j < tds.length; j++) { 
            if (tds[j]) {
                let txtValue = tds[j].textContent || tds[j].innerText;
                if (txtValue.toUpperCase().indexOf(input) > -1) {
                    found = true;
                    break; 
                }
            }
        }

        tr[i].style.display = found ? "" : "none"; 
    }
}


async function fetchTransactionSummary() {
    try {
        const response = await fetch('http://localhost:3000/api/transaction-summary');
        const data = await response.json();
        
        // Update card numbers
        document.querySelector('.data-card:nth-child(1) .number').textContent = data.incomings;
        document.querySelector('.data-card:nth-child(2) .number').textContent = data.outgoings;
        document.querySelector('.data-card:nth-child(3) .number').textContent = data.withdrawals;
        document.querySelector('.data-card:nth-child(4) .number').textContent = data.bills;
    } catch (error) {
        console.error('Error fetching transaction summary:', error);
    }
}


async function fetchRecentTransactions() {
    try {
        const response = await fetch('http://localhost:3000/api/recent-transactions');
        const transactions = await response.json();
        
        const tableBody = document.createElement('tbody');
        transactions.forEach(transaction => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${transaction.transaction_id}</td>
                <td>${transaction.category}</td>
                <td>${transaction.body}</td>
                <td>${transaction.date}</td>
                <td>${transaction.time}</td>
                <td>${transaction.amount}</td>
            `;
            tableBody.appendChild(row);
        });

        const table = document.querySelector('.table-content table');
        const existingBody = table.querySelector('tbody');
        if (existingBody) {
            existingBody.remove();
        }
        table.appendChild(tableBody);
    } catch (error) {
        console.error('Error fetching recent transactions:', error);
    }
}


function filterTransactions() {
    const searchInput = document.getElementById('searchInput');
    const filter = searchInput.value.toLowerCase();
    const rows = document.querySelectorAll('.table-content tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
}


document.addEventListener('DOMContentLoaded', () => {
    fetchTransactionSummary();
    fetchRecentTransactions();
});


setInterval(() => {
    fetchTransactionSummary();
    fetchRecentTransactions();
}, 300000);