<?php
// get_posts.php - Updated to include user ranks
require_once 'config.php';

// Check if last_timestamp parameter is provided
$last_timestamp = isset($_GET['last_timestamp']) ? (int)$_GET['last_timestamp'] : 0;

if ($last_timestamp > 0) {
    // Only count newer posts
    $count_sql = "SELECT COUNT(*) as count FROM posts WHERE UNIX_TIMESTAMP(created_at) > ?";
    $count_stmt = $conn->prepare($count_sql);
    $count_stmt->bind_param("i", $last_timestamp);
    $count_stmt->execute();
    $count_result = $count_stmt->get_result();
    $count_row = $count_result->fetch_assoc();
    
    jsonResponse(true, 'Posts count retrieved', ['count' => $count_row['count']]);
    return;
}

// Get all posts with user information and rank
$sql = "SELECT p.*, u.username, u.rank, UNIX_TIMESTAMP(p.created_at) as timestamp 
        FROM posts p 
        JOIN users u ON p.user_id = u.user_id 
        ORDER BY p.created_at DESC";

$stmt = $conn->prepare($sql);
$stmt->execute();
$result = $stmt->get_result();

$posts = [];
while ($row = $result->fetch_assoc()) {
    $posts[] = $row;
}

jsonResponse(true, 'Posts retrieved successfully', ['posts' => $posts]);
?>

<?php
// create_post.php - Updated to increment points and update rank
require_once 'config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    jsonResponse(false, 'You must be logged in to create a post');
}

// Validate input
if (!isset($_POST['title']) || !isset($_POST['content'])) {
    jsonResponse(false, 'Title and content are required');
}

$title = sanitize($_POST['title']);
$content = sanitize($_POST['content']);
$user_id = $_SESSION['user_id'];

// Validate content length
if (strlen($title) < 3 || strlen($title) > 100) {
    jsonResponse(false, 'Title must be between 3 and 100 characters');
}

if (strlen($content) < 10) {
    jsonResponse(false, 'Content must be at least 10 characters long');
}

// Insert the post
$sql = "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("iss", $user_id, $title, $content);

if ($stmt->execute()) {
    // Increment user points for posting
    $update_points = "UPDATE users SET points = points + 5 WHERE user_id = ?";
    $points_stmt = $conn->prepare($update_points);
    $points_stmt->bind_param("i", $user_id);
    $points_stmt->execute();
    
    // Update user rank based on points
    updateUserRank($user_id);
    
    jsonResponse(true, 'Post created successfully');
} else {
    jsonResponse(false, 'Error creating post: ' . $stmt->error);
}
?>