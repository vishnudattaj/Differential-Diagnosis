const DiagnoseYourSymptoms = document.querySelector(".Front-button");

DiagnoseYourSymptoms.onclick = function() {
    scroll();
};

function scroll() {
    window.scrollTo({
        top: 1000, 
        behavior: 'smooth' 
})
}
window.addEventListener("scroll",function(){
    var header = document.querySelector("nav");
    header.classList.toggle("sticky", this.window.scrollY > 0);
})