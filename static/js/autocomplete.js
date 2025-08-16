let availableKeywords = [
    "Itching",
    "Skin Rash",
    "Nodal Skin Eruptions",
    "Continuous Sneezing",
    "Shivering",
    "Chills",
    "Joint Pain",
    "Stomach Pain",
    "Acidity",
    "Ulcers On Tongue",
    "Muscle Wasting",
    "Vomiting",
    "Burning Micturition",
    "Spotting Urination",
    "Fatigue",
    "Weight Gain",
    "Anxiety",
    "Cold Hands And Feets",
    "Mood Swings",
    "Weight Loss",
    "Restlessness",
    "Lethargy",
    "Patches In Throat",
    "Irregular Sugar Level",
    "Cough",
    "High Fever",
    "Sunken Eyes",
    "Breathlessness",
    "Sweating",
    "Dehydration",
    "Indigestion",
    "Headache",
    "Yellowish Skin",
    "Dark Urine",
    "Nausea",
    "Loss Of Appetite",
    "Pain Behind The Eyes",
    "Back Pain",
    "Constipation",
    "Abdominal Pain",
    "Diarrhoea",
    "Mild Fever",
    "Yellow Urine",
    "Yellowing Of Eyes",
    "Acute Liver Failure",
    "Fluid Overload",
    "Swelling Of Stomach",
    "Swelled Lymph Nodes",
    "Malaise",
    "Blurred And Distorted Vision",
    "Phlegm",
    "Throat Irritation",
    "Redness Of Eyes",
    "Sinus Pressure",
    "Runny Nose",
    "Congestion",
    "Chest Pain",
    "Weakness In Limbs",
    "Fast Heart Rate",
    "Pain During Bowel Movements",
    "Pain In Anal Region",
    "Bloody Stool",
    "Irritation In Anus",
    "Neck Pain",
    "Dizziness",
    "Cramps",
    "Bruising",
    "Obesity",
    "Swollen Legs",
    "Swollen Blood Vessels",
    "Puffy Face And Eyes",
    "Enlarged Thyroid",
    "Brittle Nails",
    "Swollen Extremities",
    "Excessive Hunger",
    "Extra Marital Contacts",
    "Drying And Tingling Lips",
    "Slurred Speech",
    "Knee Pain",
    "Hip Joint Pain",
    "Muscle Weakness",
    "Stiff Neck",
    "Swelling Joints",
    "Movement Stiffness",
    "Spinning Movements",
    "Loss Of Balance",
    "Unsteadiness",
    "Weakness Of One Body Side",
    "Loss Of Smell",
    "Bladder Discomfort",
    "Foul Smell Of Urine",
    "Continuous Feel Of Urine",
    "Passage Of Gases",
    "Internal Itching",
    "Toxic Look (Typhos)",
    "Depression",
    "Irritability",
    "Muscle Pain",
    "Altered Sensorium",
    "Red Spots Over Body",
    "Belly Pain",
    "Abnormal Menstruation",
    "Dischromic Patches",
    "Watering From Eyes",
    "Increased Appetite",
    "Polyuria",
    "Family History",
    "Mucoid Sputum",
    "Rusty Sputum",
    "Lack Of Concentration",
    "Visual Disturbances",
    "Receiving Blood Transfusion",
    "Receiving Unsterile Injections",
    "Coma",
    "Stomach Bleeding",
    "Distention Of Abdomen",
    "History Of Alcohol Consumption",
    "Fluid Overload",
    "Blood In Sputum",
    "Prominent Veins On Calf",
    "Palpitations",
    "Painful Walking",
    "Pus Filled Pimples",
    "Blackheads",
    "Scurring",
    "Skin Peeling",
    "Silver Like Dusting",
    "Small Dents In Nails",
    "Inflammatory Nails",
    "Blister",
    "Red Sore Around Nose",
    "Yellow Crust Ooze"
]

const resultsBox = document.querySelector(".result-box");
const inputBox = document.getElementById("input-box");
const addSymptom = document.getElementById("add-button");
const symptomsList = document.getElementById("listofsymptoms");
const searchButton = document.getElementById("search-button");

