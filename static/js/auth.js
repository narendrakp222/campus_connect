/* ==========================================================================
   CAMPUS CONNECT - AUTHENTICATION INTERACTION JAVASCRIPT
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    /* Password Toggle Visibility */
    const togglePasswordBtn = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener("click", () => {
            const isPassword = passwordInput.getAttribute("type") === "password";
            passwordInput.setAttribute("type", isPassword ? "text" : "password");
            togglePasswordBtn.textContent = isPassword ? "🙈" : "👁️";
        });
    }

    /* Client-side form validation */
    const authForms = document.querySelectorAll(".auth-form");

    authForms.forEach(form => {
        form.addEventListener("submit", (event) => {
            let isValid = true;

            // Remove existing errors
            form.querySelectorAll(".validation-error").forEach(err => err.remove());

            const showError = (input, message) => {
                const error = document.createElement("div");
                error.className = "validation-error";
                error.textContent = message;
                input.insertAdjacentElement("afterend", error);
                isValid = false;
            };

            const username = form.querySelector("#username");
            if (username && !username.value.trim()) {
                showError(username, "Username or email is required.");
            }

            const email = form.querySelector("#email");
            if (email) {
                if (!email.value.trim()) {
                    showError(email, "Campus email is required.");
                } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
                    showError(email, "Enter a valid email address.");
                }
            }

            const password = form.querySelector("#password");
            if (password) {
                if (!password.value.trim()) {
                    showError(password, "Password is required.");
                } else if (password.hasAttribute("minlength") && password.value.trim().length < 6) {
                    showError(password, "Password must be at least 6 characters.");
                }
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    });
});
