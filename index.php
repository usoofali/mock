<?php
session_start();
require 'db.php'; // Include your database connection

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Check if user exists
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    if ($user && $password == $user['password']) {
        // Check exam session
        $_SESSION['user_id'] = $user['user_id'];
        $_SESSION['username'] = $user['username'];
        $_SESSION['fullname'] = $user['fullname'];
        header("Location: instruction.php");

    } else {
        $error = 'Invalid index or password';
    }
}

if(isset($_GET["error"]))
    $error = 'Your examination has been submitted or session has expired.';
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <style>
        body {
            background-image: url('asset/background.jpg');
            /* Replace with your desired background image */
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }

        .container {
            max-width: 600px;
            margin: 50px auto;
            /* Add top and bottom margins */
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            /* Semi-transparent white background */
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }

        img {
            display: block;
            margin: 0 auto;
            max-width: 50%;
            /* Reduced to 50% */
            height: auto;
            margin-bottom: 20px;
        }

        form {
            margin-top: 20px;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 15px;
        }

        button {
            background-color: #4CAF50;
            color: white;
            width: 100%;
            padding: 15px 30px;
            /* Increased padding for larger button */
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #3e8e41;
        }

        p {
            color: red;
            text-align: center;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>CHEW MOCK EXAMINATION</h1>
        <img src="asset/logo.png" alt="Logo">
        <form method="POST">
            <input type="text" name="username" placeholder="Index Number" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
            <?php if (isset($error))
                echo "<p>$error</p>"; ?>
        </form>
    </div>
</body>

</html>