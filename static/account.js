const editProfileBtn = document.getElementById("edit-profile-btn");
const confirmProfileBtn = document.getElementById("confirm-profile-btn");

const editAdressBtn = document.getElementById("edit-adress-btn");
const confirmAdressBtn = document.getElementById("confirm-adress-btn");

const labels = Array.from(document.getElementsByClassName("label"));
const inputs = Array.from(document.getElementsByClassName("form-control"));

const profileInputs = Array.from(document.getElementsByClassName("profile-input"));
const profileLabels = Array.from(document.getElementsByClassName("profile-label"));

const adressInputs = Array.from(document.getElementsByClassName("adress-input"));
const adressLabels = Array.from(document.getElementsByClassName("adress-label"));

const evt = new Event('DOMContentLoaded');




document.addEventListener("DOMContentLoaded", () => {
    labels.forEach(element => {
        element.classList.add("text-secondary")
    });
    inputs.forEach(input => {
        input.disabled = true
        input.classList.add("border-secondary")
    })
    confirmProfileBtn.hidden = true;
    confirmAdressBtn.hidden = true;
})
 

editProfileBtn.addEventListener('click', () => {
    profileLabels.forEach(element => {
        element.classList.remove("text-secondary")
    });
    profileInputs.forEach(input => {
        input.disabled = false
        input.classList.remove("border-secondary")
    })

    confirmProfileBtn.hidden = false
    this.classList.add("hidden");
})


editAdressBtn.addEventListener('click', () => {
    adressLabels.forEach(element => {
        element.classList.remove("text-secondary")
    });
    adressInputs.forEach(input => {
        input.disabled = false
        input.classList.remove("border-secondary")
    })
    confirmAdressBtn.hidden = false
    editAdressBtn.hidden = true
})


confirmProfileBtn.addEventListener('click', () => {
    document.dispatchEvent(evt);
})