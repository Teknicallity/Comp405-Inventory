function filterTable(filter, currentUserName, isAdmin) {
    const tableBody = document.getElementById("employeeTableBody");
    const rows = tableBody.getElementsByTagName("tr");

    let currentUserReportsToId = null; // The manager of the current user
    let currentUserId = null; // The ID of the logged-in user

    // First loop: Find the logged-in user's ID and their manager's ID
    for (let row of rows) {
        const username = row.querySelector("td:nth-child(6)").textContent.trim();
        if (username === currentUserName) {
            currentUserId = row.querySelector("td:nth-child(1)").textContent.trim();
            const reportsToName = row.querySelector("td:nth-child(5)").textContent.trim();

            // Find the manager's ID if "Reports To" is not "None"
            if (reportsToName !== "None") {
                for (let managerRow of rows) {
                    const managerName = `${managerRow.querySelector("td:nth-child(2)").textContent.trim()} ${managerRow.querySelector("td:nth-child(3)").textContent.trim()}`;
                    if (reportsToName === managerName) {
                        currentUserReportsToId = managerRow.querySelector("td:nth-child(1)").textContent.trim();
                        break;
                    }
                }
            }
            break; // Exit the loop once we find the logged-in user
        }
    }

    // Second loop: Apply filters
    for (let row of rows) {
        const employeeId = row.querySelector("td:nth-child(1)").textContent.trim();
        const reportsToName = row.querySelector("td:nth-child(5)").textContent.trim();
        const reportsTo = [...rows].find(r =>
            `${r.querySelector("td:nth-child(2)").textContent.trim()} ${r.querySelector("td:nth-child(3)").textContent.trim()}` === reportsToName
        )?.querySelector("td:nth-child(1)").textContent.trim();

        row.style.display = "none"; // Default: Hide all rows

        if (isAdmin) {
            // Admin users see everything
            if (filter === "all") {
                row.style.display = "";
            } else if (filter === "leads") {
                if (reportsToName === "None") {
                    row.style.display = "";
                }
            } else if (filter === "reports") {
                if (reportsTo === currentUserId) {
                    row.style.display = "";
                }
            }
        } else {
            // Non-admin user
            if (filter === "all") {
                // Show current user, their manager, and anyone reporting to the same manager
                if (
                    employeeId === currentUserId || // Current user
                    employeeId === currentUserReportsToId || // Manager (Reports To)
                    reportsTo === currentUserReportsToId || // Anyone reporting to the same manager
                    reportsTo === currentUserId // Anyone reporting directly to the current user
                ) {
                    row.style.display = "";
                }
            } else if (filter === "leads") {
                if (reportsToName === "None" && currentUserReportsToId === "None") {
                    if (employeeId === currentUserId) {
                        row.style.display = "";
                    }
                } else if (currentUserReportsToId === employeeId) {
                    row.style.display = "";
                }
            } else if (filter === "reports") {
                if (reportsTo === currentUserId) {
                    row.style.display = "";
                }
            }
        }
    }
}