/* ==========================================================================
   CAMPUS CONNECT - INTERACTIVE POST & COMMENT JAVASCRIPT
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* Helper Toast Alert */
    function showToast(message, type = "info") {
        let container = document.getElementById("flashContainer");
        if (!container) {
            container = document.createElement("div");
            container.id = "flashContainer";
            container.className = "flash-container";
            document.body.appendChild(container);
        }

        const toast = document.createElement("div");
        toast.className = `toast-alert ${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
        `;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(100%)";
            toast.style.transition = "all 0.4s ease";
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    }

    /* Escape HTML string helper */
    function escapeHTML(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    /* ----------------------------------------------------------------------
     * LIKE / UNLIKE HANDLER (AJAX)
     * ---------------------------------------------------------------------- */
    document.addEventListener("click", async (event) => {
        const likeBtn = event.target.closest(".like-btn");
        if (!likeBtn) return;

        const postId = likeBtn.dataset.postId || likeBtn.closest(".post-card")?.dataset.postId;
        if (!postId) return;

        try {
            const response = await fetch(`/post/${postId}/like`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/json"
                }
            });

            const data = await response.json();

            if (response.ok && data.success) {
                const postCard = likeBtn.closest(".post-card");
                const likeSymbol = likeBtn.querySelector(".like-symbol");
                const likeText = likeBtn.querySelector(".like-text");
                const likeNumber = postCard ? postCard.querySelector(".like-number") : null;

                if (data.is_liked) {
                    likeBtn.classList.add("liked");
                    if (likeSymbol) likeSymbol.textContent = "♥";
                    if (likeText) likeText.textContent = "Liked";
                } else {
                    likeBtn.classList.remove("liked");
                    if (likeSymbol) likeSymbol.textContent = "♡";
                    if (likeText) likeText.textContent = "Like";
                }

                if (likeNumber && data.likes_count !== undefined) {
                    likeNumber.textContent = data.likes_count;
                }
            } else {
                showToast(data.message || "Please log in to like posts.", "warning");
            }
        } catch (err) {
            console.error("Error liking post:", err);
            showToast("Network error. Please try again.", "danger");
        }
    });

    /* ----------------------------------------------------------------------
     * DELETE POST HANDLER (AJAX)
     * ---------------------------------------------------------------------- */
    document.addEventListener("click", async (event) => {
        const deleteBtn = event.target.closest(".delete-post-btn");
        if (!deleteBtn) return;

        const postId = deleteBtn.dataset.postId;
        if (!postId) return;

        if (!confirm("Are you sure you want to delete this post?")) return;

        try {
            const response = await fetch(`/post/${postId}`, {
                method: "DELETE",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();

            if (response.ok && data.success) {
                const postCard = deleteBtn.closest(".post-card");
                if (postCard) {
                    postCard.style.opacity = "0";
                    postCard.style.transform = "scale(0.95)";
                    postCard.style.transition = "all 0.3s ease";
                    setTimeout(() => postCard.remove(), 300);
                }
                showToast("Post deleted successfully.", "success");
            } else {
                showToast(data.message || "Failed to delete post.", "danger");
            }
        } catch (err) {
            console.error("Error deleting post:", err);
            showToast("Error deleting post.", "danger");
        }
    });

    /* ----------------------------------------------------------------------
     * QUICK POST CREATOR HANDLER (AJAX)
     * ---------------------------------------------------------------------- */
    const quickPostBtn = document.getElementById("quickPostBtn");
    const quickPostContent = document.getElementById("quickPostContent");
    const quickPostCategory = document.getElementById("quickPostCategory");

    if (quickPostBtn && quickPostContent) {
        quickPostBtn.addEventListener("click", async () => {
            const content = quickPostContent.value.trim();
            const category = quickPostCategory ? quickPostCategory.value : "General";

            if (!content) {
                showToast("Please write something before publishing.", "warning");
                quickPostContent.focus();
                return;
            }

            quickPostBtn.disabled = true;
            quickPostBtn.textContent = "Publishing...";

            try {
                const response = await fetch("/create-post", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    body: JSON.stringify({ content, category })
                });

                const data = await response.json();

                if (response.ok && data.success && data.post) {
                    quickPostContent.value = "";
                    showToast("Post published to campus feed!", "success");

                    const feedContainer = document.getElementById("feedContainer");
                    if (feedContainer) {
                        const emptyMsg = feedContainer.querySelector(".empty-feed");
                        if (emptyMsg) emptyMsg.remove();

                        const p = data.post;
                        const postElement = document.createElement("article");
                        postElement.className = "post-card";
                        postElement.dataset.postId = p.id;
                        postElement.innerHTML = `
                            <div class="post-header">
                                <div class="user-info">
                                    <div class="avatar" style="background-color: ${p.author.avatar_color || '#6366f1'};">
                                        ${p.author.initial}
                                    </div>
                                    <div>
                                        <h3>
                                            <a href="/profile/${p.author.id}" style="color: inherit;">
                                                ${escapeHTML(p.author.full_name)}
                                            </a>
                                            <span class="post-tag">${escapeHTML(p.category)}</span>
                                        </h3>
                                        <span class="time">@${escapeHTML(p.author.username)} • ${p.formatted_time}</span>
                                    </div>
                                </div>
                                <button class="post-menu-btn delete-post-btn" title="Delete Post" data-post-id="${p.id}">🗑️</button>
                            </div>
                            <div class="post-content">
                                <p>${escapeHTML(p.content)}</p>
                            </div>
                            <div class="post-stats">
                                <span class="like-count">♥ <span class="like-number">0</span> Likes</span>
                                <span>💬 <span class="comment-number">0</span> Comments</span>
                            </div>
                            <div class="post-actions">
                                <button class="post-action like-btn" type="button" data-post-id="${p.id}">
                                    <span class="like-symbol">♡</span>
                                    <span class="like-text">Like</span>
                                </button>
                                <a href="/post/${p.id}" class="post-action comment-btn">
                                    💬 <span>Comment</span>
                                </a>
                            </div>
                        `;

                        feedContainer.prepend(postElement);
                    } else {
                        window.location.reload();
                    }
                } else {
                    showToast(data.message || "Failed to create post.", "danger");
                }
            } catch (err) {
                console.error("Error publishing post:", err);
                showToast("Network error creating post.", "danger");
            } finally {
                quickPostBtn.disabled = false;
                quickPostBtn.textContent = "Publish Post";
            }
        });
    }

    /* ----------------------------------------------------------------------
     * CHARACTER COUNTER FOR CREATE POST FORM
     * ---------------------------------------------------------------------- */
    const postContent = document.getElementById("postContent");
    const characterCount = document.getElementById("characterCount");

    if (postContent && characterCount) {
        postContent.addEventListener("input", () => {
            characterCount.textContent = postContent.value.length;
        });
    }

    /* ----------------------------------------------------------------------
     * COMMENT SUBMISSION HANDLER (AJAX)
     * ---------------------------------------------------------------------- */
    const commentForm = document.getElementById("commentForm");
    if (commentForm) {
        commentForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const commentInput = document.getElementById("commentInput");
            const commentText = commentInput ? commentInput.value.trim() : "";
            const actionUrl = commentForm.action;

            if (!commentText) {
                if (commentInput) commentInput.focus();
                return;
            }

            const submitBtn = commentForm.querySelector("button[type='submit']");
            if (submitBtn) submitBtn.disabled = true;

            try {
                const response = await fetch(actionUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    body: JSON.stringify({ comment: commentText })
                });

                const data = await response.json();

                if (response.ok && data.success && data.comment) {
                    commentInput.value = "";
                    const commentsContainer = document.getElementById("commentsContainer");
                    const noCommentsMsg = document.getElementById("noCommentsMsg");

                    if (noCommentsMsg) noCommentsMsg.remove();

                    if (commentsContainer) {
                        const c = data.comment;
                        const commentElement = document.createElement("div");
                        commentElement.className = "comment";
                        commentElement.dataset.commentId = c.id;
                        commentElement.innerHTML = `
                            <div class="avatar small" style="background-color: ${c.avatar_color || '#6366f1'};">
                                ${c.initial}
                            </div>
                            <div class="comment-body">
                                <div class="comment-box">
                                    <strong>${escapeHTML(c.author_name)} <span style="font-size: 11px; color: var(--text-subtle); font-weight: 400;">@${escapeHTML(c.username)}</span></strong>
                                    <p>${escapeHTML(c.content)}</p>
                                </div>
                                <div class="comment-meta">
                                    <span class="comment-time">${c.formatted_time}</span>
                                    <button class="delete-comment-btn" data-comment-id="${c.id}">Delete</button>
                                </div>
                            </div>
                        `;
                        commentsContainer.appendChild(commentElement);
                    }

                    // Update comment count
                    const commentCountEl = document.getElementById("commentCount");
                    if (commentCountEl && data.comments_count !== undefined) {
                        commentCountEl.innerHTML = `💬 <span class="comment-number">${data.comments_count}</span> Comments`;
                    }
                    showToast("Comment posted!", "success");
                } else {
                    showToast(data.message || "Failed to add comment.", "danger");
                }
            } catch (err) {
                console.error("Error posting comment:", err);
                showToast("Network error submitting comment.", "danger");
            } finally {
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }

    /* ----------------------------------------------------------------------
     * DELETE COMMENT HANDLER (AJAX)
     * ---------------------------------------------------------------------- */
    document.addEventListener("click", async (event) => {
        const deleteBtn = event.target.closest(".delete-comment-btn");
        if (!deleteBtn) return;

        const commentId = deleteBtn.dataset.commentId;
        if (!commentId) return;

        try {
            const response = await fetch(`/comment/${commentId}`, {
                method: "DELETE",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();

            if (response.ok && data.success) {
                const commentEl = deleteBtn.closest(".comment");
                if (commentEl) {
                    commentEl.style.opacity = "0";
                    commentEl.style.transform = "translateX(-10px)";
                    commentEl.style.transition = "all 0.3s ease";
                    setTimeout(() => commentEl.remove(), 300);
                }

                const commentCountEl = document.getElementById("commentCount");
                if (commentCountEl && data.comments_count !== undefined) {
                    commentCountEl.innerHTML = `💬 <span class="comment-number">${data.comments_count}</span> Comments`;
                }

                showToast("Comment deleted.", "success");
            } else {
                showToast(data.message || "Failed to delete comment.", "danger");
            }
        } catch (err) {
            console.error("Error deleting comment:", err);
            showToast("Network error deleting comment.", "danger");
        }
    });

});