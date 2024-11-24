<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit();
}

// Fetch exam session
$stmt = $pdo->prepare("SELECT * FROM exam_session WHERE user_id = :user_id");
$stmt->execute(['user_id' => $_SESSION['user_id']]);
$session = $stmt->fetch();

if (!$session || $session['submit_status'] != 0) {
    header("Location: index.php?error=1");
    exit();
}

$stmt = $pdo->prepare("SELECT * FROM answers WHERE user_id = :user_id");
$stmt->execute(['user_id' => $_SESSION['user_id']]);
$questions = $stmt->fetchAll();

$user_id = $_SESSION['user_id'];
$session_stmt = $pdo->prepare("SELECT * FROM exam_session WHERE user_id = :user_id");
$session_stmt->execute(['user_id' => $user_id]);
$exam_session = $session_stmt->fetch(PDO::FETCH_ASSOC);
$remaining_time = strtotime($exam_session['stop_at']) - time();

// Set the remaining time for the exam
$remainingTime = ceil($remaining_time);


?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Exam Page</title>
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <script src="jquery/jquery-3.2.1.min.js"></script>
    <style>
        body {
            background-image: url('asset/logo.png');
            /* Replace with your desired background image */
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }

        .container {
            max-width: 950px;
            /* Adjust width as needed */
            margin: 50px auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }

        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }

        #user-details {
            margin-bottom: 20px;
            padding: 15px;
            /* Add padding for better spacing */
            background-color: #f9f9f9;
            /* Light background for contrast */
            border: 1px solid #ddd;
            /* Border for definition */
            border-radius: 8px;
            /* Rounded corners */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            /* Subtle shadow for depth */
        }

        #user-details p {
            font-size: 32px;
            /* Slightly larger font for better readability */
            margin: 5px 0;
            /* Uniform margin for paragraphs */
            text-align: left;
            /* Align text to the left */
        }

        #timer {
            font-size: 18px;
            /* Larger font for timer */
            color: #d9534f;
            /* Red color for urgency */
            font-weight: bold;
            /* Make it bold */
            margin-bottom: 15px;
            /* Space below the timer */
            background-color: #f2dede;
            /* Light red background for visibility */
            padding: 10px;
            /* Padding for better text visibility */
            border-radius: 4px;
            /* Rounded corners for the timer */
        }

        #submit-exam {
            font-size: 18px;
            /* Larger button text */
            padding: 10px 20px;
            /* Increased padding for a larger button */
            border: none;
            /* Remove default border */
            border-radius: 4px;
            /* Rounded button corners */
            cursor: pointer;
            /* Pointer cursor on hover */
        }

        #submit-exam:hover {
            background-color: #c79300;
            /* Darker color on hover for effect */
        }

        .align-right {
            text-align: right;
            /* Align content to the right */
        }

        #question-section {
            border: 1px solid #ccc;
            padding: 20px;
        }

        #question {
            margin-bottom: 10px;
        }

        #options {
            margin-bottom: 20px;
        }

        .question-map {
            display: flex;
            flex-wrap: wrap;
            max-width: 100%;
            /* Ensures wrapping */
            justify-content: center;
            /* Center the questions */
        }

        .question-button {
            width: 4.5%;
            /* Adjust width for 20 buttons per row */
            margin: 2px;
            /* Add some margin for spacing */
            padding: 5px;
            /* Add padding for better readability */
        }

        .question-button.active {
            background-color: green !important;
        }
    </style>
</head>

<body>
    <div class="container">
        <h2>NATIONAL MOCK EXAMINATION FOR CHEW</h2>
        <div id="user-details" class="align-right">
            <p>Name: <?php echo htmlspecialchars($_SESSION['fullname']); ?></p>
            <p>Index Number: <?php echo htmlspecialchars($_SESSION['username']); ?></p>
            <div id="timer">Time Remaining: <span id="time"></span></div>
            <button id="submit-exam" class="btn btn-warning">Submit Exam</button>
        </div>

        <div id="question-section" class="mt-3">
            <b>
                <div id="question_no" class="h1"></div>
            </b>
            <div id="question" class="h4"></div>
            <div id="options"></div>
            <div class="align-right mt-3">
                <button id="prev-question" class="btn btn-success">Previous Question</button>
                <button id="next-question" class="btn btn-success">Next Question</button>
            </div>
        </div>


        <div id="question-map" class="question-map mt-3">
            <?php foreach ($questions as $q): ?>
                <button id="<?php echo "q".$q['question_number']; ?>" class="question-button btn btn-secondary" data-id="<?php echo $q['question_number']; ?>"
                    style="background-color: <?php echo $q['user_answer'] ? 'green' : 'gray'; ?>;">
                    <?php echo $q['question_number']; ?>
                </button>
            <?php endforeach; ?>
        </div>
    </div>
