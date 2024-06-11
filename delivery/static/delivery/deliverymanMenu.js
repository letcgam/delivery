const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
const ordersIds = Array.from(document.getElementsByName("order-id"));


document.addEventListener("DOMContentLoaded", () => {
    ordersIds.forEach(id => {
        id.innerHTML = String(id.innerHTML).padStart(7, '0');
    })
});