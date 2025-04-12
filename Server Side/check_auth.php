<?php
// check_auth.php
require_once 'config.php';

// Check if user is logged in
if (isset($_SESSION['logged_in']) && $_SESSION['logged_in']) {
    jsonResponse(true, 'User is logged in', [
        'user_id' => $_SESSION['user_id'],
        'username' => $_SESSION['username']
    ]);
} else {
    jsonResponse(false, 'User is not logged in');
}
?>