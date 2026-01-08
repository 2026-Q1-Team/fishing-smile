<?php
if (isset($_GET['k'])) {
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtracker67";
    $dbname     = "fishtrack";

    $conn = new mysqli($servername, $username, $password, $dbname);
    $stmt = $conn->prepare(
        "SELECT track_key FROM fishlist WHERE track_key = ?"
    );
    $stmt->bind_param("s", $_GET['k']);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    $stmt->close();

    if ( $row == $_GET['k']) {
        $stmt2 = $conn->prepare(
            "INSERT INTO fishlog (track_key, datetime) VALUES (? , NOW())"
        );
        $stmt2->bind_param("s", $GET['k']);
        $stmt2->execute();
        $stmt2->close();
    }
    $conn->close();
}
?>
