var price = document.getElementsByName("price");
const orderId = document.getElementById("order-id");
const orderStatus = Array.from(document.getElementById("status").children);

orderStatus[0].classList.add("text-light");
orderStatus[0].children[0].classList.add("text-light");

document.addEventListener("DOMContentLoaded", () => {
    price.forEach(price => {
        price.innerHTML = formatPrice(price.innerHTML)
    })
    orderId.innerHTML = String(orderId.innerHTML).padStart(7, '0');
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
};