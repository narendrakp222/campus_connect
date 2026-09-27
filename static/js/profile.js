/* ==========================================================================
   CAMPUS CONNECT - PROFILE MODAL INTERACTION JAVASCRIPT
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const editProfileBtn = document.getElementById("editProfileBtn");
    const editProfileModal = document.getElementById("editProfileModal");
    const closeModalBtn = document.getElementById("closeModalBtn");
    const cancelModalBtn = document.getElementById("cancelModalBtn");

    function openModal() {
        if (editProfileModal) {
            editProfileModal.classList.add("active");
            document.body.style.overflow = "hidden";
        }
    }

    function closeModal() {
        if (editProfileModal) {
            editProfileModal.classList.remove("active");
            document.body.style.overflow = "auto";
        }
    }

    if (editProfileBtn) {
        editProfileBtn.addEventListener("click", openModal);
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", closeModal);
    }

    if (cancelModalBtn) {
        cancelModalBtn.addEventListener("click", closeModal);
    }

    if (editProfileModal) {
        editProfileModal.addEventListener("click", (e) => {
            if (e.target === editProfileModal) {
                closeModal();
            }
        });
    }
});
