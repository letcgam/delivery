const billingStreet = document.getElementById("billing-street").value;
const billingPostalCode = document.getElementById("billing-postal-code").value;
const billingCity = document.getElementById("billing-city").value;
const billingState = document.getElementById("billing-state").value;
const billingCountry = document.getElementById("billing-country").value;
const streetInput = document.getElementById("street-input");
const postalCodeInput = document.getElementById("postal-input-code");
const cityInput = document.getElementById("city-input");
const stateInput = document.getElementById("state-input");
const countryInput = document.getElementById("country-input");
var sameAdressCheck = document.getElementById("same-adress");
const adressMessage = document.getElementById("adress-message");
const product = document.getElementsByName("product");
const total = document.getElementById("total");
var orderTotal = 0;

sameAdressCheck.addEventListener("click", () => {
    if (billingStreet == "") {
        adressMessage.hidden = false
        sameAdressCheck.checked = false 
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
})


product.forEach(element => {
    productInfo = element.children[0].children[1]
    unitPrice = productInfo.children[0]
    quant = productInfo.children[1]
    exibitPrice = productInfo.children[3]
    productTotal = element.children[1]

    productTotal.innerHTML = formatPrice(unitPrice.value * Number.parseInt(quant.innerHTML))
    exibitPrice.innerHTML = formatPrice(unitPrice.value)

    orderTotal += unitPrice.value * Number.parseInt(quant.innerHTML)
});

total.innerHTML = formatPrice(orderTotal)


function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}
