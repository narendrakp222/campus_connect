/* =========================================
   CAMPUS CONNECT - POST JAVASCRIPT
========================================= */


/* =========================================
   LIKE BUTTON
========================================= */

document.addEventListener("click", function (event) {

    const likeButton = event.target.closest(".like-btn");

    if (!likeButton) {
        return;
    }

    const postCard = likeButton.closest(".post-card");

    if (!postCard) {
        return;
    }

    const likeSymbol = likeButton.querySelector(".like-symbol");
    const likeText = likeButton.querySelector(".like-text");
    const likeNumber = postCard.querySelector(".like-number");

    let currentLikes = parseInt(likeNumber.textContent) || 0;

    if (likeButton.classList.contains("liked")) {

        likeButton.classList.remove("liked");

        if (likeSymbol) {
            likeSymbol.textContent = "♡";
        }

        if (likeText) {
            likeText.textContent = "Like";
        }

        currentLikes--;

    } else {

        likeButton.classList.add("liked");

        if (likeSymbol) {
            likeSymbol.textContent = "♥";
        }

        if (likeText) {
            likeText.textContent = "Liked";
        }

        currentLikes++;
    }

    if (likeNumber) {
        likeNumber.textContent = currentLikes;
    }

});


/* =========================================
   COMMENT BUTTON
========================================= */

document.addEventListener("click", function (event) {

    const commentButton = event.target.closest(".comment-btn");

    if (!commentButton) {
        return;
    }

    const postCard = commentButton.closest(".post-card");

    if (!postCard) {
        return;
    }

    const postId = postCard.dataset.postId;

    /*
     * Later, the backend team can replace this
     * with the actual Flask route.
     */

    window.location.href = `/post/${postId}`;

});


/* =========================================
   CREATE POST VALIDATION
========================================= */

const createPostForm = document.getElementById("createPostForm");

if (createPostForm) {

    createPostForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const postContent =
            document.getElementById("postContent");

        const errorBox =
            document.getElementById("postError");

        const content = postContent.value.trim();


        if (content.length === 0) {

            errorBox.textContent =
                "Please write something before publishing.";

            errorBox.hidden = false;

            postContent.focus();

            return;
        }


        if (content.length > 1000) {

            errorBox.textContent =
                "Your post cannot contain more than 1000 characters.";

            errorBox.hidden = false;

            return;
        }


        errorBox.hidden = true;


        /*
         * Frontend demonstration.
         *
         * When the Flask backend is ready,
         * this section can submit the data
         * to the backend using fetch() or
         * normal form submission.
         */

        alert("Post validated successfully!");

    });

}


/* =========================================
   CHARACTER COUNTER
========================================= */

const postContent =
    document.getElementById("postContent");

const characterCount =
    document.getElementById("characterCount");


if (postContent && characterCount) {

    postContent.addEventListener("input", function () {

        characterCount.textContent =
            postContent.value.length;

    });

}


/* =========================================
   COMMENT FORM
========================================= */

const commentForm =
    document.getElementById("commentForm");


if (commentForm) {

    commentForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const commentInput =
            document.getElementById("commentInput");

        const commentsContainer =
            document.getElementById("commentsContainer");

        const comment =
            commentInput.value.trim();


        if (comment.length === 0) {

            commentInput.focus();

            return;
        }


        /*
         * Create new comment element
         */

        const commentElement =
            document.createElement("div");

        commentElement.className = "comment";


        commentElement.innerHTML = `
            <div class="avatar small">
                P
            </div>

            <div class="comment-body">

                <div class="comment-box">

                    <strong>Prem Sagar</strong>

                    <p>${escapeHTML(comment)}</p>

                </div>

                <span class="comment-time">
                    Just now
                </span>

            </div>
        `;


        commentsContainer.appendChild(commentElement);


        commentInput.value = "";


        /*
         * Update comment count
         */

        const commentCount =
            document.getElementById("commentCount");

        if (commentCount) {

            const currentText =
                commentCount.textContent;

            const currentCount =
                parseInt(currentText) || 0;

            commentCount.textContent =
                `${currentCount + 1} Comments`;

        }

    });

}


/* =========================================
   QUICK CREATE POST
========================================= */

const quickPostBtn =
    document.getElementById("quickPostBtn");


if (quickPostBtn) {

    quickPostBtn.addEventListener("click", function () {

        const quickPostContent =
            document.getElementById("quickPostContent");

        const content =
            quickPostContent.value.trim();


        if (content.length === 0) {

            alert("Please write something before posting.");

            quickPostContent.focus();

            return;
        }


        addPostToFeed(content);

        quickPostContent.value = "";

    });

}


/* =========================================
   ADD POST TO FEED
========================================= */

function addPostToFeed(content) {

    const feedContainer =
        document.getElementById("feedContainer");

    if (!feedContainer) {
        return;
    }


    const postCard =
        document.createElement("article");

    postCard.className = "post-card";

    postCard.dataset.postId =
        Date.now();


    postCard.innerHTML = `

        <div class="post-header">

            <div class="user-info">

                <div class="avatar">
                    P
                </div>

                <div>

                    <h3>Prem Sagar</h3>

                    <span>
                        Just now
                    </span>

                </div>

            </div>

        </div>


        <div class="post-content">

            <p>
                ${escapeHTML(content)}
            </p>

        </div>


        <div class="post-stats">

            <span class="like-count">

                <span class="like-icon">
                    ♥
                </span>

                <span class="like-number">
                    0
                </span>

                Likes

            </span>

            <span>
                0 Comments
            </span>

        </div>


        <div class="post-actions">

            <button
                class="post-action like-btn"
                type="button">

                <span class="like-symbol">
                    ♡
                </span>

                <span class="like-text">
                    Like
                </span>

            </button>


            <button
                class="post-action comment-btn"
                type="button">

                💬
                <span>
                    Comment
                </span>

            </button>

        </div>
    `;


    feedContainer.prepend(postCard);

}


/* =========================================
   SECURITY HELPER
========================================= */

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}