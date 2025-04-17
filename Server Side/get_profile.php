<?php
// get_profile.php
require_once 'config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    jsonResponse(false, 'You must be logged in to view your profile');
}

$user_id = $_SESSION['user_id'];

// Get user data
$user_sql = "SELECT username, points, rank FROM users WHERE user_id = ?";
$user_stmt = $conn->prepare($user_sql);
$user_stmt->bind_param("i", $user_id);
$user_stmt->execute();
$user_result = $user_stmt->get_result();

if ($user_result->num_rows === 0) {
    jsonResponse(false, 'User not found');
}

$user_data = $user_result->fetch_assoc();

// Get profile data
$profile_sql = "SELECT display_name, bio, avatar FROM user_profiles WHERE user_id = ?";
$profile_stmt = $conn->prepare($profile_sql);
$profile_stmt->bind_param("i", $user_id);
$profile_stmt->execute();
$profile_result = $profile_stmt->get_result();

$profile_data = [];
if ($profile_result->num_rows > 0) {
    $profile_data = $profile_result->fetch_assoc();
}

// Count posts
$posts_sql = "SELECT COUNT(*) as post_count FROM posts WHERE user_id = ?";
$posts_stmt = $conn->prepare($posts_sql);
$posts_stmt->bind_param("i", $user_id);
$posts_stmt->execute();
$posts_result = $posts_stmt->get_result();
$post_count = $posts_result->fetch_assoc()['post_count'];

// Count comments
$comments_sql = "SELECT COUNT(*) as comment_count FROM comments WHERE user_id = ?";
$comments_stmt = $conn->prepare($comments_sql);
$comments_stmt->bind_param("i", $user_id);
$comments_stmt->execute();
$comments_result = $comments_stmt->get_result();
$comment_count = $comments_result->fetch_assoc()['comment_count'];

// Combine all data
$profile = array_merge(
    $user_data,
    $profile_data,
    [
        'post_count' => $post_count,
        'comment_count' => $comment_count
    ]
);

// Send response
jsonResponse(true, 'Profile loaded successfully', ['profile' => $profile]);

// Helper function for JSON responses if not already defined in config.php
if (!function_exists('jsonResponse')) {
    function jsonResponse($success, $message, $data = []) {
        header('Content-Type: application/json');
        echo json_encode([
            'success' => $success,
            'message' => $message,
            'data' => $data
        ]);
        exit;
    }
}
?>