document.addEventListener('DOMContentLoaded', function() {
    const filterInput = document.getElementById('filterInput');
    const carContainer = document.getElementById('carContainer');
    const carCards = carContainer.getElementsByClassName('car-card');

    filterInput.addEventListener('input', function() {
      const filterText = filterInput.value.trim().toLowerCase();

      Array.from(carCards).forEach(card => {
        const cardTitle = card.querySelector('.card-title').textContent.trim().toLowerCase();

        const matchesFilter = cardTitle.includes(filterText);

        card.style.display = matchesFilter ? '' : 'none';
      });
    });
  });