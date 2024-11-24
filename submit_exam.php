<?php
session_start();

// Include database connection
require 'db.php'; // Adjust the path as needed

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    header('Location: index.php'); // Redirect to login if not authenticated
    exit();
}

// Fetch user's answers from the answers
$user_id = $_SESSION['user_id'];
$query = "SELECT question_answer_id, user_answer, answer FROM answers WHERE user_id = ?";
$stmt = $pdo->prepare($query);
$stmt->execute([$user_id]);

$score_counter = 0;

// Iterate through the fetched answers and calculate the score
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    if ($row['user_answer'] === $row['answer']) {
        $score_counter++;
    }
}

// Update the total score in the exam_session
$update_query = "UPDATE exam_session SET submit_status = 1, total_score = ? WHERE user_id = ?";
$update_stmt = $pdo->prepare($update_query);
$update_stmt->execute([$score_counter, $user_id]);

// Redirect to the completed page
header('Location: completed.php');
exit();
