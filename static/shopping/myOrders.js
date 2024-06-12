var price = document.getElementsByName("price");
const orderId = Array.from(document.getElementsByName("order-id"));
const orderDate = Array.from(document.getElementsByName("order-date"));
const orderStatus = Array.from(document.getElementsByName("order-status"));
const orderItemPictures = Array.from(document.getElementsByClassName("square"));

orderItemPictures.forEach(image => {
    width = image.clientWidth
    image.children[0].style.heigth = String(width) + "px"
    console.log(image.children[0].style.heigth)
});

document.addEventListener("DOMContentLoaded", () => {
    price.forEach(price => {
        price.innerHTML = formatPrice(price.innerHTML)
    })
    orderId.forEach(id => {
        id.innerHTML = String(id.innerHTML).padStart(7, '0');
    })
    orderDate.forEach(date => {
        date.innerHTML = String(date.innerHTML).padStart(2, '0');
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