<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
}

$user_id = $_SESSION['user_id'];
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Exam Instructions</title>
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <style>
        body {
            background-image: url('asset/logo.png');
            /* Replace with your desired background image */
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }

        .container {
            max-width: 850px;
            margin: 50px auto;
            /* Add top and bottom margins */
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            /* Semi-transparent white background */
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            text-align: center;
            /* Center the content within the container */
        }

        .logout-button {
            float: right;
            /* Position the logout button to the right */
        }


        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }

        p {
            text-align: center;
            margin-bottom: 20px;
        }

        ul {
            list-style: none;
            padding: 0;
            margin: 0;
            text-align: left;
            /* Align list items to the left */
        }

        li {
            margin-bottom: 10px;
        }

        a.btn {
            display: block;
            margin: 0 auto;
            margin-bottom: 10px;
            /* Adjust spacing between buttons */
        }
    </style>
</head>

<body>
    <div class="container">
        <a href="logout.php" class="btn btn-secondary logout-button">Logout</a>
        <h1>Welcome, <?php echo htmlspecialchars($_SESSION['fullname']); ?>!</h1>
        <h2>EXAMINATION INSTRUCTIONS</h2>
        <p>Read the instructions carefully before starting the exam.</p>
        <ul>
            <li>Exam Duration: 90 minutes</li>
            <li>Number of Questions: 200</li>
            <li>Question Type: Multiple Choice</li>
            <li>Marking Scheme: Each question carries equal marks.</li>
        </ul>
        <ul>
            <li>Choose One Answer: For each question, select the most appropriate answer from the given options.</li>
            <li>Time Management: Allocate your time wisely to ensure you can complete all questions within the allotted
                time.</li>

            <li>Prohibited Materials: No electronic devices, such as calculators or phones, are allowed during the exam.
            </li>
            <li>Adhere to Exam Rules: Follow all exam rules and regulations strictly. Any violations may result in
                disciplinary action.</li>
        </ul>
        <h3>Additional Notes:</h3>
        <ul>
            <li>If you have any questions or concerns during the exam, raise your hand to signal the invigilator.</li>
        </ul>
        <a href="start_exam.php" class="btn btn-success">Start Exam</a>

    </div>
</body>

</html>