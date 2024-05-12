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
