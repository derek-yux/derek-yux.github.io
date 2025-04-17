<?php
// add_reaction.php
require_once 'config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    jsonResponse(false, 'You must be logged in to react');
}

// Validate input
if (!isset($_POST['post_id']) || !isset($_POST['reaction_type'])) {
    jsonResponse(false, 'Post ID and reaction type are required');
}

$post_id = (int)$_POST['post_id'];
$user_id = $_SESSION['user_id'];
$reaction_type = $_POST['reaction_type'];

// Valid reaction types
$valid_reactions = ['like', 'love', 'laugh', 'wow', 'sad', 'angry'];
if (!in_array($reaction_type, $valid_reactions)) {
    jsonResponse(false, 'Invalid reaction type');
}

// Verify post exists
$check_post = "SELECT post_id FROM posts WHERE post_id = ?";
$post_stmt = $conn->prepare($check_post);
$post_stmt->bind_param("i", $post_id);
$post_stmt->execute();
$post_result = $post_stmt->get_result();

if ($post_result->num_rows === 0) {
    jsonResponse(false, 'Post not found');
}

// Check if reaction already exists
$check_sql = "SELECT * FROM reactions WHERE post_id = ? AND user_id = ? AND reaction_type = ?";
$check_stmt = $conn->prepare($check_sql);
$check_stmt->bind_param("iis", $post_id, $user_id, $reaction_type);
$check_stmt->execute();
$check_result = $check_stmt->get_result();

if ($check_result->num_rows > 0) {
    // Reaction exists, remove it (toggle)
    $delete_sql = "DELETE FROM reactions WHERE post_id = ? AND user_id = ? AND reaction_type = ?";
    $delete_stmt = $conn->prepare($delete_sql);
    $delete_stmt->bind_param("iis", $post_id, $user_id, $reaction_type);
    
    if ($delete_stmt->execute()) {
        jsonResponse(true, 'Reaction removed');
    } else {
        jsonResponse(false, 'Error removing reaction: ' . $delete_stmt->error);
    }
} else {
    // Insert new reaction
    $sql = "INSERT INTO reactions (post_id, user_id, reaction_type) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("iis", $post_id, $user_id, $reaction_type);
    
    if ($stmt->execute()) {
        // Increment user points for reacting
        $update_points = "UPDATE users SET points = points + 1 WHERE user_id = ?";
        $points_stmt = $conn->prepare($update_points);
        $points_stmt->bind_param("i", $user_id);
        $points_stmt->execute();
        
        // Update user rank based on points
        updateUserRank($user_id);
        
        jsonResponse(true, 'Reaction added successfully');
    } else {
        jsonResponse(false, 'Error adding reaction: ' . $stmt->error);
    }
}
?>