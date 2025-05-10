document.addEventListener("DOMContentLoaded", () => {
  const $ = id => document.getElementById(id);
  const modalContent = $("modal-content-placeholder");
  const statuses = {
    "Бронь": "#99959e",
    "Аренда": "#007bff",
    "Ожидание": "#ffc107",
    "Завершено": "#28a745",
  };

  const fetchHtml = (url, onSuccess) => {
    modalContent.innerHTML = "Загрузка...";
    fetch(url)
      .then(res => res.text())
      .then(onSuccess)
      .catch(err => {
        console.error("Ошибка:", err);
        modalContent.innerHTML = "Ошибка загрузки данных.";
      });
  };

  const toggleModal = (visible) => {
    $("custom-confirm-modal").style.display = visible ? "flex" : "none";
  };

  const attachDeleteHandlers = () => {
    $("delete-button")?.addEventListener("click", e => {
      e.preventDefault();
      toggleModal(true);
    });

    $("confirm-ok-button")?.addEventListener("click", () => {
      toggleModal(false);
      $("delete-form").submit();
    });

    $("confirm-cancel-button")?.addEventListener("click", () => toggleModal(false));
  };

  const updateBookingStatus = (bookingId, status) => {
    fetch("/booking/update_status", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ booking_id: bookingId, new_status: status })
    })
    .then(res => res.ok ? location.reload() : alert("Не удалось обновить статус"))
    .catch(err => console.error("Ошибка:", err));
  };

  const createStatusOption = (status, color, bookingId, menu) => {
    const div = document.createElement("div");
    div.textContent = status;
    Object.assign(div.style, {
      color,
      padding: "4px 9px",
      cursor: "pointer"
    });
    div.onclick = () => {
      if (confirm(`Вы действительно хотите изменить статус брони на "${status}"?`)) {
        updateBookingStatus(bookingId, status);
      }
      menu.remove();
    };
    menu.appendChild(div);
  };

  const createContextMenu = (e, bookingId) => {
    e.preventDefault();
    document.querySelector(".custom-context-menu")?.remove();

    const menu = document.createElement("div");
    menu.className = "custom-context-menu";
    Object.assign(menu.style, {
      top: `${e.pageY}px`,
      left: `${e.pageX}px`,
      position: "absolute",
      backgroundColor: "#fff",
      border: "1px solid #ccc",
      zIndex: 1000
    });

    const title = document.createElement("div");
    title.textContent = "Статус:";
    Object.assign(title.style, {
      fontWeight: "bold",
      padding: "4px 9px",
      borderBottom: "1px solid #e0e0e0",
      backgroundColor: "#fafafa"
    });

    menu.appendChild(title);
    Object.entries(statuses).forEach(([status, color]) => {
      createStatusOption(status, color, bookingId, menu);
    });

    $("context-menu-container").appendChild(menu);
  };

  window.openBookingModal = bookingId => {
    const url = modalBookingUrl.replace('0', bookingId);
    fetchHtml(url, html => {
      modalContent.innerHTML = html;
      attachDeleteHandlers();
      $("#bookingModal").modal("show");
    });
  };

  document.querySelectorAll("tbody tr").forEach(row => {
    const bookingId = row.dataset.bookingId;

    row.addEventListener("contextmenu", e => createContextMenu(e, bookingId));
    row.addEventListener("click", e => {
      if (e.button === 0) openBookingModal(bookingId);
    });
  });

  document.addEventListener("click", e => {
    const menu = document.querySelector(".custom-context-menu");
    if (menu && !menu.contains(e.target)) menu.remove();
  });

  document.addEventListener("contextmenu", e => {
    const menu = document.querySelector(".custom-context-menu");
    if (menu && !e.target.closest("tbody tr")) menu.remove();
  });

  attachDeleteHandlers();
});
