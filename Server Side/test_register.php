<?php
// Database config
$db_host = 'localhost';
$db_user = 'yyn'; // Change this to your actual DB username
$db_pass = 'zapyyn20062006mac'; // Change this to your actual DB password
$db_name = 'forum_db'; // Change this if you used a different database name

// Create connection
$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Test a simple insert
$username = 'testuser' . time(); // Make unique
$password = password_hash('TestPassword123', PASSWORD_DEFAULT);

$stmt = $conn->prepare("INSERT INTO users (username, password) VALUES (?, ?)");

if (!$stmt) {
    die("Prepare failed: " . $conn->error);
}

$stmt->bind_param("ss", $username, $password);

if ($stmt->execute()) {
    echo "Test user created successfully";
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>