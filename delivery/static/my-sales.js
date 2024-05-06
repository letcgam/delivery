const orderContainer = document.getElementsByName('orders').first();
const orders = Array.from(document.getElementsByName("order"));
const ordersStatus = document.getElementsByName("status");
const orderDates = document.getElementsByName("order-date")
const price = document.getElementsByName("price");
const statusFilter = document.getElementById("status-filter");
const orderByFilter = document.getElementById("order-by-filter");
const dateFilter = document.getElementById("date-filter");



statusFilter.addEventListener("change", () => {
    var status = statusFilter.value
    var len = orders.length
    for (i=0; i<len; i++) {
        console.log(status)
        console.log(ordersStatus[i].innerHTML)
        if (ordersStatus[i].innerHTML.trim() != status) {
            orders[i].style.display = 'none';
        } else {
            orders[i].style.display = 'block';
        }
    }
})

orderByFilter.addEventListener("change", () => {
    for (i=0; i<len; i++) {
        divsArray.sort((a, b) => {
            var dateA = new Date().textContent);
            var dateB = new Date().textContent);
            return dateA - dateB; // Ordene de forma decrescente (mais recente para mais antiga)
        });
        divsArray.forEach(div => orderContainer.appendChild(div));
    }
})


document.addEventListener("DOMContentLoaded", () => {
    price.forEach(price => {
        price.innerHTML = formatPrice(price.innerHTML)
    })
})

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}