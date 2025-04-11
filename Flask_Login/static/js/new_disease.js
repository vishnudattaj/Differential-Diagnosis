document.addEventListener("DOMContentLoaded", function () {
    const addCardButton = document.querySelector(".add-card-button");

    addCardButton.addEventListener("click", function () {
        const diseaseName = prompt("Enter the disease name:");
        const diseaseDate = prompt("Enter the date (e.g., MM/DD/YYYY):");

        if (!diseaseName || !diseaseDate) {
            alert("Both disease name and date are required!");
            return;
        }

        // Create data to send to the server
        const diseaseData = {
            disease: diseaseName,
            date: diseaseDate
        };

        // Send the data to the server using fetch API
        fetch('/add_disease', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(diseaseData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert('Disease added successfully!');
            // Optionally refresh the page to show updated history
            window.location.href = '/disease_history';
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error adding disease. Please try again.');
        });
    });
});