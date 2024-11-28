function filterCheckout(filter) {
    const tableBody = document.getElementById("checkoutTableBody");
    const rows = tableBody.getElementsByTagName("tr");

    for (let row of rows) {
        const returnDate = row.querySelector("td:nth-child(5)").textContent.trim();
        row.style.display = "none"; // Default: Hide all rows

        if(filter === 'all') {
            row.style.display = "";

        } else if (filter === 'out') {
            if (returnDate === 'None') {
                row.style.display = "";
            }
            
        } else if (filter === 'closed') {
            if (returnDate !== 'None') {
                row.style.display = "";
            }
        }
    }
}