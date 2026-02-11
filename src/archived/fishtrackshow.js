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
    
    animateCounter(totalEl, 5);
    animateCounter(activeEl, 5);
    animateCounter(todayEl, 2);
});