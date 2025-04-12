<?php
// logout.php
require_once 'config.php';

// Destroy session
session_unset();
session_destroy();

jsonResponse(true, 'Logged out successfully');
?>