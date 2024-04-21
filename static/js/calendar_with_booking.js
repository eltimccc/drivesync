document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridWeek',
        events: [
            {% for booking in bookings %}
            {
                title: '{{ booking.car }}',
                start: '{{ booking.start }}',
                end: '{{ booking.end }}',
                url: '{{ url_for("view_booking", booking_id=booking.id) }}',
                color: '{{ booking.status_color }}'
            }{% if not loop.last %},{% endif %}
            {% endfor %}
        ],
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridYear,dayGridDay,dayGridWeek'
        },
        eventClick: function(info) {
            info.jsEvent.preventDefault();
            $('#bookingModal').modal('show').find('.modal-content').load(info.event.url);
        },
        dateClick: function(info) {
            calendar.gotoDate(info.date);
            calendar.changeView('dayGridDay');
        },
        locale: 'ru',
        monthNames: [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ],
        buttonText: {
            month: 'Месяц',
            week: 'Неделя',
            year: 'Год',
            day: 'День',
        }
    });

    calendar.render();


    $('button[data-bs-target="#addBookingModal"]').on('click', function() {
        $.ajax({
            url: '/add_booking',
            type: 'GET',
            success: function(response) {
                $('#addBookingModalContent').html(response);
                $('#addBookingModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    });


    $('button[data-bs-target="#addCarModal"]').on('click', function() {
        $.ajax({
            url: '/add_car',
            type: 'GET',
            success: function(response) {
                $('#addCarModalContent').html(response);
                $('#addCarModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    });
});