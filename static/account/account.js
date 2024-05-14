const editProfileBtn = document.getElementById("edit-profile-btn");
const confirmProfileBtn = document.getElementById("confirm-profile-btn");
const profileInputs = Array.from(document.getElementsByClassName("profile-input"));
const profileLabels = Array.from(document.getElementsByClassName("profile-label"));

const editAdressBtn = document.getElementById("edit-adress-btn");
const confirmAdressBtn = document.getElementById("confirm-adress-btn");
const adressInputs = Array.from(document.getElementsByClassName("adress-input"));
const adressLabels = Array.from(document.getElementsByClassName("adress-label"));

const editLicenseBtn = document.getElementById("edit-license-btn");
if (editAdressBtn) {
    const confirmLicenseBtn = document.getElementById("confirm-license-btn");
    const licenseInputs = Array.from(document.getElementsByClassName("license-input"));
    const licenseLabels = Array.from(document.getElementsByClassName("license-label"));
}

const labels = Array.from(document.getElementsByClassName("label"));
const inputs = Array.from(document.getElementsByClassName("form-control"));

const documentTypeInput = document.getElementById("document-type-input");
const ssnInput = document.getElementById("ssn-input");
const einInput = document.getElementById("ein-input");

const evt = new Event('DOMContentLoaded');

const birthInput = document.getElementById("birth-input");

if (birthInput.value == "") {
    birthInput.classList.replace("text-light", "text-secondary");
}

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
    confirmLicenseBtn.hidden = true;
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
    hide(editProfileBtn)
})

if (editLicenseBtn) {
    editLicenseBtn.addEventListener('click', () => {
        licenseLabels.forEach(element => {
            element.classList.remove("text-secondary")
        });
        licenseInputs.forEach(input => {
            input.disabled = false
            input.classList.remove("border-secondary")
        })
        confirmLicenseBtn.hidden = false
        hide(editLicenseBtn)
    })
}

editAdressBtn.addEventListener('click', () => {
    adressLabels.forEach(element => {
        element.classList.remove("text-secondary")
    });
    adressInputs.forEach(input => {
        input.disabled = false
        input.classList.remove("border-secondary")
    })
    confirmAdressBtn.hidden = false
    hide(editAdressBtn)
})


confirmProfileBtn.addEventListener('click', () => {
    location.reload()
})

confirmAdressBtn.addEventListener('click', () => {
    location.reload()
})

documentTypeInput.addEventListener("change", () => {
    if (this.value == "SSN") {
        ssnInput.hidden = false;
        einInput.hidden = true;
    } else {
        ssnInput.hidden = true;
        einInput.hidden = false;
    }
})


function hide(elem) {
    elem.style.opacity = 0;
    elem.style.height = 0;
    elem.style.width = 0;
    elem.style.padding = 0;
    elem.style.margin = 0;
}


var inputPhoneNumber = document.getElementById('phone-number');

inputPhoneNumber.addEventListener('input', function() {
    var phoneNumber = inputPhoneNumber.value;
    phoneNumber = phoneNumber.replace(/\D/g, '');

    var formattedPhoneNumber = '+';
    formattedPhoneNumber += phoneNumber.slice(0, 2) + ' ';

    if (phoneNumber.length > 2) {
        formattedPhoneNumber += '(' + phoneNumber.slice(2, 4) + ') ';
    }
    if (phoneNumber.length > 4) {
        formattedPhoneNumber += phoneNumber.slice(4, 9);
    }
    if (phoneNumber.length > 9) {
        formattedPhoneNumber += '-' + phoneNumber.slice(9);
    }
    inputPhoneNumber.value = formattedPhoneNumber;
});