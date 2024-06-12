const productPictures = Array.from(document.getElementsByClassName("square"));

productPictures.forEach(image => {
    var width = image.clientWidth;

    image.style.height = String(width) + "px";
    image.children[0].style.objectFit = "fill";
});