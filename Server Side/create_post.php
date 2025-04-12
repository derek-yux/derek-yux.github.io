<?php
// create_post.php
require_once 'config.php';

// Check if the request is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonResponse(false, 'Invalid request method');
}

// Check if user is logged in
if (!isset($_SESSION['logged_in']) || !$_SESSION['logged_in']) {
    jsonResponse(false, 'You must be logged in to create a post');
}

// Get input data
$title = isset($_POST['title']) ? sanitize($_POST['title']) : '';
$content = isset($_POST['content']) ? sanitize($_POST['content']) : '';
$user_id = $_SESSION['user_id'];

// Validate input
if (empty($title) || empty($content)) {
    jsonResponse(false, 'Title and content are required');
}

// Insert new post
$stmt = $conn->prepare("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)");
$stmt->bind_param("iss", $user_id, $title, $content);

if ($stmt->execute()) {
    $post_id = $conn->insert_id;
    
    // Get the newly created post with username
    $post_query = $conn->prepare("
        SELECT p.post_id, p.title, p.content, p.created_at, u.username
        FROM posts p 
        JOIN users u ON p.user_id = u.user_id 
        WHERE p.post_id = ?
    ");
    $post_query->bind_param("i", $post_id);
    $post_query->execute();
    $post_result = $post_query->get_result();
    $post = $post_result->fetch_assoc();
    
    jsonResponse(true, 'Post created successfully', $post);
} else {
    jsonResponse(false, 'Failed to create post: ' . $conn->error);
}

$stmt->close();
$conn->close();
?>