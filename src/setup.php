<?php
// setup.php

try {
    // Create (or connect to) a file-based SQLite database
    $pdo = new PDO('sqlite:simulation.db');
    
    // Set error mode to exception for easier debugging
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 1. Create the table
    // We use INTEGER for boolean in SQLite (0 = false, 1 = true)
    $sql = "CREATE TABLE IF NOT EXISTS targets (
                key_id TEXT PRIMARY KEY,
                name TEXT,
                click INTEGER DEFAULT 0
            )";
    $pdo->exec($sql);

    // 2. Insert dummy data
    // We use prepared statements for security (even in simulations!)
    $stmt = $pdo->prepare("INSERT OR IGNORE INTO targets (key_id, name, click) VALUES (:key, :name, 0)");

    $targets = [
        ['key' => '7f62496b0cb865f7b99f9ff14f7de540a57119ec57b8ac99b4f45064318645ea', 'name' => 'Non'],
        ['key' => 'b5346bdbe8691b284e02ab0e0569da093a941d12e800691d254e995c37d10fcf', 'name' => 'Mat'],
        ['key' => '6d8c1edf0a8c123da81e3947b349c03327dba532cc6f2147edfa4d76d97aaaf2', 'name' => 'Pe'],
        ['key' => '30d1fe2b2c45f3fead1f1ad94e3976ed8f7f19563fb7806592da0a6b15ac8066', 'name' => 'Gimhong'],
    ];

    foreach ($targets as $target) {
        $stmt->execute($target);
    }

    echo "Database 'simulation.db' created and targets added successfully.";

} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>