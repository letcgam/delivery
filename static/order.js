var price = document.getElementsByName("price");
const orderId = Array.from(document.getElementsByName("order-id"));


orderId.innerHTML = format

document.addEventListener("DOMContentLoaded", () => {
    for (i = 0; i < price.length; i++) {
        price[i].innerHTML = formatPrice(price[i].innerHTML)
    }
    orderId.forEach(id => {
        id.innerHTML = "String(id.innerHTML).padStart(7, '0');"
    })
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
};