<?php
// track.php
if (isset($_GET['key'])) {
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtrack67";
    $dbname     = "fishtrack.db"; 

    try {
        $conn = new mysqli($servername, $username, $password, $dbname);

        $stmt = $conn->prepare(
            "SELECT email FROM fishlist WHERE key_id = ?"
        );
        $stmt->bind_param("s", $_GET['key']);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        $stmt->close();

        if ($row) {
            $email = $row['email'];
            $stmt2 = $conn->prepare(
                "INSERT INTO fishlog (trackkey, datetime, email)
                 VALUES (?, NOW(), ?)"
            );
            $stmt2->bind_param("ss", $_GET['key'], $email);
            $stmt2->execute();
            $stmt2->close();
        }
        $conn->close();

        // Invisible success
        http_response_code(200);
    } catch (Exception $e) {
        http_response_code(500);
    }
}
?>
