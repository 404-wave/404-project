//holds all form validations for the app

function redAlert(errorField) {
    console.log(errorField);
    el = document.getElementById("id_"+errorField).parentElement
    el.classList.add("redAlert");
}  