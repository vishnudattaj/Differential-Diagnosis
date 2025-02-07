let availableKeywords = [
    'Itching',
    'Skin Rash',
    'Nodal Skin Eruption',
    'Continuous Sneezing',
    'Shivering',
    'Chills',
    'Stomach Pain',
    'Acidity',
    'Ulcers on Tongue',
    'Muscle Shrinkage',
    'Vomiting',
    'Burning Micturition',
    'Fatigue',
    'Weight Gain',
    'Weight Loss',
    'Anxiety',
    'Cold Hands and Feet',
    'Mood Swings',
    'Restlessness',
    'Lethargy',
    'Patches in Throat',
    'Irregular Blood Sugar',
    'Cough',
    'High Fever',
    'Breathlessness',  
    'Sweating',
    'Indigestion',
    'Headache',
    'Yellowish Skin',
    'Dark Urine',
    'Nausea',
    'Loss of Appetite',
    'Pain Behind the Eyes',
    'Back Pain',
    'Constipation',
    'Abdominal Pain',
    'Diarrhea',
    'Mild Fever',
    'Yellow Urine',
    'Yellowing of Eyes',
    'Acute Liver Failure',
    'Fluid Overload',
    'Swelling of Stomach',
    'Swollen Lymph Nodes',
    'Malaise',
    'Blurred and Distorted Vision',
    'Phlegm',
    'Throat Irritation',
    'Redness of Eyes',
    'Sinus Pressure',
    'Runny Nose',
    'Congestion',
    'Chest Pain',
    'Weakness in Limbs',
    'Fast Heart Rate',
    'Pain During Bowel Movements',
    'Pain in Anal Region',
    'Bloody Stool',
    'Irritation in Anus',
    'Neck Pain',
    'Dizziness',
    'Cramps',
    'Bruising',
    'Obesity',
    'Swollen Legs',
    'Swollen Blood Vessels',
    'Puffy Face and Eyes',
    'Enlarged Thyroid',
    'Brittle Nails',
    'Swollen Extremeties',
    'Excessive Hunger',
    'Extra Marital Contacts',
    'Drying and Tingling Lips',
    'Slurred Speech',
    'Knee Pain',
    'Hip Joint Pain',
    'Muscle Weakness',
    'Stiff Neck',
    'Swelling Joints',
    'Movement Stiffness',
    'Spinning Movements',
    'Unsteadiness',
    'Loss of Balance',
    'Loss of Smell',
    'Weakness of One Body Side',
    'Bladder Discomfort',
    'Foul Smell of Urine',
    'Continuous Feeling of Urine',
    'Passage of Gases',
    'Internal Itching',
    'Toxic Look (Typhos)',
    'Depression',
    'Irritability',
    'Muscle Pain',
    'Altered Sensorium',
    'Red Spots Over Body',
    'Belly Pain',
    'Abnormal Menstruation',
    'Dischromic Patches',
    'Watering from Eyes',
    'Increased Appetite',
    'Polyuria',
    'Mucoid Sputum',
    'Rusty Sputum',
    'Lack of Concentration',
    'Visual Disturbances',
    'Receiving Blood Transfusion',
    'Receiving Unsterile Injections',
    'Coma',
    'Stomach Bleeding',
    'Distension of Abdomen',
    'History of Alcohol Consumption',
    'Fluid Overload',
    'Blood in Sputum',
    'Prominent Veins on Calf',
    'Palpitations',
    'Painful Walking',
    'Pus Filled Pimples',
    'Blackheads',
    'Scarring',
    'Skin Peeling',
    'Silver Like Dusting',
    'Small Dents in Nails',
    'Inflamed Nails',
    'Blister',
    'Red Sore Around Nose',
    'Yellow Crust Ooze',
]


const resultsBox = document.querySelector(".result-box");
const inputBox = document.getElementById("input-box");
const addSymptom = document.getElementById("add-button");
const symptomsList = document.getElementById("listofsymptoms");
const clearButton = document.getElementById("clear-button");

inputBox.onkeyup = function() {
    let result = [];
    let input = inputBox.value;
    if (input.length) {
        result = availableKeywords.filter((keyword) => {
            return keyword.toLowerCase().includes(input.toLowerCase());
        });
        console.log(result);
    }
    display(result);
    if (!result.length) {
        resultsBox.innerHTML = '';
    }
};

function display(result) {
    const content = result.map((list) => {
        return "<li onclick=selectInput(this)>" + list + "<li>";
    });
    resultsBox.innerHTML = "<ul>" + content.join('') + "<ul>";
}

function selectInput(list) {
    inputBox.value = list.innerHTML;
    resultsBox.innerHTML = '';
}

addSymptom.onclick = function() {
    addSymptomToList();
    console.log("added");
};

inputBox.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        addSymptomToList();
    }
});

function addSymptomToList() {
    if (inputBox.value.trim() !== "") {
        let symptomToAdd = document.createElement("li");
        symptomToAdd.innerHTML = inputBox.value;
        symptomsList.appendChild(symptomToAdd);
        inputBox.value = "";
    }
}

clearButton.onclick = function() {
    symptomsList.innerHTML = "";
    console.log("cleared");
};