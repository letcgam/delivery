const isOwner = document.getElementById("is-owner");

if (isOwner) {
    const inputs = Array.from(document.getElementsByClassName("input"));
    const editBtn = document.getElementById("edit-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const confirmBtn = document.getElementById("confirm-btn");

    editBtn.addEventListener("click", () => {
        inputs.forEach(input => {
            input.disabled = false;
            input.classList.remove("border-secondary");
        })
        editBtn.hidden = true;
        cancelBtn.hidden = false;
        confirmBtn.hidden = false;
    })

    cancelBtn.addEventListener("click", () => {
        location.reload();
    })

} else {
    var totalPrice = document.getElementById("total-price");
    var quantityInput = document.getElementById("quantity-input");
    var productPrice = document.getElementById("product-price");
    const productUnitPrice = document.getElementById("product-unit-price");

    quantityInput.addEventListener("change", () => {
        price = quantityInput.value * productUnitPrice.innerHTML;
        totalPrice.innerHTML = formatPrice(price);
    });


    document.addEventListener("DOMContentLoaded", () => {
        productPrice.innerHTML = formatPrice(productUnitPrice.innerHTML);
        totalPrice.innerHTML = productPrice.innerHTML
    });
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