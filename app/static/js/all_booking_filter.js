document.addEventListener('DOMContentLoaded', function() {
  const filterInput = document.getElementById('filterInput');
  const statusFilter = document.getElementById('statusFilter');
  const filterForm = document.getElementById('filterForm');
  const tableRows = document.querySelectorAll('.table-hover tbody tr');

  const loadFilterFromLocalStorage = (key, element) => {
    const savedValue = localStorage.getItem(key);
    if (savedValue) element.value = savedValue;
  };

  const saveFilterToLocalStorage = (key, value) => {
    localStorage.setItem(key, value);
  };

  const filterTableRows = () => {
    const filterText = filterInput.value.trim().toLowerCase();
    const statusText = statusFilter.value.trim().toLowerCase();

    tableRows.forEach(row => {
      const rowMatchesFilter = Array.from(row.cells).some(cell =>
        cell.textContent.trim().toLowerCase().includes(filterText)
      );

      const rowStatus = row.className.split('-').pop();
      let rowMatchesStatus = true;

      if (statusText === "in_work") {
        const workingStatuses = ["аренда", "бронь", "ожидание"];
        rowMatchesStatus = workingStatuses.includes(rowStatus);
      } else {
        rowMatchesStatus = !statusText || rowStatus === statusText;
      }

      row.style.display = rowMatchesFilter && rowMatchesStatus ? '' : 'none';
    });
  };

  loadFilterFromLocalStorage('bookingFilter', filterInput);
  loadFilterFromLocalStorage('statusFilter', statusFilter);

  filterInput.addEventListener('input', () => {
    saveFilterToLocalStorage('bookingFilter', filterInput.value);
    if (filterInput.value.length >= 2 || filterInput.value.length === 0) {
      filterTableRows();
    }
  });

  statusFilter.addEventListener('change', () => {
    saveFilterToLocalStorage('statusFilter', statusFilter.value);
    filterTableRows();
  });

  filterForm.addEventListener('submit', event => {
    event.preventDefault();
    filterTableRows();
  });

  filterTableRows();

  window.addEventListener('beforeunload', () => {
    localStorage.removeItem('bookingFilter');
    localStorage.removeItem('statusFilter');
  });
});
