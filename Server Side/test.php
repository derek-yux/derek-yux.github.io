<?php
require_once "pdo.php";
require_once "util.php";
session_start();

if (!(isset($_SESSION['user_id']))) {
    die ('ACCESS DENIED');
}
if (isset($_POST['cancel'])) {
    header('Location: ../index.html');
    return;
}