const isOwner = document.getElementById("is-owner").value;
const prices = document.getElementsByName("price");
const ratingInput = document.getElementById("rating");

document.addEventListener("DOMContentLoaded", () => {
    var value = String(ratingInput.value)
    console.log(value)
    ratingInput.style.setProperty('--value', value)
})

prices.forEach(price => {
    price.innerHTML = formatPrice(price.innerHTML);
})

const categoryCarousel = new bootstrap.Carousel(
    document.getElementById("same-category-carousel"),
    {
        interval: 2000,
        touch: false
    }
);
const sellerCarousel = new bootstrap.Carousel(
    document.getElementById("same-seller-carousel"),
    {
        interval: 2000,
        touch: false
    }
);

if (isOwner == "true") {
    const inputs = Array.from(document.getElementsByClassName("input"));
    const editBtn = document.getElementById("edit-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const confirmBtn = document.getElementById("confirm-btn");
    const productImage = document.getElementById("product-image");
    const productImgLabel = document.getElementById("product-image-label");
    const productImgInput = document.getElementById("product-image-input");
    const cancelImageBtn = document.getElementById("cancel-image-btn");

    window.onload = function resizeLabel() {
        productImgLabel.style.width = `${productImage.width}px`;
        productImgLabel.style.height = `${productImage.height}px`;
    };
    window.onresize = function resizeLabel() {
        productImgLabel.style.width = `${productImage.width}px`;
        productImgLabel.style.height = `${productImage.height}px`;
    };

    cancelImageBtn.addEventListener("click", () => {
        productImgInput.value = "";
    })

    editBtn.addEventListener("click", () => {
        inputs.forEach(input => {
            input.disabled = false;
            input.classList.remove("border-dark");
        })
        editBtn.hidden = true;
        cancelBtn.hidden = false;
        confirmBtn.hidden = false;
        productImgLabel.style.zIndex = 1;
    })

    cancelBtn.addEventListener("click", () => {
        location.reload();
    })
}

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}