</body>

</html>

<script>
    let remainingTime = <?php echo $remainingTime; ?>;

    function formatTime(seconds) {
        const hours = String(Math.floor(seconds / 3600)).padStart(2, '0');
        const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        return `${hours}:${minutes}:${secs}`;
    }

    function updateTimer() {
        if (remainingTime <= 0) {
            	$.post('submit_exam.php', { user_id: <?php echo $_SESSION['user_id']; ?> })
                    .done(function () {
                        // Redirect on success
                        window.location.href = 'completed.php';
                    })
                    .fail(function () {
                        // Handle error case
                        alert("There was an error submitting your exam. Please try again.");
                        // Re-enable the button
                        $('#submit-exam').prop('disabled', false);
                    })
                    .always(function () {
                        // Hide loading indicator
                        $('#loading').hide();
                    });
        } else {
            $('#time').text(formatTime(remainingTime));
            remainingTime--;
        }
    }

    $(document).ready(function () {
        // Start timer
        updateTimer();
        setInterval(updateTimer, 1000);

        // Load the first question
        let currentQuestionId = $(".question-button").first().data("id");
        loadQuestion(currentQuestionId);

        // Load question on button click
        $('.question-button').click(function () {
            const questionId = $(this).data('id');
            loadQuestion(questionId);
            currentQuestionId = questionId;
        });

        // Handle answer selection
        $(document).on('change', 'input[name="answer"]', function () {
            const selectedAnswer = $(this).val();
            $.post('save_answer.php', { user_id: <?php echo $_SESSION['user_id']; ?>, question_id: currentQuestionId, answer: selectedAnswer }, function () {
                // Update button color
                $('.question-button[data-id="' + currentQuestionId + '"]').css('background-color', 'green');
            });
        });

        // Handle exam submission
        $('#submit-exam').click(function () {
            if (confirm("Are you sure you want to submit the exam?")) {
                // Disable the button to prevent multiple submissions
                $(this).prop('disabled', true);

                // Optional: Show a loading indicator
                $('#loading').show();

                $.post('submit_exam.php', { user_id: <?php echo $_SESSION['user_id']; ?> })
                    .done(function () {
                        // Redirect on success
                        window.location.href = 'completed.php';
                    })
                    .fail(function () {
                        // Handle error case
                        alert("There was an error submitting your exam. Please try again.");
                        // Re-enable the button
                        $('#submit-exam').prop('disabled', false);
                    })
                    .always(function () {
                        // Hide loading indicator
                        $('#loading').hide();
                    });
            }
        });
        $('#next-question').click(function () {
            if (currentQuestionId < 199) {
                currentQuestionId++;
                loadQuestion(currentQuestionId);
            }
        });

        $('#prev-question').click(function () {
            if (currentQuestionId > 1) {
                currentQuestionId--;
                loadQuestion(currentQuestionId);
            }
        });

    });

    // Function to load a question
    function loadQuestion(questionId) {
        $.get('fetch_question.php', { id: questionId }, function (data) {
            $('#question').text(data.question);
            $('#question_no').text('Q.' + data.question_number);
            $('#options').html(`
            <label><input type="radio" name="answer" value="1" ${data.user_answer == 1 ? 'checked' : ''}> A. ${data.option1}</label><br>
            <label><input type="radio" name="answer" value="2" ${data.user_answer == 2 ? 'checked' : ''}> B. ${data.option2}</label><br>
            <label><input type="radio" name="answer" value="3" ${data.user_answer == 3 ? 'checked' : ''}> C. ${data.option3}</label><br>
            <label><input type="radio" name="answer" value="4" ${data.user_answer == 4 ? 'checked' : ''}> D. ${data.option4}</label><br>
        `);
        }, 'json');
    }

</script>
</body>

</html>