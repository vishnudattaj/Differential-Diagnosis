document.addEventListener("DOMContentLoaded", function () {
    const addCardButton = document.querySelector(".add-card-button");
    const diseaseList = document.querySelector(".disease-list");

    addCardButton.addEventListener("click", function () {

        const diseaseName = prompt("Enter the disease name:");
        const diseaseDate = prompt("Enter the date (e.g., MM/DD/YYYY):");


        if (!diseaseName || !diseaseDate) {
            alert("Both disease name and date are required!");
            return;
        }


        const newCard = document.createElement("div");
        newCard.className = "disease-card";


        const nameElement = document.createElement("h2");
        nameElement.className = "disease-name";
        nameElement.textContent = diseaseName;


        const dateElement = document.createElement("p");
        dateElement.className = "disease-date";
        dateElement.textContent = diseaseDate;


        newCard.appendChild(nameElement);
        newCard.appendChild(dateElement);


        diseaseList.appendChild(newCard);
    });
});