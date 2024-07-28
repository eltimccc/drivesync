document.addEventListener('DOMContentLoaded', function() {
    const filterInput = document.getElementById('filterInput');
    const filterForm = document.getElementById('filterForm');
  
    // Загрузка сохраненного фильтра из localStorage
    const savedFilter = localStorage.getItem('bookingFilter');
    if (savedFilter) {
      filterInput.value = savedFilter;
    }
  
    // Обработчик изменения значения фильтра
    filterInput.addEventListener('input', function() {
      localStorage.setItem('bookingFilter', filterInput.value);
      filterTableRows(); // Вызываем функцию фильтрации
    });
  
    // Обработчик отправки формы
    filterForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Отменяем стандартное поведение формы
      filterTableRows(); // Вызываем функцию фильтрации
    });
  
    // Функция фильтрации таблицы
    function filterTableRows() {
      const filterText = filterInput.value.trim().toLowerCase(); // Приводим текст фильтра к нижнему регистру
      if (filterText.length < 2) {
        // Если текст фильтра короче двух символов, показываем все строки
        document.querySelectorAll('.table-hover tbody tr').forEach(row => {
          row.style.display = '';
        });
        return;
      }
  
      const tableRows = document.querySelectorAll('.table-hover tbody tr');
  
      tableRows.forEach(row => {
        let rowMatches = false;
  
        Array.from(row.cells).forEach(cell => {
          const cellText = cell.textContent.trim().toLowerCase();
          if (cellText.includes(filterText)) {
            rowMatches = true;
          }
        });
  
        row.style.display = rowMatches ? '' : 'none'; // Показываем или скрываем строку
      });
    }
  
    // Вызываем функцию фильтрации при загрузке страницы
    filterTableRows();
  
    // Очистка сохраненного фильтра при обновлении страницы
    window.addEventListener('beforeunload', function() {
      localStorage.removeItem('bookingFilter');
    });
  });
  