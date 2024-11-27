function filterTable(filter, currentUserName, isAdmin) {
    const tableBody = document.getElementById("employeeTableBody");
    const rows = tableBody.getElementsByTagName("tr");

    let currentUserReportsToId = null;
    let currentUserId = null;

    // First loop: Find current user and their manager's ID
    for (let row of rows) {
        const username = row.querySelector("td:nth-child(6)").textContent.trim();
        if (username === currentUserName) {
            currentUserId = row.querySelector("td:nth-child(1)").textContent.trim();
            const reportsToName = row.getAttribute("data-reports-to");

            if (reportsToName !== "null") {
                for (let managerRow of rows) {
                    const managerName = `${managerRow.querySelector("td:nth-child(2)").textContent.trim()} ${managerRow.querySelector("td:nth-child(3)").textContent.trim()}`;
                    if (reportsToName === managerName) {
                        currentUserReportsToId = managerRow.querySelector("td:nth-child(1)").textContent.trim();
                        break;
                    }
                }
            }
            break;
        }
    }

    // Second loop: Apply filters
    for (let row of rows) {
        const reportsTo = row.getAttribute("data-reports-to");
        const employeeId = row.querySelector("td:nth-child(1)").textContent.trim();

        row.style.display = "none";

        if (isAdmin) {
            // Admin users see everything
            if (filter === "all") {
                row.style.display = "";
            } else if (filter === "leads") {
                if (reportsTo === "null") {
                    row.style.display = "";
                }
            } else if (filter === "reports") {
                if (reportsTo !== "null") {
                    row.style.display = "";
                }
            }
        } else { // Not Admin
            if (filter === "all") {
                // Show current user, their manager (reportsTo), and anyone reporting to the same manager
                if (
                    employeeId === currentUserId ||                      // Current user
                    employeeId === currentUserReportsToId ||              // Manager (Reports To)
                    reportsTo === currentUserReportsToId ||               // Employee reporting to the same manager
                    reportsTo === currentUserId                           // Anyone reporting directly to the current user
                ) {
                    row.style.display = "";
                }
            } else if (filter === "leads") {
                if (reportsTo === "null" && currentUserReportsTo === "null") {
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