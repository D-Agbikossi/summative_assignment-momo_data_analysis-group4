function filterTransactions() {
    let input = document.getElementById("searchInput").value.toUpperCase();
    let table = document.querySelector(".table-content table");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) { // Start from 1 to skip table headers
        let tds = tr[i].getElementsByTagName("td");
        let found = false;

        for (let j = 0; j < tds.length; j++) { // Loop through all columns
            if (tds[j]) {
                let txtValue = tds[j].textContent || tds[j].innerText;
                if (txtValue.toUpperCase().indexOf(input) > -1) {
                    found = true;
                    break; // If a match is found in any column, no need to check further
                }
            }
        }

        tr[i].style.display = found ? "" : "none"; // Show/hide the row
    }
}