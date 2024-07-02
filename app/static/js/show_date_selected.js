  $(document).ready(function() {
    var dateSelected = false;

    $('#start_datetime').datetimepicker({
      format: 'd.m.Y H:i',
      step: 30,
      onSelectDate: function(ct) {
        dateSelected = true;
      },
      onSelectTime: function(ct) {
        if (dateSelected) {
          $('#end_datetime').datetimepicker('show');
          dateSelected = false;  // Reset for the next use
        }
      }
    });

    $('#end_datetime').datetimepicker({
      format: 'd.m.Y H:i',
      step: 30
    });
  });
