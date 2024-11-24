<?php
session_start();
require 'db.php';

// Ensure user is logged in
if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit();
}

// Fetch the exam session details
$user_id = $_SESSION['user_id'];
$username = $_SESSION['username'];
$session_stmt = $pdo->prepare("SELECT * FROM exam_session WHERE user_id = :user_id and username = :username");
$session_stmt->execute(['user_id' => $user_id, 'username' => $username]);
$exam_session = $session_stmt->fetch(PDO::FETCH_ASSOC);

if (!$exam_session) {
    // Insert new exam session
    $startedAt = date('Y-m-d H:i:s', time());
    $stopAt = date('Y-m-d H:i:s', time() + (90 * 60)); // 80 minutes in seconds
    $insert_stmt = $pdo->prepare("INSERT INTO exam_session (user_id, username, started_at, stop_at, submit_status, total_score) VALUES (:user_id, :username, :started_at, :stop_at, 0, 0)");
    $insert_stmt->execute([
        'user_id' => $user_id,
        'username' => $username,
        'started_at' => $startedAt,
        'stop_at' => $stopAt
    ]);
    // Fetch random questions
    $stmt = $pdo->query("SELECT * FROM question ORDER BY RAND() LIMIT 200");
    $questions = $stmt->fetchAll();

    // Insert questions into answers_table
    foreach ($questions as $index => $question) {
        $stmt = $pdo->prepare("INSERT INTO answers (question_number, question, option1, option2, option3, option4, answer, user_answer, user_id) VALUES (:question_number, :question, :option1, :option2, :option3, :option4, :answer, 0, :user_id)");
        $stmt->execute([
            'question_number' => $index + 1,
            'question' => $question['question'],
            'option1' => $question['option1'],
            'option2' => $question['option2'],
            'option3' => $question['option3'],
            'option4' => $question['option4'],
            'answer' => $question['answer'],
            'user_id' => $_SESSION['user_id']
        ]);
    }

    header("Location: exam.php");
    exit();

} elseif ($exam_session['submit_status'] == 0 && time() < strtotime($exam_session['stop_at'])) {
    // Calculate remaining time for ongoing session
    header("Location: exam.php");
    exit();

} else {
    header("Location: index.php?error=1");
    exit();
}



