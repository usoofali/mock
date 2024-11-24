<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit;
}

// Process the submission and calculate score
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Exam Completed</title>
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body {
            background-image: url('asset/logo.png'); /* Replace with your desired background image */
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }

        .container {
            max-width: 400px;
            margin: 100px auto; /* Adjust top and bottom margins */
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        h1 {
            font-size: 24px; /* Adjust font size as needed */
            font-weight: bold;
            margin-bottom: 20px;
        }

        a.btn {
            display: block;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Exam Successfully Submitted!</h1>
        <h3>Kindly walk out from the exam hall. </h3>
        <a href="index.php" class="btn btn-primary">Goto Login</a>
    </div>
</body>
</html>
