const orderContainer = document.getElementsByName('orders').first;
const orders = Array.from(document.getElementsByName("order"));
const ordersStatus = document.getElementsByName("status");
const price = document.getElementsByName("price");
const statusFilter = document.getElementById("status-filter");
const orderByFilter = document.getElementById("order-by-filter");
const fromDate = document.getElementById("from-date");
const toDate = document.getElementById("to-date");
const salesDiv = document.getElementById("sales-div");
const reverseSalesDiv = document.getElementById("reverse-sales-div");
const orderDate = document.getElementsByName("order-date");

statusFilter.addEventListener("change", () => {
    var status = statusFilter.value
    var len = orders.length
    for (i=0; i<len; i++) {
        if (ordersStatus[i].innerHTML.trim() != status) {
            orders[i].style.display = 'none';
        } else {
            orders[i].style.display = 'block';
        }
    }
})

orderByFilter.addEventListener("change", () => {
    if (orderByFilter.value == "newest") {
        salesDiv.hidden = false;
        reverseSalesDiv.hidden = true;
    } else {
        salesDiv.hidden = true;
        reverseSalesDiv.hidden = false;
    }
})


document.addEventListener("DOMContentLoaded", () => {
    price.forEach(price => {
        price.innerHTML = formatPrice(price.innerHTML)
    })
})

fromDate.addEventListener("change", () => {
    console.log(fromDate.value)
    orderDate.forEach(date => {
        if (date.value < fromDate.value) {
            date.parentElement.hidden = true;
        } else {
            date.parentElement.hidden = false;
        }
    })
})

toDate.addEventListener("change", () => {
    console.log(toDate.value)
    orderDate.forEach(date => {
        if (date.value > toDate.value) {
            date.parentElement.hidden = true;
        } else {
            date.parentElement.hidden = false;
        }
    })
})

orderDate.forEach(orderDate => {
    let date = new Date();
    
    let year = date.getFullYear();
    let month = String(date.getMonth() + 1).padStart(2, '0');
    let day = String(date.getDate()).padStart(2, '0');
    
    orderDate.value = `${year}-${month}-${day}`;
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}