var totalPrice = document.getElementById("total-price");
var quantityInput = document.getElementById("quantity-input");
var productPrice = document.getElementById("product-price");

quantityInput.addEventListener("change", () => {
    const accounting = require('../../static/accounting');
    const formattedPrice = productPrice.innerHTML;
    const numberValue = accounting.unformat(formattedPrice);

    price = quantityInput.value * numberValue;
    console.log(productPrice.innerHTML)
    totalPrice.innerHTML = formatPrice(price);
});

document.addEventListener("DOMContentLoaded", () => {
    productPrice.innerHTML = formatPrice(productPrice.innerHTML);
});

function formatPrice(price) {
    return Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
    }).format(price);
}
