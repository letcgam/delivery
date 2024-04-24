const unitPrice = document.getElementsByName("product-price");
const quantity = document.getElementsByName("quantity-input");
const totalPrice = document.getElementsByName("total-price");


const evt = new Event('change');

document.addEventListener('DOMContentLoaded', () => {
    unitPrice.forEach(elem => {
        console.log(elem.children[0]);
        elem.children[0].innerHTML = formatPrice(elem.children[1].value);
    })

    quantity.forEach(elem => {
        elem.dispatchEvent(evt);
    })
})

quantity.forEach((elem, index) => {
    elem.addEventListener('change', () => {
        elem.value = elem.value<1 ? 1 : elem.value
        totalPrice[index].innerHTML = formatPrice(unitPrice[index].children[1].value * elem.value);
    })
});

function formatPrice(price) {
    return Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
    }).format(price);
}
