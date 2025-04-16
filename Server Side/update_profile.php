<?php
// update_profile.php
require_once 'config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    jsonResponse(false, 'You must be logged in to update your profile');
}

$user_id = $_SESSION['user_id'];
$display_name = isset($_POST['display_name']) ? sanitize($_POST['display_name']) : null;
$bio = isset($_POST['bio']) ? sanitize($_POST['bio']) : null;

// Validate input
if ($display_name && (strlen($display_name) < 3 || strlen($display_name) > 50)) {
    jsonResponse(false, 'Display name must be between 3 and 50 characters');
}

if ($bio && strlen($bio) > 500) {
    jsonResponse(false, 'Bio cannot exceed 500 characters');
}

// Check if profile exists
$check_sql = "SELECT * FROM user_profiles WHERE user_id = ?";
$check_stmt = $conn->prepare($check_sql);
$check_stmt->bind_param("i", $user_id);
$check_stmt->execute();
$check_result = $check_stmt->get_result();

if ($check_result->num_rows > 0) {
    // Update existing profile
    $sql = "UPDATE user_profiles SET display_name = ?, bio = ? WHERE user_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssi", $display_name, $bio, $user_id);
} else {
    // Create new profile
    $sql = "INSERT INTO user_profiles (user_id, display_name, bio) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("iss", $user_id, $display_name, $bio);
}

// Handle avatar upload if provided
$avatar_path = null;
if (isset($_FILES['avatar']) && $_FILES['avatar']['error'] == 0) {
    $allowed = ['jpg', 'jpeg', 'png', 'gif'];
    $filename = $_FILES['avatar']['name'];
    $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    
    if (in_array($ext, $allowed)) {
        $upload_path = 'uploads/avatars/';
        
        // Create directory if it doesn't exist
        if (!file_exists($upload_path)) {
            mkdir($upload_path, 0777, true);
        }
        
        $new_filename = uniqid() . '.' . $ext;
        $destination = $upload_path . $new_filename;
        
        if (move_uploaded_file($_FILES['avatar']['tmp_name'], $destination)) {
            $avatar_path = $new_filename;
            
            // Update avatar in database
            $avatar_sql = "UPDATE user_profiles SET avatar = ? WHERE user_id = ?";
            $avatar_stmt = $conn->prepare($avatar_sql);
            $avatar_stmt->bind_param("si", $avatar_path, $user_id);
            $avatar_stmt->execute();
        } else {
            jsonResponse(false, 'Failed to upload avatar');
        }
    } else {
        jsonResponse(false, 'Invalid file type. Only JPG, PNG, and GIF are allowed');
    }
}

if ($stmt->execute()) {
    jsonResponse(true, 'Profile updated successfully');
} else {
    jsonResponse(false, 'Error updating profile: ' . $stmt->error);
}
?>

<?php
// get_profile.php
require_once 'config.php';

if (!isset($_GET['user_id'])) {
    // Get current user's profile if no ID provided
    if (!isset($_SESSION['user_id'])) {
        jsonResponse(false, 'User ID is required');
    }
    $user_id = $_SESSION['user_id'];
} else {
    $user_id = (int)$_GET['user_id'];
}

// Get user profile
$sql = "SELECT u.username, u.points, u.rank, up.display_name, up.bio, up.avatar 
        FROM users u 
        LEFT JOIN user_profiles up ON u.user_id = up.user_id 
        WHERE u.user_id = ?";

$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $profile = $result->fetch_assoc();
    
    // Add stats
    $stats_sql = "SELECT
        (SELECT COUNT(*) FROM posts WHERE user_id = ?) as post_count,
        (SELECT COUNT(*) FROM comments WHERE user_id = ?) as comment_count,
        (SELECT COUNT(*) FROM reactions WHERE user_id = ?) as reaction_count";
    
    $stats_stmt = $conn->prepare($stats_sql);
    $stats_stmt->bind_param("iii", $user_id, $user_id, $user_id);
    $stats_stmt->execute();
    $stats_result = $stats_stmt->get_result();
    $stats = $stats_result->fetch_assoc();
    
    $profile = array_merge($profile, $stats);
    
    jsonResponse(true, 'Profile retrieved successfully', ['profile' => $profile]);
} else {
    jsonResponse(false, 'User not found');
}
?>

<?php
// Add this function to config.php
function updateUserRank($user_id) {
    global $conn;
    
    // Get user's points
    $points_sql = "SELECT points FROM users WHERE user_id = ?";
    $points_stmt = $conn->prepare($points_sql);
    $points_stmt->bind_param("i", $user_id);
    $points_stmt->execute();
    $points_result = $points_stmt->get_result();
    
    if ($points_result->num_rows > 0) {
        $user = $points_result->fetch_assoc();
        $points = $user['points'];
        
        // Define rank thresholds
        $ranks = [
            0 => 'Newcomer',
            20 => 'Regular',
            50 => 'Active Member',
            100 => 'Forum Expert',
            200 => 'Discussion Master',
            500 => 'Forum Legend'
        ];
        
        // Determine user's rank
        $current_rank = 'Newcomer';
        foreach ($ranks as $threshold => $rank) {
            if ($points >= $threshold) {
                $current_rank = $rank;
            } else {
                break;
            }
        }
        
        // Update user's rank
        $rank_sql = "UPDATE users SET rank = ? WHERE user_id = ?";
        $rank_stmt = $conn->prepare($rank_sql);
        $rank_stmt->bind_param("si", $current_rank, $user_id);
        $rank_stmt->execute();
    }
}
?>