var price = document.getElementsByName("price");
const orderId = Array.from(document.getElementsByName("order-id"));
const orderStatus = Array.from(document.getElementsByName("order-status"));
const shippingStatus = document.getElementById("status");

// Array.from(shippingStatus.children).forEach(item => {
//     children = Array.from(item.children)
//     children.forEach(child => {
//         child
//     })
// })

document.addEventListener("DOMContentLoaded", () => {
    price.forEach(price => {
        price.innerHTML = formatPrice(price.innerHTML)
    })
    orderId.forEach(id => {
        id.innerHTML = String(id.innerHTML).padStart(7, '0');
    })
    orderStatus.forEach(status => {
        status.innerHTML = status.innerHTML.charAt(0).toUpperCase() + status.innerHTML.substring(1).toLowerCase()
    })
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
};