<?php
if (isset($_GET['k'])) {
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtracker67";
    $dbname     = "fishtrack";

    $conn = new mysqli($servername, $username, $password, $dbname);
    $stmt = $conn->prepare( "INSERT INTO fishlog (track_key, datetime) VALUES (? , NOW())" );
    $stmt->bind_param("s", $_GET['k']);
    $stmt->execute();
    $stmt->close();
    $conn->close();
}
?>
