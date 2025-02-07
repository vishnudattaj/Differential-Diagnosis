window.addEventListener("scroll",function(){
    var header = document.querySelector("nav");
    header.classList.toggle("sticky", this.window.scrollY > 0);
})