<?php
// add_comment.php
require_once 'config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    jsonResponse(false, 'You must be logged in to comment');
}

// Validate input
if (!isset($_POST['post_id']) || !isset($_POST['content']) || empty($_POST['content'])) {
    jsonResponse(false, 'Post ID and content are required');
}

// Get and sanitize input
$post_id = (int)$_POST['post_id'];
$user_id = $_SESSION['user_id'];
$content = $_POST['content']; // Don't sanitize here to preserve emojis

// Verify post exists
$check_post = "SELECT post_id FROM posts WHERE post_id = ?";
$post_stmt = $conn->prepare($check_post);
$post_stmt->bind_param("i", $post_id);
$post_stmt->execute();
$post_result = $post_stmt->get_result();

if ($post_result->num_rows === 0) {
    jsonResponse(false, 'Post not found');
}

// Insert the comment - use prepared statements for security
$sql = "INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("iis", $post_id, $user_id, $content);

if ($stmt->execute()) {
    // Increment user points for commenting
    $update_points = "UPDATE users SET points = points + 2 WHERE user_id = ?";
    $points_stmt = $conn->prepare($update_points);
    $points_stmt->bind_param("i", $user_id);
    $points_stmt->execute();
    
    // Update user rank based on points
    updateUserRank($user_id);
    
    // Get the created comment with username
    $comment_id = $stmt->insert_id;
    $query = "SELECT c.*, u.username FROM comments c 
              JOIN users u ON c.user_id = u.user_id 
              WHERE c.comment_id = ?";
    $comment_stmt = $conn->prepare($query);
    $comment_stmt->bind_param("i", $comment_id);
    $comment_stmt->execute();
    $result = $comment_stmt->get_result();
    
    if ($result->num_rows > 0) {
        $comment = $result->fetch_assoc();
        jsonResponse(true, 'Comment added successfully', ['comment' => $comment]);
    } else {
        jsonResponse(true, 'Comment added successfully');
    }
} else {
    jsonResponse(false, 'Error adding comment: ' . $stmt->error);
}
?>