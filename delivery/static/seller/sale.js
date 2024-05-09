const prices = document.getElementsByName("price");

prices.forEach(price => {
    price.innerHTML = formatPrice(price.innerHTML)
})

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}