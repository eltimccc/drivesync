$(document).ready(function () {
    $(".car-input").on("mousedown", function (e) {
      e.preventDefault();
      $("#carModal").modal("show");
    });
  });

  function selectCar(carId, carDescription) {
    document.querySelector('[name="car"]').value = carId;
    document.querySelector(".car-input").value = carDescription;
    $("#carModal").modal("hide");
  }