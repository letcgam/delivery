const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
const ordersIds = Array.from(document.getElementsByName("order-id"));
const prices = document.getElementsByName("price");

document.addEventListener("DOMContentLoaded", () => {
    ordersIds.forEach(id => {
        id.innerHTML = String(id.innerHTML).padStart(7, '0');
    })
});

prices.forEach(price => {
    price.innerHTML = formatPrice(Number.parseFloat(price.innerHTML))
})

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
};