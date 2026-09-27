document.addEventListener("DOMContentLoaded", () => {
const editButton = document.querySelector(".edit-profile-btn");
const editModal = document.querySelector("#editProfileModal");
const editForm = document.querySelector("#editProfileForm");
const closeModalButton = document.querySelector(".close-modal");


if (editButton && editModal) {
    editButton.addEventListener("click", (event) => {
        event.preventDefault();
        editModal.classList.add("active");
        document.body.classList.add("modal-open");
    });
}

if (closeModalButton && editModal) {
    closeModalButton.addEventListener("click", () => {
        editModal.classList.remove("active");
        document.body.classList.remove("modal-open");
    });
}

if (editModal) {
    editModal.addEventListener("click", (event) => {
        if (event.target === editModal) {
            editModal.classList.remove("active");
            document.body.classList.remove("modal-open");
        }
    });
}

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && editModal?.classList.contains("active")) {
        editModal.classList.remove("active");
        document.body.classList.remove("modal-open");
    }
});

if (editForm) {
    editForm.addEventListener("submit", (event) => {
        const username = editForm.querySelector("#username");
        const email = editForm.querySelector("#email");
        const bio = editForm.querySelector("#bio");

        let isValid = true;

        editForm.querySelectorAll(".validation-error").forEach(error => {
            error.remove();
        });

        const showError = (input, message) => {
            const error = document.createElement("small");
            error.className = "validation-error";
            error.textContent = message;
            error.style.color = "#e41e3f";
            error.style.marginTop = "5px";
            input.insertAdjacentElement("afterend", error);
            isValid = false;
        };

        if (username && username.value.trim().length < 3) {
            showError(username, "Username must contain at least 3 characters.");
        }

        if (email) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!email.value.trim()) {
                showError(email, "Email is required.");
            } else if (!emailPattern.test(email.value.trim())) {
                showError(email, "Enter a valid email address.");
            }
        }

        if (bio && bio.value.length > 250) {
            showError(bio, "Bio must not exceed 250 characters.");
        }

        if (!isValid) {
            event.preventDefault();
        }
    });
}

const bioInput = document.querySelector("#bio");
const bioCounter = document.querySelector(".bio-counter");

if (bioInput && bioCounter) {
    const updateBioCounter = () => {
        bioCounter.textContent = `${bioInput.value.length}/250`;
    };

    bioInput.addEventListener("input", updateBioCounter);
    updateBioCounter();
}

const avatar = document.querySelector(".profile-avatar");

if (avatar) {
    avatar.addEventListener("click", () => {
        avatar.classList.toggle("avatar-active");
    });
}


});
