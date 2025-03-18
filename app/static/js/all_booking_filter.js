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

      // Определяем статус строки по классу (например, status-аренда, status-бронь)
      const match = row.className.match(/status-(\S+)/);
      const rowStatus = match ? match[1] : "";
      const isOverdue = row.classList.contains('overdue-booking');

      let rowMatchesStatus = true;

      if (statusText === "in_work") {
        // Только "аренда", "бронь", "ожидание" (НЕ "завершено" и т.д.)
        const workingStatuses = ["аренда", "бронь", "ожидание"];
        rowMatchesStatus = workingStatuses.includes(rowStatus);

        // Подсвечиваем просроченные "аренда" и "бронь"
        if (isOverdue && (rowStatus === "аренда" || rowStatus === "бронь")) {
          row.classList.add("overdue-highlight");
        } else {
          row.classList.remove("overdue-highlight");
        }
      } else {
        // Остальные фильтры работают как раньше
        rowMatchesStatus = !statusText || rowStatus === statusText;

        // Убираем подсветку при смене фильтра
        row.classList.remove("overdue-highlight");
      }

      // Отображаем строку только если совпадает с фильтром и статусом
      row.style.display = rowMatchesFilter && rowMatchesStatus ? "" : "none";
    });
  };

  // Вызываем фильтрацию при изменении поля фильтра и статуса
  filterInput.addEventListener("input", filterTableRows);
  statusFilter.addEventListener("change", filterTableRows);

  // Запускаем фильтрацию при загрузке страницы
  filterTableRows();
});