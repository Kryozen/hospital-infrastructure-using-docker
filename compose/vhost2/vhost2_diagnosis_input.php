<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css?family=Karla:700 subset=latin,latin-ext,cyrillic" rel="stylesheet">
<link rel="stylesheet" href="../styles.css">
<title>Додавання даних</title>
</head>

<body>
<?php
// Assuming you have a MySQL database connection
$servername = "database.localhost:3306";
$username = "admin";
$password = "admin";
$dbname = "hospital_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get form data
$surname = $_POST['surname'];
$diagnosis = $_POST['diagnosis'];
$appointmentDate = $_POST['appointmentDate'];

// Insert data into MySQL database
$sql = "INSERT INTO medical_records (surname, diagnosis, appointment_date) VALUES ('$surname', '$diagnosis', '$appointmentDate')";

if ($conn->query($sql) === TRUE) {
    echo "Record added successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

// Close the connection
$conn->close();
?>
<a type="button" id="back" href='vhost2_main.html'><button>Main page</button></a>
</body>
</html>