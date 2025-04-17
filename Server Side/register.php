<?php
// register.php
require_once('config.php');
// Check if the request is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonResponse(false, 'Invalid request method');
}

// Get input data
$username = isset($_POST['username']) ? sanitize($_POST['username']) : '';
$password = isset($_POST['password']) ? $_POST['password'] : '';

// Validate input
if (empty($username)) {
    jsonResponse(false, 'Username is required');
}

if (empty($password)) {
    jsonResponse(false, 'Password is required');
}

// Username validation
if (strlen($username) < 4) {
    jsonResponse(false, 'Username must be at least 4 characters long');
}

if (strlen($username) > 30) {
    jsonResponse(false, 'Username cannot exceed 30 characters');
}

if (!preg_match('/^[a-zA-Z0-9_]+$/', $username)) {
    jsonResponse(false, 'Username can only contain letters, numbers, and underscores');
}

// Password validation
if (strlen($password) < 8) {
    jsonResponse(false, 'Password must be at least 8 characters long');
}

if (!preg_match('/[A-Z]/', $password)) {
    jsonResponse(false, 'Password must contain at least one uppercase letter');
}

if (!preg_match('/[a-z]/', $password)) {
    jsonResponse(false, 'Password must contain at least one lowercase letter');
}

if (!preg_match('/[0-9]/', $password)) {
    jsonResponse(false, 'Password must contain at least one number');
}

// Check if username already exists
$check_stmt = $conn->prepare("SELECT user_id FROM users WHERE username = ?");
$check_stmt->bind_param("s", $username);
$check_stmt->execute();
$result = $check_stmt->get_result();

if ($result->num_rows > 0) {
    jsonResponse(false, 'Username already exists. Please choose a different username.');
}
$check_stmt->close();

// Hash the password
$hashed_password = password_hash($password, PASSWORD_DEFAULT);

// Insert new user
$insert_stmt = $conn->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
$insert_stmt->bind_param("ss", $username, $hashed_password);

if ($insert_stmt->execute()) {
    jsonResponse(true, 'Registration successful! You can now log in with your credentials.');
} else {
    jsonResponse(false, 'Registration failed: ' . $conn->error);
}

$insert_stmt->close();
$conn->close();
?>