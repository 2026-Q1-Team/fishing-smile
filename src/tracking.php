<?php
// track.php

if (isset($_GET['key'])) {
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtrack67";
    $dbname     = "fishtrack"; 

    try {
        $conn = new mysqli($servername, $username, $password, $dbname);
    
        $stmt2 = $conn->prepare(
            "INSERT INTO fishlog (track_key, datetime)
                VALUES (?, NOW())"
        );
        $stmt2->bind_param("s", $_GET['key']);
        $stmt2->execute();
        $stmt2->close();
    
        $conn->close();

        // Invisible success
        http_response_code(200);
    } catch (Exception $e) {
        http_response_code(500);
    }
}
?>
