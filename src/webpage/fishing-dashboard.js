let campaignData = {};
let trackingData = [];
const API_BASE = 'http://localhost:8001';

async function fetchDashboardData() {
    try {
        const response = await fetch(`${API_BASE}/api/dashboard`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        campaignData = {};
        data.campaigns.forEach((c, index) => {
            const key = `campaign${index + 1}`;
            campaignData[key] = {
                id: key,
                name: c.scheme || `Campaign ${index + 1}`,
                colorClass: `round${index + 1}`,
            };
        });

        trackingData = data.tracking.map(t => ({
            campaignId: `campaign${t.attack_uid}`,
            email: t.email,
            status: t.status,
            sentDate: t.sent_ts ? formatDate(t.sent_ts) : null,
            sentTime: t.sent_ts ? formatTime(t.sent_ts) : null,
            clickDate: t.click_ts ? formatDate(t.click_ts) : null,
            clickTime: t.click_ts ? formatTime(t.click_ts) : null,
            submitDate: t.submit_ts ? formatDate(t.submit_ts) : null,
            submitTime: t.submit_ts ? formatTime(t.submit_ts) : null,
            ip: t.detail?.ip || null,
            password: t.detail?.password || null,
        }));
        
        return true;

    } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        showError(`ไม่สามารถโหลดข้อมูลได้: ${error.message}`);
        return false;
    }
}

function formatDate(isoString) {
    const d = new Date(isoString);
    const day = d.getDate();
    const months = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'];
    return `${day} ${months[d.getMonth()]} ${d.getFullYear()}`;
}

function formatTime(isoString) {
    const d = new Date(isoString);
    return d.toTimeString().split(' ')[0];
}

function showError(message) {
    const tbody = document.getElementById('trackingTableBody');
    if (tbody) {
        tbody.innerHTML = `
        <tr>
            <td colspan="8" style="text-align:center; color:#ef4444; padding:2rem;">
                ${message}
            </td>
        </tr>
    `;
    }
}
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

        async function refreshData() {
            await fetchDashboardData();
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

        document.addEventListener('DOMContentLoaded', async function() {
            const success = await fetchDashboardData();
            if(success) {
                renderAll();
            }
            updateLastUpdate();
        });