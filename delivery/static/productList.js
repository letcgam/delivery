const productPictures = document.getElementsByClassName("square");

for (i = 0; i < productPictures.length; i++) {
    var heigth = productPictures[i].clientHeight
    var width = productPictures[i].clientWidth
    
    productPictures[i].style.height = String(width) + "px"
    productPictures[i].children[0].style.objectFit = "fill"
}