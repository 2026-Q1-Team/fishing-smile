<?php
// admin.php

try {
    $pdo = new PDO('sqlite:simulation.db');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Get all targets from the database
    $stmt = $pdo->query("SELECT * FROM targets");
    $targets = $stmt->fetchAll(PDO::FETCH_ASSOC);

} catch (PDOException $e) {
    die("Error: " . $e->getMessage());
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Phishing Simulation Admin</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 50%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .clicked-yes { background-color: #ffcccc; color: #a00000; font-weight: bold; } /* Red for danger */
        .clicked-no { background-color: #ccffcc; color: green; } /* Green for safe */
    </style>
</head>
<body>

    <h1>Campaign Results</h1>
    <p><a href="admin.php">Refresh Data</a></p>

    <table>
        <thead>
            <tr>
                <th>Key ID</th>
                <th>Name</th>
                <th>Clicked?</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($targets as $row): ?>
            <tr class="<?php echo ($row['click'] == 1) ? 'clicked-yes' : 'clicked-no'; ?>">
                <td><?php echo htmlspecialchars($row['key_id']); ?></td>
                <td><?php echo htmlspecialchars($row['name']); ?></td>
                <td><?php echo ($row['click'] == 1) ? 'YES' : 'NO'; ?></td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>

</body>
</html>