<?php
// get_posts.php
require_once 'config.php';

// Get optional timestamp parameter for real-time updates
$last_timestamp = isset($_GET['last_timestamp']) ? sanitize($_GET['last_timestamp']) : 0;

// Prepare SQL query to get posts
$sql = "
    SELECT p.post_id, p.title, p.content, p.created_at, 
           u.username, UNIX_TIMESTAMP(p.created_at) as timestamp
    FROM posts p 
    JOIN users u ON p.user_id = u.user_id 
";

// If last_timestamp is provided, only get newer posts
if ($last_timestamp > 0) {
    $sql .= " WHERE UNIX_TIMESTAMP(p.created_at) > ? ";
}

// Order by newest first
$sql .= " ORDER BY p.created_at DESC ";

// Limit to prevent overloading (optional)
$sql .= " LIMIT 50";

$stmt = $conn->prepare($sql);

// Bind parameters if needed
if ($last_timestamp > 0) {
    $stmt->bind_param("i", $last_timestamp);
}

$stmt->execute();
$result = $stmt->get_result();

$posts = [];
while ($row = $result->fetch_assoc()) {
    $posts[] = $row;
}

jsonResponse(true, 'Posts retrieved successfully', [
    'posts' => $posts,
    'count' => count($posts)
]);

$stmt->close();
$conn->close();
?>