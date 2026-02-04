<?php
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtracker67";
    $dbname     = "fishtrack";
    $conn = new mysqli($servername, $username, $password, $dbname);
    $conn->query("SET time_zone = '+07:00'");
if (isset($_GET['k'])) {
    $stmt = $conn->prepare( "insert into fishhook(`ID`, `KEY`, `CLICK`) SELECT `ID`, `KEY`, NOW() FROM fishcast where `KEY` = ?" );
    $stmt->bind_param("s", $_GET['k']);
    $stmt->execute();
    $stmt->close();
    $conn->close();
}
elseif (isset($_GET['k2'])){
    $stmt = $conn->prepare( "insert into fishcook(`ID`, `KEY`, `PWND`, `TEXT`) SELECT `ID`, `KEY`, NOW(), ? FROM fishcast where `KEY` = ?" );
    $stmt->bind_param("ss", $_GET['p'], $_GET['k2']);
    $stmt->execute();
    $stmt->close();
    $conn->close();
}
?>
