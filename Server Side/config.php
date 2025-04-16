<?php
// config.php - Database configuration
$db_host = 'localhost';
$db_user = 'yyn';
$db_pass = 'zapyyn20062006mac';
$db_name = 'forum_db';

// Create connection
$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Start session
session_start();
// Set character set to UTF-8mb4 for emoji support
$conn->set_charset("utf8mb4");
// Helper functions
function sanitize($data) {
    global $conn;
    return $conn->real_escape_string(htmlspecialchars(trim($data)));
}

function jsonResponse($success, $message, $data = null) {
    $response = [
        'success' => $success,
        'message' => $message
    ];
    
    if ($data !== null) {
        $response['data'] = $data;
    }
    
    header('Content-Type: application/json');
    echo json_encode($response);
    exit;
}

function updateUserRank($user_id) {
    global $conn;
    
    // Get current points
    $points_query = "SELECT points FROM users WHERE user_id = ?";
    $stmt = $conn->prepare($points_query);
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        $points = $user['points'];
        
        // Determine rank based on points
        $rank = 'Newcomer';
        if ($points >= 500) {
            $rank = 'Forum Legend';
        } else if ($points >= 200) {
            $rank = 'Discussion Master';
        } else if ($points >= 100) {
            $rank = 'Forum Expert';
        } else if ($points >= 50) {
            $rank = 'Active Member';
        } else if ($points >= 20) {
            $rank = 'Regular';
        }
        
        // Update user rank
        $update_rank = "UPDATE users SET rank = ? WHERE user_id = ?";
        $rank_stmt = $conn->prepare($update_rank);
        $rank_stmt->bind_param("si", $rank, $user_id);
        $rank_stmt->execute();
    }
}
?>