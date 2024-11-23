<?php
$input = file_get_contents('php://stdin');
parse_str($input, $_POST);
$symptoms = $_POST["symptoms"] ?? null;
$diabetes = $_POST["diabetes"] ?? null;
$hypertension = $_POST["hypertension"] ?? null;
$asthma = $_POST["asthma"] ?? null;


$array = ['symptoms' => $symptoms, 'diabetes' => $diabetes, 'hypertension' => $hypertension, 'asthma' => $asthma];
var_dump($array);