<?php
// get_reactions.php
require_once 'config.php';

if (!isset($_GET['post_id'])) {
    jsonResponse(false, 'Post ID is required');
}

$post_id = (int)$_GET['post_id'];
$user_id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : null;

// Verify post exists
$check_post = "SELECT post_id FROM posts WHERE post_id = ?";
$post_stmt = $conn->prepare($check_post);
$post_stmt->bind_param("i", $post_id);
$post_stmt->execute();
$post_result = $post_stmt->get_result();

if ($post_result->num_rows === 0) {
    jsonResponse(false, 'Post not found');
}

// Get reaction counts for the post
$sql = "SELECT reaction_type, COUNT(*) as count FROM reactions 
        WHERE post_id = ? GROUP BY reaction_type";

$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $post_id);
$stmt->execute();
$result = $stmt->get_result();

$reactions = [];
while ($row = $result->fetch_assoc()) {
    $reactions[$row['reaction_type']] = (int)$row['count'];
}

// Get user's reactions if logged in
$user_reactions = [];
if ($user_id) {
    $user_sql = "SELECT reaction_type FROM reactions 
                WHERE post_id = ? AND user_id = ?";
    $user_stmt = $conn->prepare($user_sql);
    $user_stmt->bind_param("ii", $post_id, $user_id);
    $user_stmt->execute();
    $user_result = $user_stmt->get_result();
    
    while ($row = $user_result->fetch_assoc()) {
        $user_reactions[] = $row['reaction_type'];
    }
}

jsonResponse(true, 'Reactions retrieved successfully', [
    'reactions' => $reactions,
    'user_reactions' => $user_reactions
]);
?>