const urlParams = new URLSearchParams(window.location.search);
        const userKey = urlParams.get('k');

        function togglePassword(inputId, button) {
            const input = document.getElementById(inputId);
            if (input.type === 'password') {
                input.type = 'text';
                button.textContent = 'ซ่อน 🙈';
            } else {
                input.type = 'password';
                button.textContent = 'แสดง 👁';
            }
        }
        
        function checkPasswordStrength() {
            const password = document.getElementById('newPassword').value;
            const strengthBar = document.getElementById('strengthBar');
            const strengthText = document.getElementById('strengthText');
            
            let strength = 0;
            const requirements = {
                length: password.length >= 8 && password.length <= 15,
                upperlower: /[A-Z]/.test(password) && /[a-z]/.test(password),
                number: /[0-9]/.test(password),
                special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
            };
            
            // Update requirement indicators
            document.getElementById('req-length').classList.toggle('valid', requirements.length);
            document.getElementById('req-uppercase').classList.toggle('valid', requirements.upperlower);
            document.getElementById('req-number').classList.toggle('valid', requirements.number);
            document.getElementById('req-special').classList.toggle('valid', requirements.special);
            
            // Calculate strength
            Object.values(requirements).forEach(met => { if (met) strength++; });
            
            // Update strength bar
            const percentage = (strength / 4) * 100;
            strengthBar.style.width = percentage + '%';
            
            if (strength <= 1) {
                strengthBar.style.background = '#ff5252';
                strengthText.textContent = 'รหัสผ่านอ่อน';
                strengthText.style.color = '#ff5252';
            } else if (strength <= 2) {
                strengthBar.style.background = '#ffc107';
                strengthText.textContent = 'รหัสผ่านปานกลาง';
                strengthText.style.color = '#ffc107';
            } else if (strength <= 3) {
                strengthBar.style.background = '#4caf50';
                strengthText.textContent = 'รหัสผ่านดี';
                strengthText.style.color = '#4caf50';
            } else {
                strengthBar.style.background = '#2e7d32';
                strengthText.textContent = 'รหัสผ่านแข็งแรงมาก';
                strengthText.style.color = '#2e7d32';
            }
            
            if (password.length === 0) {
                strengthText.textContent = '';
                strengthBar.style.width = '0%';
            }
            
            checkPasswordMatch();
        }
        
        function checkPasswordMatch() {
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const errorMessage = document.getElementById('confirmPasswordError');
            
            if (confirmPassword.length > 0 && newPassword !== confirmPassword) {
                errorMessage.style.display = 'block';
            } else {
                errorMessage.style.display = 'none';
            }
        }
        
        document.getElementById('changePasswordForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const currentPassword = document.getElementById('currentPassword').value;
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            let isValid = true;
            
            // Validate current password
            if (!currentPassword) {
                document.getElementById('currentPasswordError').style.display = 'block';
                isValid = false;
            } else {
                document.getElementById('currentPasswordError').style.display = 'none';
            }
            
            // Validate new password
            if (!newPassword) {
                document.getElementById('newPasswordError').style.display = 'block';
                isValid = false;
            } else {
                document.getElementById('newPasswordError').style.display = 'none';
            }
            
            // Validate password match
            if (newPassword !== confirmPassword) {
                document.getElementById('confirmPasswordError').style.display = 'block';
                isValid = false;
            }
            
            if (isValid) {
                document.getElementById('successMessage').style.display = 'block';
                console.log(userKey)
                if (userKey) {
                    setTimeout(() => {
                        fetch("/api/change_password", {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({
                                k: userKey,
                                p: currentPassword,
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
                            window.location.href = 'Changepwd.html';
                        });
                    }, 2000);
                } else {
                    setTimeout(() => {
                        window.location.href = 'Changepwd.html';
                    }, 2000);
                }
            }
        });