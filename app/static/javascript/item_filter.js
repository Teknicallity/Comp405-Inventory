function filterItem(filter) {
    const tableBody = document.getElementById("itemTableBody");
    const rows = tableBody.getElementsByTagName("tr");

    for (let row of rows) {
        const status = row.querySelector("td:nth-child(6)").textContent.trim();
        row.style.display = "none"; // Default: Hide all rows

        if (filter === 'all') {
            row.style.display = "";

        } else if (filter === 'available') {
            if (status === 'Available') {
                row.style.display = "";
            }
            
        } else if (filter === 'checked-out') {
            if (status === 'Checked Out') {
                row.style.display = "";
            }
        }
    }
}