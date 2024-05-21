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
    var proportion = productPictures[i].clientWidth / productPictures[i].clientHeight
    productPictures[i].style.maxHeight = String(productPictures[i].clientWidth) + "px"
    productPictures[i].style.width = String(productPictures[i].clientWidth * proportion) + "px"

    console.log(proportion)
    console.log(productPictures[i].style.maxHeight)
    console.log(productPictures[i].clientWidth * proportion)
}