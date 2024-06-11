const productsList = document.getElementById("product-list");
const products = Array.from(document.getElementsByName("product"));
const sortInput = document.getElementById("sort-by");
const minPriceInput = document.getElementById("min-price");
const maxPriceInput = document.getElementById("max-price");
var price = 0;

sortInput.addEventListener("change", () => {
    sortByPrice(sortInput.value);
});

minPriceInput.addEventListener("input", () => {
    filterPrice();
});

maxPriceInput.addEventListener("input", () => {
    filterPrice();
});

function sortByPrice(option) {
    var ul = [];
    var item = {};

    products.forEach(product => {
        item = {
            product: product.parentNode,
            price: product.nextElementSibling.value
        };
        ul.push(item);
    })

    ul.sort(function(a, b) {
        return a.price - b.price;
    });

    if (option == "high") {
        ul.reverse()
    }

    ul.forEach(item => {
        productsList.appendChild(item.product)
    });
}

function filterPrice() {
    products.forEach(product => {
        price = product.nextElementSibling.value;
    
        if (price > Number.parseFloat(maxPriceInput.value) || price < Number.parseFloat(minPriceInput.value)) {
            product.parentElement.style.display = "none";
        } else {
            product.parentElement.style.display = "inline";
        };
    });
};