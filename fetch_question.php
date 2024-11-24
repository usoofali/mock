<?php
session_start();
require 'db.php';

if (!isset($_GET['id'])) {
    die("Invalid request.");
}

$stmt = $pdo->prepare("SELECT * FROM answers WHERE question_number = :id AND user_id = :user_id");
$stmt->execute(['id' => $_GET['id'], 'user_id' => $_SESSION['user_id']]);
$question = $stmt->fetch();

echo json_encode($question);
