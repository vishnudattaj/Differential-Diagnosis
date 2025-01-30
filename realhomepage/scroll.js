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