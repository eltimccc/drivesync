document.addEventListener('DOMContentLoaded', function() {
  // Модальное окно бронирования
  window.openBookingModal = function(bookingId, url) {
    const modalContentPlaceholder = document.getElementById('modal-content-placeholder');
    modalContentPlaceholder.innerHTML = 'Загрузка...';

    fetch(url)
      .then(response => response.text())
      .then(data => {
        modalContentPlaceholder.innerHTML = data;
        attachDeleteEvent(); // Привязка событий к новым элементам
        $('#bookingModal').modal('show');
      })
      .catch(error => {
        modalContentPlaceholder.innerHTML = 'Ошибка загрузки данных';
        console.error('Ошибка:', error);
      });
  }

  // Функция привязки событий удаления
  function attachDeleteEvent() {
    const deleteButton = document.getElementById('delete-button');
    const confirmOkButton = document.getElementById('confirm-ok-button');
    const confirmCancelButton = document.getElementById('confirm-cancel-button');

    if (deleteButton) {
      deleteButton.addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('custom-confirm-modal').style.display = 'flex';
      });
    }

    if (confirmOkButton) {
      confirmOkButton.addEventListener('click', function() {
        document.getElementById('custom-confirm-modal').style.display = 'none';
        document.getElementById('delete-form').submit();
      });
    }

    if (confirmCancelButton) {
      confirmCancelButton.addEventListener('click', function() {
        document.getElementById('custom-confirm-modal').style.display = 'none';
      });
    }
  }

  // Вызываем привязку событий удаления при загрузке страницы
  attachDeleteEvent();
});