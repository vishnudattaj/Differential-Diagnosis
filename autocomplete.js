let availableKeywords = [
    'Fever',
    'Chills',
    'Fatigue',
    'Weight Loss',
    'Weight Gain',
    'Sweating (Night Sweats)',
    'Loss of appetite',
    'Dehydration',
    'Swollen lymph nodes',
    'Dry Cough',
    'Productive Cough',
    'Shortness of Breath',
    'Chest Pain',
    'Runny Nose',
    'Sore Throat',
    'Nasal Congestion',
    'Sneezing',
    'Nausea',
    'Vomiting',
    'Diarrhea',
    'Constipation',
    'Abdominal Pain',
    'Heartburn',
    'Blood in stool',
    'Headache',
    'Dizziness',
    'Numbness',
    'Memory Loss',
    'Seizures',
    'Muscular Weakness',
    'Joint Pain',
    'Back Pain',
    'Stiffness',
    'Swelling',
    'Inflamation',
    'Rash',
    'Itching',
    'Bruising',
    'Hives',
    'Hair Loss',

];

const resultsBox = document.querySelector(".result-box");
const inputBox = document.getElementById("input-box");
inputBox.onkeyup = function(){
    let result = [];
    let input = inputBox.value;
    if(input.length){
        result = availableKeywords.filter((keyword)=>{
           return keyword.toLowerCase().includes(input.toLowerCase());
        });
        console.log(result);

    }
    display(result);
    if(!result.length){
        resultBox.innerHTML = '';
    }
}
function display(result){
    const content = result.map((list)=>{
        return "<li onclick=selectInput(this)>" + list + "<li>";
    });
    resultsBox.innerHTML = "<ul>" + content.join('') + "<ul>";
}
function selectInput(list){
    inputBox.value = list.innerHTML;
    resultsBox.innerHTML = '';
}