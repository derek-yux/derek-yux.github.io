<?php
// update_profile.php
require_once 'config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    jsonResponse(false, 'You must be logged in to update your profile');
}

$user_id = $_SESSION['user_id'];
$display_name = isset($_POST['display_name']) ? sanitize($_POST['display_name']) : null;
$bio = isset($_POST['bio']) ? sanitize($_POST['bio']) : null;

// Validate input
if ($display_name && (strlen($display_name) < 3 || strlen($display_name) > 50)) {
    jsonResponse(false, 'Display name must be between 3 and 50 characters');
}

if ($bio && strlen($bio) > 500) {
    jsonResponse(false, 'Bio cannot exceed 500 characters');
}

// Initialize update success flag
$update_success = false;

// Check if profile exists
$check_sql = "SELECT * FROM user_profiles WHERE user_id = ?";
$check_stmt = $conn->prepare($check_sql);
$check_stmt->bind_param("i", $user_id);
$check_stmt->execute();
$check_result = $check_stmt->get_result();

if ($check_result->num_rows > 0) {
    // Update existing profile
    $sql = "UPDATE user_profiles SET display_name = ?, bio = ? WHERE user_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssi", $display_name, $bio, $user_id);
} else {
    // Create new profile
    $sql = "INSERT INTO user_profiles (user_id, display_name, bio) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("iss", $user_id, $display_name, $bio);
}

// Execute the profile update/insert
$update_success = $stmt->execute();

// If profile update failed, report error
if (!$update_success) {
    jsonResponse(false, 'Error updating profile: ' . $stmt->error);
}

// Handle avatar upload if provided
$avatar_path = null;
if (isset($_FILES['avatar']) && $_FILES['avatar']['error'] == 0) {
    $allowed = ['jpg', 'jpeg', 'png', 'gif'];
    $filename = $_FILES['avatar']['name'];
    $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    
    if (in_array($ext, $allowed)) {
        $upload_path = 'uploads/avatars/';
        
        // Create directory if it doesn't exist
        if (!file_exists($upload_path)) {
            mkdir($upload_path, 0777, true);
        }
        
        $new_filename = uniqid() . '.' . $ext;
        $destination = $upload_path . $new_filename;
        
        if (move_uploaded_file($_FILES['avatar']['tmp_name'], $destination)) {
            $avatar_path = $new_filename;
            
            // Update avatar in database
            $avatar_sql = "UPDATE user_profiles SET avatar = ? WHERE user_id = ?";
            $avatar_stmt = $conn->prepare($avatar_sql);
            $avatar_stmt->bind_param("si", $avatar_path, $user_id);
            
            // Execute the avatar update
            if (!$avatar_stmt->execute()) {
                jsonResponse(false, 'Error updating avatar: ' . $avatar_stmt->error);
            }
        } else {
            jsonResponse(false, 'Failed to upload avatar');
        }
    } else {
        jsonResponse(false, 'Invalid file type. Only JPG, PNG, and GIF are allowed');
    }
}

// If we got here, everything was successful
jsonResponse(true, 'Profile updated successfully');
?>