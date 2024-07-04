    document.querySelectorAll('.table thead th').forEach(header => {
        header.addEventListener('click', function() {
            const sortField = this.getAttribute('data-sort');
            if (!sortField) return;

            const currentUrl = new URL(window.location.href);
            const currentSortBy = currentUrl.searchParams.get('sort_by');
            const currentSortOrder = currentUrl.searchParams.get('sort_order');

            let newSortOrder = 'asc';
            if (currentSortBy === sortField && currentSortOrder === 'asc') {
                newSortOrder = 'desc';
            }

            currentUrl.searchParams.set('sort_by', sortField);
            currentUrl.searchParams.set('sort_order', newSortOrder);

            window.location.href = currentUrl.toString();
        });
    });

    window.addEventListener('load', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const editedBookingId = urlParams.get('edited_booking_id');

        if (editedBookingId) {
            const editedBookingRow = document.getElementById(`booking-${editedBookingId}`);
            if (editedBookingRow) {
                editedBookingRow.classList.add('highlight');
                editedBookingRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });