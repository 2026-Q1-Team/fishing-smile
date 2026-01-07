<?php
// track.php

if (isset($_GET['key'])) {
    try {
        $pdo = new PDO('sqlite:simulation.db');
        // We set the timeout to avoid locking issues if multiple people click at once
        $pdo->setAttribute(PDO::ATTR_TIMEOUT, 5);
        
        $stmt = $pdo->prepare("UPDATE targets SET click = 1 WHERE key_id = :key");
        $stmt->execute(['key' => $_GET['key']]);
        
        // Return a simple success status (invisible to user)
        http_response_code(200);
    } catch (Exception $e) {
        http_response_code(500);
    }
}
?>