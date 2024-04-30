const product = document.getElementsByName("product");
const total = document.getElementById("total");
var orderTotal = 0;

product.forEach(element => {
    productInfo = element.children[0].children[1]
    unitPrice = productInfo.children[0]
    quant = productInfo.children[1]
    exibitPrice = productInfo.children[3]
    productTotal = element.children[1]

    productTotal.innerHTML = formatPrice(unitPrice.value * Number.parseInt(quant.innerHTML))
    exibitPrice.innerHTML = formatPrice(unitPrice.value)

    orderTotal += unitPrice.value * Number.parseInt(quant.innerHTML)
});

total.innerHTML = formatPrice(orderTotal)


function formatPrice(price) {
    return Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
    }).format(price);
}
