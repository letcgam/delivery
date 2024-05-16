const editProfileBtn = document.getElementById("edit-profile-btn");
const confirmProfileBtn = document.getElementById("confirm-profile-btn");
const profileInputs = Array.from(document.getElementsByClassName("profile-input"));
const profileLabels = Array.from(document.getElementsByClassName("profile-label"));

const editAdressBtn = document.getElementById("edit-adress-btn");
const confirmAdressBtn = document.getElementById("confirm-adress-btn");
const adressInputs = Array.from(document.getElementsByClassName("adress-input"));
const adressLabels = Array.from(document.getElementsByClassName("adress-label"));

const editLicenseBtn = document.getElementById("edit-license-btn");
const confirmLicenseBtn = document.getElementById("confirm-license-btn");
const licenseInputs = Array.from(document.getElementsByClassName("license-input"));
const licenseLabels = Array.from(document.getElementsByClassName("license-label"));

const labels = Array.from(document.getElementsByClassName("label"));
const inputs = Array.from(document.getElementsByClassName("account-input"));

const documentTypeInput = document.getElementById("document-type-input");
var docNumberInput = document.getElementById("doc-number-input");
var docNumberLabel = document.getElementById("doc-number-label");

const evt = new Event('DOMContentLoaded');

const birthInput = document.getElementById("birth-input");
var phoneNumberInput = document.getElementById('phone-number');

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
        
        const userType = document.getElementById("user-type").value
        if (userType.includes("deliveryman") || userType.includes("seller")) {
            input.required = true;
        }
    })
    confirmProfileBtn.hidden = true;
    confirmAdressBtn.hidden = true;
    if (confirmLicenseBtn) {
        confirmLicenseBtn.hidden = true;
    }
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
    if (documentTypeInput.value == "SSN") {
        docNumberLabel.innerHTML = "SSN"
        docNumberInput.placeholder="XXX-XX-XXXX"
    } else {
        docNumberLabel.innerHTML = "EIN"
        docNumberInput.placeholder="XX-XXXXXXX"
    }
})

docNumberInput.addEventListener("input", () => {
    var docNumber = docNumberInput.value.replace(/\D/g, '');
    var formattedDoc = ""
    var type = documentTypeInput.value;

    if (formattedDoc != undefined) {
        if (type == "SSN") {
            formattedDoc += docNumber.slice(0, 3);
            if (docNumber.length > 3) {
                formattedDoc += '-' + docNumber.slice(3, 5);
            }
            if (docNumber.length > 5) {
                formattedDoc += '-' + docNumber.slice(5, 9);
            }
        } else {
            formattedDoc += docNumber.slice(0, 2);
            if (docNumber.length > 2) {
                formattedDoc += '-' + docNumber.slice(2, 9);
            }
        }
        docNumberInput.value = formattedDoc
    }
});

function hide(elem) {
    elem.style.opacity = 0;
    elem.style.height = 0;
    elem.style.width = 0;
    elem.style.padding = 0;
    elem.style.margin = 0;
}

phoneNumberInput.addEventListener('input', () => {
    var phoneNumber = phoneNumberInput.value;
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
    phoneNumberInput.value = formattedPhoneNumber;
});

function validateForm() {
    alert("hi")
    profileInputs.forEach(input => {
        if (input.value == "") {
            return false;
        }
    })
    return true;
}