<?php

$symptoms = $_POST["symptoms"];
$diabetes = $_POST["diabetes"];
$hypertension = $_POST["hypertension"];
$asthma = $_POST["asthma"];
$terms = filter_input(INPUT_POST, "terms", FILTER_VALIDATE_BOOLEAN);

if ( ! $terms) {
    die("Terms must be accepted");
}

var_dump($symptoms, $diabetes, $hypertension, $asthma, $terms);