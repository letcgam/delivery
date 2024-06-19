




const categoryBars = document.getElementsByName("bar");

categoryBars.array.forEach(bar => {
    console.log(bar)
    bar.style.width = valor + '%';
    document.getElementById("category-percent").innerHTML = valor + "%";
});

