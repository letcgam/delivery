var indexProductsPrice = document.getElementsByName("product-price");

document.addEventListener("DOMContentLoaded", () => {
    for (i = 0; i < indexProductsPrice.length; i++) {
        indexProductsPrice[i].innerHTML = formatPrice(indexProductsPrice[i].innerHTML)
    }
});

function formatPrice(price) {
    return Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
    }).format(price);
};