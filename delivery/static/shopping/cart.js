const unitPrice = document.getElementsByName("product-price");
const quantity = document.querySelectorAll('[name^="quantity-input"]');
var totalItemPrice = document.querySelectorAll('[name^="total-price"]');
const totalCartPrice = document.getElementById("total");
const radioBtns = document.getElementsByName("seller-radio");
const purchaseBtn = document.getElementById("purchase-btn");
var selectedSeller = null;
const changeEvt = new Event('change');

document.addEventListener('DOMContentLoaded', () => {
    unitPrice.forEach(elem => {
        elem.children[0].innerHTML = formatPrice(elem.children[1].value);
    })

    quantity.forEach(elem => {
        elem.dispatchEvent(changeEvt);
    })

    totalCartPrice.innerHTML = formatPrice(0);
});

radioBtns.forEach(btn => {
    btn.addEventListener("input", () => {
        sellerId = btn.value
        updateTotal(sellerId)
    });
});

quantity.forEach((quant, index) => {
    quant.addEventListener('change', () => {
        quant.value = quant.value<1 ? 1 : quant.value;
        var price = unitPrice[index].children[1].value * quant.value;
        var priceTag = totalItemPrice[index].children[0];
        priceTag.innerHTML = formatPrice(price);
        
        totalItemPrice[index].children[1].value = price;

        radioBtns.forEach(btn => {
            if (btn.checked) {
                updateTotal(btn.value);
            }
        });
    });
});

function updateTotal(sellerId) {
    var name = "total-price-seller" + String(sellerId);
    sellerItemTotal = document.getElementsByName(name);

    var cartPrice = 0;
    sellerItemTotal.forEach(elem => {
        cartPrice += Number.parseFloat(elem.children[1].value);
    });
    totalCartPrice.innerHTML = formatPrice(cartPrice);

    purchaseBtn.disabled = false;
};

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
};
