async function fetchTransactionSummary() {
    try {
        const response = await fetch('http://localhost:3000/api/transaction-summary');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();

        if (!Array.isArray(data)) {
            throw new Error("Unexpected data format from API.");
        }

        const summaryElements = {
            incomings: document.getElementById("incomings"),
            outgoings: document.getElementById("outgoings"),
            withdrawals: document.getElementById("withdrawals"),
            bills: document.getElementById("bills"),
        };

        data.forEach(entry => {
            if (entry.category && summaryElements[entry.category.toLowerCase()]) {
                summaryElements[entry.category.toLowerCase()].textContent = entry.transaction_count;
            }
        });

    } catch (error) {
        console.error('Error fetching transaction summary:', error);
    }
}

async function fetchRecentTransactions() {
    try {
        console.log('Fetching transactions...');

        const response = await fetch('http://localhost:3000/api/recent-transactions');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        console.log('Fetched Data:', data);

        const transactionsTableBody = document.getElementById('transactions-table-body');
        if (!transactionsTableBody) {
            console.error('Error: Transactions table body not found!');
            return;
        }

        transactionsTableBody.innerHTML = '';

        data.forEach(transaction => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${transaction.transaction_id}</td>
                <td>${transaction.category}</td>
                <td>${transaction.sms_body}</td>
                <td>${transaction.date}</td>
                <td>${transaction.time}</td>
                <td>${transaction.amount}</td>
                <td>${transaction.type}</td> 
            `;

            transactionsTableBody.appendChild(row);
        });

    } catch (error) {
        console.error('Error fetching transactions:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchTransactionSummary();
    fetchRecentTransactions();

    document.getElementById('searchInput').addEventListener('input', filterTransactions);

    setInterval(() => {
        fetchTransactionSummary();
        fetchRecentTransactions();
    }, 300000);
});

function filterTransactions() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    document.querySelectorAll('#transactions-table-body tr').forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(searchInput) ? '' : 'none';
    });
}