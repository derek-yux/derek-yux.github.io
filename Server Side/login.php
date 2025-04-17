<?php
// login.php
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

// Check if user exists
$stmt = $conn->prepare("SELECT user_id, username, password FROM users WHERE username = ?");
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    jsonResponse(false, 'Username does not exist. Please check your spelling or register a new account.');
}

$user = $result->fetch_assoc();
$stmt->close();

// Verify password
if (!password_verify($password, $user['password'])) {
    jsonResponse(false, 'Incorrect password. Please try again.');
}

// Set session variables
$_SESSION['logged_in'] = true;
$_SESSION['user_id'] = $user['user_id'];
$_SESSION['username'] = $user['username'];

jsonResponse(true, 'Login successful! Welcome back, ' . $user['username'] . '!', [
    'user_id' => $user['user_id'],
    'username' => $user['username']
]);

$conn->close();
?>