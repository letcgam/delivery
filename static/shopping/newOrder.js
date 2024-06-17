const firstName = document.getElementById("first-name");
const lastName = document.getElementById("first-name");
const phoneNumber = document.getElementById("phone-number");
const email = document.getElementById("email");
const billingStreet = document.getElementById("billing-street").value;
const billingPostalCode = document.getElementById("billing-postal-code").value;
const billingCity = document.getElementById("billing-city").value;
const billingState = document.getElementById("billing-state").value;
const billingCountry = document.getElementById("billing-country").value;
const streetInput = document.getElementById("street-input");
const postalCodeInput = document.getElementById("postal-code-input");
const cityInput = document.getElementById("city-input");
const stateInput = document.getElementById("state-input");
const countryInput = document.getElementById("country-input");
var sameAdressCheck = document.getElementById("same-adress");
const adressMessage = document.getElementById("adress-message");
const product = document.getElementsByName("product");
const total = document.getElementById("total");
var orderTotal = 0;
const cardCvv = document.getElementById("card-cvv");
const cardNumber = document.getElementById("card-number");
const cardExpDate = document.getElementById("card-expiration");
const shipping = document.getElementById("shipping");
const shippingPrice = document.getElementById("shipping-price");
const checkoutBtn = document.getElementById("checkout-btn");
const completeBtn = document.getElementById("complete-btn");
const returnBtn = document.getElementById("return-btn");
const form1 = Array.from(document.getElementsByClassName("form1"));
const form2 = Array.from(document.getElementsByClassName("form2"));
const inputsForm1 = [firstName, lastName, phoneNumber, email, sameAdressCheck, streetInput, postalCodeInput, cityInput, stateInput, countryInput]

document.addEventListener("DOMContentLoaded", () => {
    checkoutBtn.disabled = true;

    form2.forEach(item => {
        item.style.height = '0px';
        item.style.opacity = 0;
        item.hidden = true;
        console.log(item);
    });

    inputsForm1.forEach(input => {
        input.addEventListener("input", () => {
            if (inputsForm1.every(input => input.value != "")) {
                checkoutBtn.disabled = false;
            } else {
                checkoutBtn.disabled = true;
            };
        });
    });
});

checkoutBtn.addEventListener("click", () => {
    shippingPrice.value = randomShipping();
    shipping.innerHTML = formatPrice(shippingPrice.value);
    total.value += shippingPrice.value;
    total.innerHTML = formatPrice(total.shippingPrice.value);

    form1.forEach(item => {
        item.style.height = '0px';
        item.style.opacity = 0;
        item.hidden = true;
        console.log(item);
    });
    form2.forEach(item => {
        item.style.height = 'auto';
        item.style.opacity = 1;
        item.hidden = false;
        console.log(item);
    });

    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

returnBtn.addEventListener("click", () => {
    form1.forEach(item => {
        item.style.height = 'auto';
        item.style.opacity = 1;
        item.hidden = false;
        console.log(item);
    });
    form2.forEach(item => {
        item.style.height = '0px';
        item.style.opacity = 0;
        item.hidden = true;
        console.log(item);
    });
})

cardCvv.addEventListener("input", () => {
    if (cardCvv.value.length > 3) {
        cardCvv.value = cardCvv.value.slice(0, 3);
    }
});

cardNumber.addEventListener("input", () => {
    var number = cardNumber.value.replace(/\D/g, "");
    var formattedNumber = "" + number.slice(0, 4);

    if (number.length > 4) {
        formattedNumber += "-" + number.slice(4, 8);
    }
    if (number.length > 8) {
        formattedNumber += "-" + number.slice(8, 12);
    }
    if (number.length > 12) {
        formattedNumber += "-" + number.slice(12, 16);
    }

    cardNumber.value = formattedNumber;
});

cardExpDate.addEventListener("input", () => {
    var date = cardExpDate.value.replace(/\D/g, "");
    var formattedDate = "" + date.slice(0, 2);

    if (date.length > 2) {
        formattedDate += "/" + date.slice(2, 4);
    }

    cardExpDate.value = formattedDate;
});

sameAdressCheck.addEventListener("click", () => {
    if (billingStreet == "") {
        adressMessage.hidden = false;
        sameAdressCheck.checked = false;
    } else {
        if (sameAdressCheck.checked == true) {
            streetInput.value = billingStreet;
            postalCodeInput.value = billingPostalCode;
            cityInput.value = billingCity;
            stateInput.value = billingState;
            countryInput.value = billingCountry;
        } else {;
            streetInput.value = "";
            postalCodeInput.value = "";
            cityInput.value = "";
            stateInput.value = "";
            countryInput.value = "";
        }
    }
});

product.forEach(element => {
    productInfo = element.children[0].children[1];
    unitPrice = productInfo.children[0];
    quant = productInfo.children[1];
    exibitPrice = productInfo.children[3];
    productTotal = element.children[1];

    productTotal.innerHTML = formatPrice(unitPrice.value * Number.parseInt(quant.innerHTML));
    exibitPrice.innerHTML = formatPrice(unitPrice.value);

    orderTotal += unitPrice.value * Number.parseInt(quant.innerHTML);
});

total.value = orderTotal;
total.innerHTML = formatPrice(orderTotal);

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}

function randomShipping() {
    // Returns a random float between 20 and 60.
    return Math.random() * 40 + 20;
}