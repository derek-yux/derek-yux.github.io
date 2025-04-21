<?php
// check_auth.php
require_once 'config.php';

if (isset($_SESSION['user_id'])) {
    // Get user data including rank
    $sql = "SELECT user_id, username, points, rank FROM users WHERE user_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $_SESSION['user_id']);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        jsonResponse(true, 'User is authenticated', $user);
    } else {
        // Session exists but user not found
        unset($_SESSION['user_id']);
        jsonResponse(false, 'Authentication failed');
    }
} else {
    jsonResponse(false, 'User is not authenticated');
}
?>

<?php
// login.php - Updated to include rank in session
require_once 'config.php';

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonResponse(false, 'Invalid request method');
}

// Check if username and password are provided
if (!isset($_POST['username']) || !isset($_POST['password'])) {
    jsonResponse(false, 'Username and password are required');
}

$username = sanitize($_POST['username']);
$password = $_POST['password'];

// Check if user exists
$sql = "SELECT user_id, username, password, rank FROM users WHERE username = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    jsonResponse(false, 'Username not found');
}

$user = $result->fetch_assoc();

// Verify password
if (password_verify($password, $user['password'])) {
    // Set session
    $_SESSION['user_id'] = $user['user_id'];
    $_SESSION['username'] = $user['username'];
    $_SESSION['rank'] = $user['rank'];
    
    jsonResponse(true, 'Login successful');
} else {
    jsonResponse(false, 'Incorrect password');
}
?>

<?php
// register.php - Updated to initialize points and rank
require_once 'config.php';

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonResponse(false, 'Invalid request method');
}

// Check if username and password are provided
if (!isset($_POST['username']) || !isset($_POST['password'])) {
    jsonResponse(false, 'Username and password are required');
}

$username = sanitize($_POST['username']);
$password = $_POST['password'];

// Validate username
if (strlen($username) < 4 || strlen($username) > 30) {
    jsonResponse(false, 'Username must be between 4 and 30 characters');
}

if (!preg_match('/^[a-zA-Z0-9_]+$/', $username)) {
    jsonResponse(false, 'Username can only contain letters, numbers, and underscores');
}

// Validate password
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
$check_sql = "SELECT user_id FROM users WHERE username = ?";
$check_stmt = $conn->prepare($check_sql);
$check_stmt->bind_param("s", $username);
$check_stmt->execute();
$check_result = $check_stmt->get_result();

if ($check_result->num_rows > 0) {
    jsonResponse(false, 'Username already exists');
}

// Hash password
$hashed_password = password_hash($password, PASSWORD_DEFAULT);

// Insert new user with default points and rank
$sql = "INSERT INTO users (username, password, points, rank) VALUES (?, ?, 0, 'Newcomer')";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $username, $hashed_password);

if ($stmt->execute()) {
    // Create default profile
    $user_id = $stmt->insert_id;
    $create_profile = "INSERT INTO user_profiles (user_id) VALUES (?)";
    $profile_stmt = $conn->prepare($create_profile);
    $profile_stmt->bind_param("i", $user_id);
    $profile_stmt->execute();
    
    jsonResponse(true, 'Registration successful. You can now login.');
} else {
    jsonResponse(false, 'Registration failed: ' . $stmt->error);
}
?>