// Disable the search button initially
searchButton.disabled = true;

// Update symptoms list on input
inputBox.onkeyup = function() {
    let result = [];
    let input = inputBox.value;
    if (input.length) {
        result = availableKeywords.filter((keyword) => {
            return keyword.toLowerCase().includes(input.toLowerCase());
        });
    }
    display(result);
    if (!result.length) {
        resultsBox.innerHTML = '';
    }
};

// Display matched symptoms
function display(result) {
    const content = result.map((list) => {
        return "<li onclick=selectInput(this)>" + list + "</li>";
    });
    resultsBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

// Select symptom from result list
function selectInput(list) {
    inputBox.value = list.innerHTML;
    resultsBox.innerHTML = '';
}

// Add symptom to the list
addSymptom.onclick = function() {
    addSymptomToList();
};

// Add symptom when Enter is pressed
inputBox.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        addSymptomToList();
    }
});

// Add symptom to the list and create hidden input
function addSymptomToList() {
    if (inputBox.value.trim() !== "") {
        let symptomToAdd = document.createElement("li");
        symptomToAdd.innerHTML = inputBox.value;
        symptomsList.appendChild(symptomToAdd);
        
        // Create and append a hidden input for this symptom
        createHiddenInput(inputBox.value);
        
        inputBox.value = ""; // Clear the input box
        updateSearchButtonState(); // Update the state of the search button
    }
}

// Function to create a hidden input for the symptom
function createHiddenInput(symptom) {
    // Generate a unique name for each hidden input (using the number of existing inputs)
    const hiddenInputs = document.querySelectorAll('[type="hidden"]');
    const hiddenInputName = `symptom${hiddenInputs.length + 1}`;
    
    // Create a new hidden input element
    let newHiddenInput = document.createElement('input');
    newHiddenInput.type = 'hidden';
    newHiddenInput.name = hiddenInputName;
    newHiddenInput.value = symptom;
    
    // Append the hidden input to the form
    document.querySelector('form').appendChild(newHiddenInput);
}

// Clear symptoms list
document.getElementById("clear-button").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the form from submitting
    clearSymptoms(); // Call your custom clear function
});

function clearSymptoms() {
    // Clear the list of symptoms
    const symptomsList = document.getElementById("listofsymptoms");
    symptomsList.innerHTML = ""; // Clear all symptoms from the list

    // Optionally, clear any hidden inputs or other form data
    const hiddenInputs = document.querySelectorAll('[type="hidden"]');
    hiddenInputs.forEach(input => input.remove());

    // Update the state of the search button
    updateSearchButtonState();
}

// Update the state of the search button
function updateSearchButtonState() {
    const hiddenInputs = document.querySelectorAll('[type="hidden"]');
    searchButton.disabled = hiddenInputs.length < 3;
}

// Submit the form (handled by the browser's default form submission)
searchButton.onclick = async function(event) {

    // Get the list of symptoms
    const symptoms = [];
    const hiddenInputs = document.querySelectorAll('[type="hidden"]');
    hiddenInputs.forEach(input => symptoms.push(input.value));

    if (symptoms.length < 3) {
        alert("Please add at least 3 symptoms before searching.");
        return;
    }
};

// Function to display results dynamically
function displayResults(predictedDisease) {
    const resultsContainer = document.querySelector(".results-container");
    const diseaseImage = document.getElementById("disease-image");

    // Clear previous results
    resultsContainer.innerHTML = "";

    if (!predictedDisease) {
        resultsContainer.innerHTML = "<p>No disease prediction available.</p>";
        diseaseImage.style.display = "none"; // Hide the image
        return;
    }

    // Display the predicted disease
    const diseaseText = document.createElement("p");
    diseaseText.style.fontSize = "45px";
    diseaseText.innerHTML = `<strong>Most Likely Disease:</strong> ${predictedDisease}`;
    resultsContainer.appendChild(diseaseText);

    // Show the image
    diseaseImage.style.display = "block";
}
