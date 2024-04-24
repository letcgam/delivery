var totalPrice = document.getElementById("total-price");
var quantityInput = document.getElementById("quantity-input");
var productPrice = document.getElementById("product-price");
const productUnitPrice = document.getElementById("product-unit-price");

quantityInput.addEventListener("change", () => {
    price = quantityInput.value * productUnitPrice.innerHTML;
    totalPrice.innerHTML = formatPrice(price);
});


document.addEventListener("DOMContentLoaded", () => {
    productPrice.innerHTML = formatPrice(productUnitPrice.innerHTML);
    totalPrice.innerHTML = productPrice.innerHTML
});

function formatTotalPrice() {
    price = quantityInput.value * productPrice.innerHTML;
    totalPrice.innerHTML = formatPrice(price);
}

function formatPrice(price) {
    return Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
    }).format(price);
}
