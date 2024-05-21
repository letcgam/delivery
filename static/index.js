var indexProductsPrice = document.getElementsByName("product-price");

document.addEventListener("DOMContentLoaded", () => {
    for (i = 0; i < indexProductsPrice.length; i++) {
        indexProductsPrice[i].innerHTML = formatPrice(indexProductsPrice[i].innerHTML)
    }
});

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
};

const productPictures = document.getElementsByClassName("square");

for (i = 0; i < productPictures.length; i++) {
    console.log(productPictures[i].style)
    productPictures[i].style.maxHeight = String(productPictures[i].clientWidth) + "px"
}