const product = document.getElementsByName("product");
const total = document.getElementById("total");
var orderTotal = 0;

product.forEach(element => {
    var unitPrice = element.children[1]
    var quantity = element.children[2]
    var totalPrice = element.children[3]

    unitPrice.children[0].innerHTML = formatPrice(unitPrice.children[1].value);
    totalPrice.innerHTML = formatPrice(unitPrice.children[1].value * quantity.innerHTML)
    orderTotal += (unitPrice.children[1].value * quantity.innerHTML)
});

total.innerHTML = formatPrice(orderTotal)


function formatPrice(price) {
    return Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
    }).format(price);
}
