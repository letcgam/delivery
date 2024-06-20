const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
const ordersIds = Array.from(document.getElementsByName("order-id"));
const prices = document.getElementsByName("price");
const historyBtn = document.getElementById("see-history-btn");
const mainBtn = document.getElementById("see-main-btn");
const mainPage = document.getElementsByName("main");
const history = document.getElementsByName("history");


document.addEventListener("DOMContentLoaded", () => {
    ordersIds.forEach(id => {
        id.innerHTML = String(id.innerHTML).padStart(7, '0');
    })
});

prices.forEach(price => {
    price.innerHTML = formatPrice(Number.parseFloat(price.innerHTML))
})

mainBtn.addEventListener("click", () => {
    mainPage.hidden = false;
    history.hidden = true;
});

historyBtn.addEventListener("click", () => {
    mainPage.hidden = true;
    history.hidden = false;
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
};