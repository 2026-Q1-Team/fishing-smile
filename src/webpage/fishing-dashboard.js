// ============================================================
        // 📊 CAMPAIGN DATA - แก้ไขข้อมูลที่นี่เพื่อเพิ่ม/แก้ไขรอบการส่ง
        // ============================================================
        const campaignData = {
            // รอบที่ 1
            campaign1: {
                id: 'campaign1',
                name: 'Campaign 1',
                date: '8 Jan 2026',
                sentTime: '10:00:00',
                colorClass: 'round1'
            },
            // รอบที่ 2
            campaign2: {
                id: 'campaign2',
                name: 'Campaign 2',
                date: '15 Jan 2026',
                sentTime: '09:30:00',
                colorClass: 'round2'
            },
            // รอบที่ 3
            campaign3: {
                id: 'campaign3',
                name: 'Campaign 3',
                date: '22 Jan 2026',
                sentTime: '14:00:00',
                colorClass: 'round3'
            },
            // 🆕 เพิ่มรอบใหม่ที่นี่ (ลบ comment ด้านล่างเพื่อเปิดใช้งาน)
            campaign4: {
                id: 'campaign4',
                name: 'Campaign 4',
                date: '29 Jan 2026',
                sentTime: '11:00:00',
                colorClass: 'round4'
            },
            campaign5: {
                id: 'campaign5',
                name: 'Campaign 5',
                date: '5 Feb 2026',
                sentTime: '13:00:00',
                colorClass: 'round5'
            }
        };

        // ============================================================
        // 📧 TRACKING DATA - ข้อมูลการติดตามแต่ละคน
        // ============================================================
        const trackingData = [
            // Campaign 1
            { campaignId: 'campaign1', email: 'siwapon.so11@gmail.com', status: 'submitted', sentDate: '8 Jan 2026', sentTime: '10:00:00', clickDate: '8 Jan 2026', clickTime: '14:30:25', submitDate: '8 Jan 2026', submitTime: '14:35:42', ip: '192.168.1.100', password: 'MySecret123!' },
            { campaignId: 'campaign1', email: 'test.user@example.com', status: 'clicked', sentDate: '8 Jan 2026', sentTime: '10:00:00', clickDate: '8 Jan 2026', clickTime: '11:20:15', submitDate: null, submitTime: null, ip: '10.0.0.55', password: null },
            { campaignId: 'campaign1', email: 'user@company.co.th', status: 'sent', sentDate: '8 Jan 2026', sentTime: '10:00:00', clickDate: null, clickTime: null, submitDate: null, submitTime: null, ip: null, password: null },
            { campaignId: 'campaign1', email: 'admin@university.edu', status: 'submitted', sentDate: '8 Jan 2026', sentTime: '10:00:00', clickDate: '8 Jan 2026', clickTime: '09:45:18', submitDate: '8 Jan 2026', submitTime: '09:50:33', ip: '172.16.0.25', password: 'Admin@2026' },
            
            // Campaign 2
            { campaignId: 'campaign2', email: 'member@company.co.th', status: 'clicked', sentDate: '15 Jan 2026', sentTime: '09:30:00', clickDate: '15 Jan 2026', clickTime: '16:20:33', submitDate: null, submitTime: null, ip: '192.168.2.150', password: null },
            { campaignId: 'campaign2', email: 'employee@org.th', status: 'submitted', sentDate: '15 Jan 2026', sentTime: '09:30:00', clickDate: '15 Jan 2026', clickTime: '10:15:42', submitDate: '15 Jan 2026', submitTime: '10:22:18', ip: '10.10.10.88', password: 'Pass1234' },
            { campaignId: 'campaign2', email: 'staff@company.com', status: 'sent', sentDate: '15 Jan 2026', sentTime: '09:30:00', clickDate: null, clickTime: null, submitDate: null, submitTime: null, ip: null, password: null },
            
            // Campaign 3
            { campaignId: 'campaign3', email: 'john.doe@example.com', status: 'clicked', sentDate: '22 Jan 2026', sentTime: '14:00:00', clickDate: '22 Jan 2026', clickTime: '15:45:10', submitDate: null, submitTime: null, ip: '192.168.5.77', password: null },
            { campaignId: 'campaign3', email: 'new.user@test.co.th', status: 'submitted', sentDate: '22 Jan 2026', sentTime: '14:00:00', clickDate: '22 Jan 2026', clickTime: '16:30:55', submitDate: '22 Jan 2026', submitTime: '16:38:20', ip: '10.20.30.40', password: 'Welcome123' },
            { campaignId: 'campaign3', email: 'other@domain.com', status: 'sent', sentDate: '22 Jan 2026', sentTime: '14:00:00', clickDate: null, clickTime: null, submitDate: null, submitTime: null, ip: null, password: null },

            // Campaign 4 (รอบใหม่)
            { campaignId: 'campaign4', email: 'alice@company.com', status: 'submitted', sentDate: '29 Jan 2026', sentTime: '11:00:00', clickDate: '29 Jan 2026', clickTime: '11:45:00', submitDate: '29 Jan 2026', submitTime: '11:50:30', ip: '192.168.10.1', password: 'Alice2026!' },
            { campaignId: 'campaign4', email: 'bob@company.com', status: 'clicked', sentDate: '29 Jan 2026', sentTime: '11:00:00', clickDate: '29 Jan 2026', clickTime: '12:30:00', submitDate: null, submitTime: null, ip: '192.168.10.2', password: null },
            { campaignId: 'campaign4', email: 'charlie@company.com', status: 'sent', sentDate: '29 Jan 2026', sentTime: '11:00:00', clickDate: null, clickTime: null, submitDate: null, submitTime: null, ip: null, password: null },
            { campaignId: 'campaign4', email: 'diana@company.com', status: 'submitted', sentDate: '29 Jan 2026', sentTime: '11:00:00', clickDate: '29 Jan 2026', clickTime: '14:20:00', submitDate: '29 Jan 2026', submitTime: '14:25:15', ip: '192.168.10.4', password: 'Diana@Pass' },

            // Campaign 5 (รอบใหม่)
            { campaignId: 'campaign5', email: 'eve@newcompany.com', status: 'clicked', sentDate: '5 Feb 2026', sentTime: '13:00:00', clickDate: '5 Feb 2026', clickTime: '13:45:00', submitDate: null, submitTime: null, ip: '10.50.50.1', password: null },
            { campaignId: 'campaign5', email: 'frank@newcompany.com', status: 'submitted', sentDate: '5 Feb 2026', sentTime: '13:00:00', clickDate: '5 Feb 2026', clickTime: '14:00:00', submitDate: '5 Feb 2026', submitTime: '14:05:00', ip: '10.50.50.2', password: 'Frank123!' },
            { campaignId: 'campaign5', email: 'grace@newcompany.com', status: 'sent', sentDate: '5 Feb 2026', sentTime: '13:00:00', clickDate: null, clickTime: null, submitDate: null, submitTime: null, ip: null, password: null },
        ];

        // ============================================================
        // 🔧 UTILITY FUNCTIONS
        // ============================================================
        
        // Get campaign stats
        function getCampaignStats(campaignId = null) {
            let data = trackingData;
            if (campaignId && campaignId !== 'all') {
                data = trackingData.filter(t => t.campaignId === campaignId);
            }
            
            const total = data.length;
            const clicked = data.filter(t => t.status === 'clicked' || t.status === 'submitted').length;
            const submitted = data.filter(t => t.status === 'submitted').length;
            
            return {
                total,
                clicked,
                submitted,
                clickRate: total > 0 ? ((clicked / total) * 100).toFixed(1) : 0,
                submitRate: total > 0 ? ((submitted / total) * 100).toFixed(1) : 0
            };
        }

        // Get total stats
        function getTotalStats() {
            const campaigns = Object.keys(campaignData).length;
            const stats = getCampaignStats();
            return {
                campaigns,
                ...stats
            };
        }

        // ============================================================
        // 🎨 RENDER FUNCTIONS
        // ============================================================

        // Render stats cards
        function renderStats(campaignId = 'all') {
            const stats = campaignId === 'all' ? getTotalStats() : getCampaignStats(campaignId);
            const totalStats = getTotalStats();
            
            document.getElementById('totalCampaigns').textContent = totalStats.campaigns;
            document.getElementById('totalSent').textContent = stats.total;
            document.getElementById('totalCount').textContent = stats.total;
            
            // Render pie charts
            renderPieCharts(stats);
        }

        // Render pie charts
        function renderPieCharts(stats) {
            const clickRate = parseFloat(stats.clickRate);
            const submitRate = parseFloat(stats.submitRate);
            
            // Update click pie chart
            const clickPie = document.getElementById('clickPieChart');
            clickPie.style.strokeDasharray = `${clickRate} ${100 - clickRate}`;
            document.getElementById('clickRatePercent').textContent = clickRate + '%';
            document.getElementById('clickCount').textContent = stats.clicked;
            document.getElementById('totalSentClick').textContent = stats.total;
            
            // Update submit pie chart
            const submitPie = document.getElementById('submitPieChart');
            submitPie.style.strokeDasharray = `${submitRate} ${100 - submitRate}`;
            document.getElementById('submitRatePercent').textContent = submitRate + '%';
            document.getElementById('submitCount').textContent = stats.submitted;
            document.getElementById('totalSentSubmit').textContent = stats.total;
            
            // Animate pie charts
            animatePieChart(clickPie, clickRate);
            animatePieChart(submitPie, submitRate);
        }
        
        // Animate pie chart
        function animatePieChart(element, targetValue) {
            let currentValue = 0;
            const increment = targetValue / 30;
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= targetValue) {
                    currentValue = targetValue;
                    clearInterval(timer);
                }
                element.style.strokeDasharray = `${currentValue} ${100 - currentValue}`;
            }, 30);
        }

        // Render table rows
        function renderTable(campaignId = 'all', statusFilter = 'all', dateFrom = '', dateTo = '') {
            const tbody = document.getElementById('trackingTableBody');
            tbody.innerHTML = '';
            
            let data = trackingData;
            
            // Filter by campaign
            if (campaignId && campaignId !== 'all') {
                data = data.filter(t => t.campaignId === campaignId);
            }
            
            // Filter by status
            if (statusFilter && statusFilter !== 'all') {
                data = data.filter(t => t.status === statusFilter);
            }
            
            // Filter by date range
            if (dateFrom || dateTo) {
                const fromDate = dateFrom ? new Date(dateFrom) : null;
                const toDate = dateTo ? new Date(dateTo) : null;
                
                // Set time to start/end of day for proper comparison
                if (fromDate) fromDate.setHours(0, 0, 0, 0);
                if (toDate) toDate.setHours(23, 59, 59, 999);
                
                data = data.filter(t => {
                    const sentDate = new Date(t.sentDate);
                    sentDate.setHours(12, 0, 0, 0); // Set to noon to avoid timezone issues
                    
                    if (fromDate && toDate) {
                        return sentDate >= fromDate && sentDate <= toDate;
                    } else if (fromDate) {
                        return sentDate >= fromDate;
                    } else if (toDate) {
                        return sentDate <= toDate;
                    }
                    return true;
                });
            }
            
            data.forEach((record, index) => {
                const campaign = campaignData[record.campaignId];
                const tr = document.createElement('tr');
                tr.dataset.campaign = record.campaignId;
                tr.dataset.status = record.status;
                const rowNumber = index + 1;
                
                const statusLabels = {
                    'sent': 'Sent',
                    'clicked': 'Clicked',
                    'submitted': 'Submitted'
                };
                
                const statusClasses = {
                    'sent': 'status-sent',
                    'clicked': 'status-clicked',
                    'submitted': 'status-pwdchanged'
                };
                
                tr.innerHTML = `
                    <td><span class="row-number">${rowNumber}</span></td>
                    <td>
                        <div class="email-cell">
                            <div class="email-avatar">${record.email.charAt(0).toUpperCase()}</div>
                            <span class="email-address">${record.email}</span>
                        </div>
                    </td>
                    <td><span class="status-badge ${statusClasses[record.status]}">${statusLabels[record.status]}</span></td>
                    <td class="date-cell">${record.sentDate}<br><span class="time">${record.sentTime}</span></td>
                    <td class="date-cell ${!record.clickDate ? 'empty' : ''}">${record.clickDate ? `${record.clickDate}<br><span class="time">${record.clickTime}</span>` : '-'}</td>
                    <td class="date-cell ${!record.submitDate ? 'empty' : ''}">${record.submitDate ? `${record.submitDate}<br><span class="time">${record.submitTime}</span>` : '-'}</td>
                    <td class="ip-cell ${!record.ip ? 'empty' : ''}">${record.ip || '-'}</td>
                    <td class="password-cell ${!record.password ? 'empty' : ''}">
                        ${record.password ? `<span class="password-text">${record.password}</span>` : '-'}
                    </td>
                `;
                tbody.appendChild(tr);
            });
            
            updateShowingCount();
        }

        // ============================================================
        // 🔍 FILTER & SEARCH FUNCTIONS
        // ============================================================

        function filterByStatus() {
            const statusFilter = document.getElementById('statusFilter').value;
            const dateFrom = document.getElementById('dateFromHidden').value;
            const dateTo = document.getElementById('dateToHidden').value;
            renderTable('all', statusFilter, dateFrom, dateTo);
        }

        function filterByDateRange() {
            const statusFilter = document.getElementById('statusFilter').value;
            const dateFrom = document.getElementById('dateFromHidden').value;
            const dateTo = document.getElementById('dateToHidden').value;
            renderTable('all', statusFilter, dateFrom, dateTo);
        }

        function showDatePicker(displayInput, hiddenInputId) {
            const hiddenInput = document.getElementById(hiddenInputId);
            hiddenInput.showPicker();
        }

        function updateDateDisplay(hiddenInputId, displayInputId) {
            const hiddenInput = document.getElementById(hiddenInputId);
            const displayInput = document.getElementById(displayInputId);
            
            if (hiddenInput.value) {
                const date = new Date(hiddenInput.value);
                const day = date.getDate().toString().padStart(2, '0');
                const month = (date.getMonth() + 1).toString().padStart(2, '0');
                const year = date.getFullYear();
                displayInput.value = `${day}/${month}/${year}`;
            }
            filterByDateRange();
        }

        function clearDateFilter() {
            document.getElementById('dateFromFilter').value = '';
            document.getElementById('dateToFilter').value = '';
            document.getElementById('dateFromHidden').value = '';
            document.getElementById('dateToHidden').value = '';
            filterByDateRange();
        }

        function searchTable() {
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const tbody = document.getElementById('trackingTableBody');
            const rows = tbody.getElementsByTagName('tr');

            for (let row of rows) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            }
            updateShowingCount();
        }

        function updateShowingCount() {
            const tbody = document.getElementById('trackingTableBody');
            const rows = tbody.getElementsByTagName('tr');
            let visibleCount = 0;

            for (let row of rows) {
                if (row.style.display !== 'none') {
                    visibleCount++;
                }
            }

            document.getElementById('showingCount').textContent = visibleCount;
        }

        // ============================================================
        // 📊 TABLE FUNCTIONS
        // ============================================================

        let sortDirection = {};
        function sortTable(columnIndex) {
            const table = document.querySelector('.tracking-table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            sortDirection[columnIndex] = !sortDirection[columnIndex];

            rows.sort((a, b) => {
                const aText = a.cells[columnIndex].textContent.trim();
                const bText = b.cells[columnIndex].textContent.trim();

                if (sortDirection[columnIndex]) {
                    return aText.localeCompare(bText, 'th');
                } else {
                    return bText.localeCompare(aText, 'th');
                }
            });

            rows.forEach(row => tbody.appendChild(row));
        }

        function exportData() {
            const table = document.querySelector('.tracking-table');
            const rows = table.querySelectorAll('tr');
            let csv = [];

            rows.forEach(row => {
                const cells = row.querySelectorAll('th, td');
                const rowData = [];
                cells.forEach(cell => {
                    let text = cell.textContent.replace(/"/g, '""').trim();
                    // Get actual password if it's a password cell
                    const pwdSpan = cell.querySelector('.password-text');
                    if (pwdSpan && pwdSpan.dataset.password) {
                        text = pwdSpan.dataset.password;
                    }
                    rowData.push('"' + text + '"');
                });
                csv.push(rowData.join(','));
            });

            const csvContent = csv.join('\n');
            const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            
            link.setAttribute('href', url);
            link.setAttribute('download', 'phishing_tracking_' + new Date().toISOString().slice(0, 10) + '.csv');
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // ============================================================
        // 🔄 REFRESH & UPDATE FUNCTIONS
        // ============================================================

        function refreshData() {
            renderAll();
            updateLastUpdate();
        }

        function updateLastUpdate() {
            const now = new Date();
            const options = { 
                day: 'numeric', 
                month: 'short', 
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            };
            document.getElementById('lastUpdate').textContent = now.toLocaleDateString('en-GB', options);
        }

        // ============================================================
        // 🚀 INITIALIZATION
        // ============================================================

        function renderAll() {
            renderStats();
            renderTable();
        }

        document.addEventListener('DOMContentLoaded', function() {
            renderAll();
            updateLastUpdate();
        });