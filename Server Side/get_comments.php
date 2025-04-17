<?php
// get_comments.php
require_once 'config.php';

if (!isset($_GET['post_id'])) {
    jsonResponse(false, 'Post ID is required');
}

$post_id = (int)$_GET['post_id'];

// Verify post exists
$check_post = "SELECT post_id FROM posts WHERE post_id = ?";
$post_stmt = $conn->prepare($check_post);
$post_stmt->bind_param("i", $post_id);
$post_stmt->execute();
$post_result = $post_stmt->get_result();

if ($post_result->num_rows === 0) {
    jsonResponse(false, 'Post not found');
}

// Get comments for the post
$sql = "SELECT c.comment_id, c.post_id, c.user_id, c.content, c.created_at, 
        u.username, IFNULL(up.avatar, 'default.png') as avatar 
        FROM comments c 
        JOIN users u ON c.user_id = u.user_id 
        LEFT JOIN user_profiles up ON u.user_id = up.user_id
        WHERE c.post_id = ? 
        ORDER BY c.created_at ASC";

$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $post_id);
$stmt->execute();
$result = $stmt->get_result();

$comments = [];
while ($row = $result->fetch_assoc()) {
    $comments[] = $row;
}

jsonResponse(true, 'Comments retrieved successfully', ['comments' => $comments]);
?>