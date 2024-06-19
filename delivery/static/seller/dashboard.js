const categoryBars = document.getElementsByName("bar");

categoryBars.forEach(bar => {
    console.log(bar.parentNode)
    var valor = bar.nextElementSibling.value;
    bar.style.width = String(valor) + '%';
    console.log(bar.style.width)
    // document.getElementById("category-percent").innerHTML = valor + "%";
});

