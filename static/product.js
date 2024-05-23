const isOwner = document.getElementById("is-owner").value;
console.log(isOwner);

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
} else {
    try {
        var totalPrice = document.getElementById("total-price");
        var quantityInput = document.getElementById("quantity-input");
        var productPrice = document.getElementById("product-price");
        const productUnitPrice = document.getElementById("product-unit-price");

        quantityInput.addEventListener("change", () => {
            price = quantityInput.value * productUnitPrice.innerHTML;
            totalPrice.innerHTML = formatPrice(price);
        });
        
        productPrice.innerHTML = formatPrice(productUnitPrice.innerHTML);
        totalPrice.innerHTML = productPrice.innerHTML
    } catch {

    }
}

function formatTotalPrice() {
    price = quantityInput.value * productPrice.innerHTML;
    totalPrice.innerHTML = formatPrice(price);
}

function formatPrice(price) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(price);
}