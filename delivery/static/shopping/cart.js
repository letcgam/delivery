const unitPrice = document.getElementsByName("product-price");
const quantity = document.querySelectorAll('[name^="quantity-input"]');
var totalItemPrice = document.querySelectorAll('[name^="total-price"]');
const totalCartPrice = document.getElementById("total");
const radioBtns = document.getElementsByName("seller-radio");
const purchaseBtn = document.getElementById("purchase-btn");
const evt = new Event('change');

// totalItemPrice.forEach(elem => {
//     console.log(elem.attributes.name.value);
// })

document.addEventListener('DOMContentLoaded', () => {
    unitPrice.forEach(elem => {
        elem.children[0].innerHTML = formatPrice(elem.children[1].value);
    })

    quantity.forEach(elem => {
        elem.dispatchEvent(evt);
    })

    totalCartPrice.innerHTML = formatPrice(0);
})

radioBtns.forEach(btn => {
    btn.addEventListener("input", () => {
        var name = "total-price-seller" + String(btn.value)
        totalItemPrice = document.getElementsByName(name);

        var cartPrice = 0;
        totalItemPrice.forEach(elem => {
            cartPrice += Number.parseFloat(elem.children[1].value);
        })
        totalCartPrice.innerHTML = formatPrice(cartPrice);

        purchaseBtn.disabled = false;
    })
})

quantity.forEach((elem, index) => {
    elem.addEventListener('change', () => {
        elem.value = elem.value<1 ? 1 : elem.value;
        var price = unitPrice[index].children[1].value * elem.value;
        const priceTag = totalItemPrice[index].children[0]
        priceTag.append(formatPrice(price));
        priceTag.removeChild(priceTag.firstChild);
        totalItemPrice[index].children[1].value = price;
    });
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}
