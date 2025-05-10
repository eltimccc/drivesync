document.addEventListener("DOMContentLoaded", function () {
  window.openBookingModal = function (bookingId) {
    const modalContentPlaceholder = document.getElementById("modal-content-placeholder");
    modalContentPlaceholder.innerHTML = "Загрузка...";

    const fetchUrl = window.bookingModalUrl.replace("0", bookingId);

    fetch(fetchUrl)
      .then((response) => response.text())
      .then((data) => {
        modalContentPlaceholder.innerHTML = data;
        attachDeleteEvent();
        $("#bookingModal").modal("show");
      })
      .catch((error) => {
        modalContentPlaceholder.innerHTML = "Ошибка загрузки данных";
        console.error("Ошибка:", error);
      });
  };

  function attachDeleteEvent() {
    const deleteButton = document.getElementById("delete-button");
    const confirmOkButton = document.getElementById("confirm-ok-button");
    const confirmCancelButton = document.getElementById("confirm-cancel-button");

    if (deleteButton) {
      deleteButton.addEventListener("click", function (event) {
        event.preventDefault();
        document.getElementById("custom-confirm-modal").style.display = "flex";
      });
    }

    if (confirmOkButton) {
      confirmOkButton.addEventListener("click", function () {
        document.getElementById("custom-confirm-modal").style.display = "none";
        document.getElementById("delete-form").submit();
      });
    }

    if (confirmCancelButton) {
      confirmCancelButton.addEventListener("click", function () {
        document.getElementById("custom-confirm-modal").style.display = "none";
      });
    }
  }

  attachDeleteEvent();
});
