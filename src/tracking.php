<?php
// track.php

if (isset($_GET['k'])) {
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtrack67";
    $dbname     = "fishtrack"; 

    try {
        $conn = new mysqli($servername, $username, $password, $dbname);

        $stmt = $conn->prepare(
            "SELECT track_key FROM fishlist WHERE fishlist.track_key = ?"
        );
        $stmt->bind_param("s", $_GET['k']);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        $stmt->close();
    
        if ($row == $_GET['k']) {
            $stmt2 = $conn->prepare(
                "INSERT INTO fishlog (track_key, datetime)
                    VALUES (?, NOW())"
            );
            $stmt2->bind_param("s", $_GET['k']);
            $stmt2->execute();
            $stmt2->close();
        
            $conn->close();
        }
        // Invisible success
        http_response_code(200);
    } catch (Exception $e) {
        http_response_code(500);
    }
}
?>
