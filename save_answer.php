<?php
session_start();
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $userId = $_POST['user_id'];
    $questionId = $_POST['question_id'];
    $answer = $_POST['answer'];

    $stmt = $pdo->prepare("UPDATE answers SET user_answer = :user_answer WHERE question_number = :question_number AND user_id = :user_id");
    $stmt->execute(['user_answer' => $answer, 'question_number' => $questionId, 'user_id' => $userId]);
}
