$(document).ready(function () {
    var dateSelected = false;

    $('#start_date').datetimepicker({
        format: 'Y-m-d H:i',
        step: 30,
        onSelectDate: function (ct) {
            dateSelected = true;
        },
        onSelectTime: function (ct) {
            if (dateSelected) {
                $('#end_date').datetimepicker('show');
                dateSelected = false;  // Сброс для следующего использования
            }
        }
    });

    $('#end_date').datetimepicker({
        format: 'Y-m-d H:i',
        step: 30
    });
});