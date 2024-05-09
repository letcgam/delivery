const categoryFilter = document.getElementById("category");
const products = Array.from(document.getElementsByName("product"));
const productsCategory = document.getElementsByName("product-category");
var searchInput = document.getElementById("seller-search")

categoryFilter.addEventListener("change", () => {
    productsCategory.forEach(category => {
        if (category.value != categoryFilter.value) {
            category.parentElement.classList.add("d-none");
        } else {
            category.parentElement.classList.remove("d-none");
        }
    })
})

searchInput.addEventListener("input", () => {
    search = searchInput.value.toLowerCase();

    products.forEach(product => {
        var productName = product.querySelectorAll(".product-name")[0].innerHTML.toLowerCase();
        if (search == "") {
            product.classList.remove("d-none");
        } else if (productName.includes(search)) {
            product.classList.remove("d-none");
            console.log(productName)
        } else {
            product.classList.add("d-none");
        }
    })
});