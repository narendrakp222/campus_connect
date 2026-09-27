document.addEventListener("DOMContentLoaded", () => {
const forms = document.querySelectorAll(".auth-form");


forms.forEach(form => {
    form.addEventListener("submit", (event) => {
        const username = form.querySelector("#username");
        const email = form.querySelector("#email");
        const password = form.querySelector("#password");
        const confirmPassword = form.querySelector("#confirm_password");

        let isValid = true;

        form.querySelectorAll(".validation-error").forEach(error => {
            error.remove();
        });

        const showError = (input, message) => {
            const error = document.createElement("small");
            error.className = "validation-error";
            error.textContent = message;
            error.style.color = "#e41e3f";
            input.insertAdjacentElement("afterend", error);
            isValid = false;
        };

        if (username && !username.value.trim()) {
            showError(username, "Username is required.");
        }

        if (email) {
            if (!email.value.trim()) {
                showError(email, "Email is required.");
            } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
                showError(email, "Enter a valid email address.");
            }
        }

        if (!password || !password.value.trim()) {
            if (password) {
                showError(password, "Password is required.");
            }
        }

        if (confirmPassword) {
            if (!confirmPassword.value.trim()) {
                showError(confirmPassword, "Please confirm your password.");
            } else if (password.value !== confirmPassword.value) {
                showError(confirmPassword, "Passwords do not match.");
            }
        }

        if (!isValid) {
            event.preventDefault();
        }
    });
});


});
