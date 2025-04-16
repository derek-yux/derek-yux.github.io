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

$post_id = (int)$_POST['post_id'];
$user_id = $_SESSION['user_id'];
$content = sanitize($_POST['content']);

// Insert the comment
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

<?php
// get_comments.php
require_once 'config.php';

if (!isset($_GET['post_id'])) {
    jsonResponse(false, 'Post ID is required');
}

$post_id = (int)$_GET['post_id'];

// Get comments for the post
$sql = "SELECT c.*, u.username, up.avatar FROM comments c 
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
$reaction_type = sanitize($_POST['reaction_type']);

// Valid reaction types
$valid_reactions = ['like', 'love', 'laugh', 'wow', 'sad', 'angry'];
if (!in_array($reaction_type, $valid_reactions)) {
    jsonResponse(false, 'Invalid reaction type');
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

<?php
// get_reactions.php
require_once 'config.php';

if (!isset($_GET['post_id'])) {
    jsonResponse(false, 'Post ID is required');
}

$post_id = (int)$_GET['post_id'];
$user_id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : null;

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