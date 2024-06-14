const prices = document.getElementsByName("price");
const orderId = Array.from(document.getElementsByName("order-id"));
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));


document.addEventListener("DOMContentLoaded", () => {
    prices.forEach(price => {
        price.innerHTML = formatPrice(price.innerHTML)
    })
    orderId.forEach(id => {
        id.innerHTML = String(id.innerHTML).padStart(7, '0');
    })
})

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}