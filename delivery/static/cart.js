const unitPrice = document.getElementsByName("product-price");
const quantity = document.querySelectorAll('[name^="quantity-input"]');
const totalPrice = document.getElementsByName("total-price");
const total = document.getElementById("total");
const totalValue = document.getElementById("total-input");
const evt = new Event('change');


document.addEventListener('DOMContentLoaded', () => {
    unitPrice.forEach(elem => {
        elem.children[0].innerHTML = formatPrice(elem.children[1].value);
    })

    quantity.forEach(elem => {
        elem.dispatchEvent(evt);
    })

    total.innerHTML = formatPrice(totalValue.value);
})

quantity.forEach((elem, index) => {
    elem.addEventListener('change', () => {
        elem.value = elem.value<1 ? 1 : elem.value;
        var price = unitPrice[index].children[1].value * elem.value;
        const priceTag = totalPrice[index].children[0]
        priceTag.append(formatPrice(price));
        priceTag.removeChild(priceTag.firstChild);
        totalPrice[index].children[1].value = price;

        var cartPrice = 0;
        totalPrice.forEach(elem => {
            cartPrice += Number.parseFloat(elem.children[1].value);
        })
        total.innerHTML = formatPrice(cartPrice);
        totalValue.value = cartPrice;
    })
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}
