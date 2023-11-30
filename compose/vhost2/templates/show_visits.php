<?php
// Assuming you have a MySQL database connection
$servername = "database";
$username = "root";
$password = "root";
$dbname = "hospital_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}


// Get the doctor's name from the form
$doctorName = $_GET['doctor'];

// Fetch data from the database for the specific doctor
$sql = "SELECT *
FROM (Visit JOIN Doctor ON Visit.doctor = Doctor.id)
WHERE Doctor.last_name = '$doctorName';";
// ATTENTION: THIS IS SUBJECT TO SQL INJECTION (we need to avoid passing input parameters like this in a query)

$result = $conn->query($sql);

return $result
?>
