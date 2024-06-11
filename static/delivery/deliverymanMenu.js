const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
const ordersIds = Array.from(document.getElementsByName("order-id"));


document.addEventListener("DOMContentLoaded", () => {
    price.forEach(price => {
        price.innerHTML = formatPrice(price.innerHTML)
    })
    ordersIds.forEach(id => {
        id.innerHTML = String(id.innerHTML).padStart(7, '0');
    })
    orderDate.forEach(date => {
        date.innerHTML = String(date.innerHTML).padStart(2, '0');
    })
    orderStatus.forEach(status => {
        status.innerHTML = status.innerHTML.charAt(0).toUpperCase() + status.innerHTML.substring(1).toLowerCase()
    })
});