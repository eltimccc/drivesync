document.addEventListener("DOMContentLoaded", function () {
  const filterInput = document.getElementById("filterInput");
  const statusFilter = document.getElementById("statusFilter");
  const tableRows = document.querySelectorAll("tbody tr");

  const filterTableRows = () => {
    const filterText = filterInput.value.trim().toLowerCase();
    const statusText = statusFilter.value.trim().toLowerCase();

    tableRows.forEach(row => {
      const rowMatchesFilter = Array.from(row.cells).some(cell =>
        cell.textContent.trim().toLowerCase().includes(filterText)
      );

      const match = row.className.match(/status-(\S+)/);
      const rowStatus = match ? match[1] : "";
      const isOverdue = row.classList.contains('overdue-booking');

      let rowMatchesStatus = true;

      if (statusText === "in_work") {
        const workingStatuses = ["аренда", "бронь", "ожидание"];
        rowMatchesStatus = workingStatuses.includes(rowStatus);

        if (isOverdue && (rowStatus === "аренда" || rowStatus === "бронь")) {
          row.classList.add("overdue-highlight");
        } else {
          row.classList.remove("overdue-highlight");
        }
      } else {
        rowMatchesStatus = !statusText || rowStatus === statusText;

        row.classList.remove("overdue-highlight");
      }

      row.style.display = rowMatchesFilter && rowMatchesStatus ? "" : "none";
    });
  };

  filterInput.addEventListener("input", filterTableRows);
  statusFilter.addEventListener("change", filterTableRows);

  filterTableRows();
});