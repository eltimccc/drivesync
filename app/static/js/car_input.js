document.addEventListener("DOMContentLoaded", function () {
    var selectedCarElement = document.getElementById("selectedCar");
    var selectedCarId = document.getElementById("selectedCarId");

    if (bookingCar && bookingCar.brand && bookingCar.number && bookingCar.id) {
        selectedCarElement.value = bookingCar.brand + " " + bookingCar.number;
        selectedCarId.value = bookingCar.id;
    } else {
        selectedCarElement.value = "";
        selectedCarId.value = "";
    }

    $(".datetimepicker").datetimepicker({
        format: "d.m.Y H:i",
        step: 15,
    });
});

function openCarModal() {
    var modal = document.getElementById("carModal");
    modal.style.display = "block";
}

function closeCarModal() {
    var modal = document.getElementById("carModal");
    modal.style.display = "none";
}

function selectCar(carId, carName) {
    console.log("Выбран автомобиль:", carId, carName);
    document.getElementById("selectedCar").value = carName;
    document.getElementById("selectedCarId").value = carId;
    closeCarModal();
}

function closeIfOutside(event) {
    var modal = document.getElementById("carModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
