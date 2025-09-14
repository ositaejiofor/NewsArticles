// ===============================
// CSRF & AJAX Helper
// ===============================
function getCsrfToken() {
  const token = document.querySelector('[name=csrfmiddlewaretoken]');
  return token ? token.value : "";
}

function ajaxPost(url, body, onSuccess, onError) {
  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCsrfToken(),
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: body
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        if (typeof onSuccess === "function") onSuccess(data);
      } else {
        if (typeof onError === "function") onError(data);
        else alert(data.error || "Something went wrong");
      }
    })
    .catch(err => console.error("AJAX error:", err));
}

// ===============================
// UI Toggles
// ===============================
function toggleEdit(commentId) {
  document.getElementById(`edit-form-${commentId}`)?.classList.toggle("d-none");
}

function toggleReply(commentId) {
  document.getElementById(`reply-form-${commentId}`)?.classList.toggle("d-none");
}

function toggleReplies(commentId) {
  const repliesDiv = document.getElementById(`replies-${commentId}`);
  const toggleBtn = document.getElementById(`replies-toggle-${commentId}`);

  if (repliesDiv && toggleBtn) {
    const isHidden = repliesDiv.classList.contains("d-none");
    repliesDiv.classList.toggle("d-none", !isHidden);
    toggleBtn.textContent = isHidden
      ? "Hide replies ▲"
      : `View ${repliesDiv.children.length} replies ▼`;
  }
}

// ===============================
// Comment Actions
// ===============================
function toggleLike(commentId) {
  ajaxPost(`/comments/toggle-like/`, `id=${commentId}`, data => {
    const countSpan = document.getElementById(`like-count-${commentId}`);
    if (countSpan) countSpan.textContent = data.like_count;
  });
}

// ===============================
// Event Delegation for Forms
// ===============================
document.addEventListener("submit", function (e) {
  const form = e.target;

  // --- Reply form ---
  if (form.classList.contains("reply-comment-form")) {
    e.preventDefault();
    const commentId = form.dataset.comment;
    const content = form.querySelector("textarea").value;

    ajaxPost(
      `/comments/reply/`, // flat endpoint
      `id=${commentId}&content=${encodeURIComponent(content)}`,
      data => {
        const repliesDiv = document.getElementById(`replies-${data.parent_id}`);
        if (repliesDiv) repliesDiv.insertAdjacentHTML("beforeend", data.html);

        form.reset();
        toggleReply(commentId);
      }
    );
  }

  // --- Edit form ---
  if (form.classList.contains("edit-comment-form")) {
    e.preventDefault();
    const commentId = form.dataset.comment;
    const content = form.querySelector("textarea").value;

    ajaxPost(
      `/comments/edit/`, // flat endpoint
      `id=${commentId}&content=${encodeURIComponent(content)}`,
      data => {
        const oldDiv = document.getElementById(`comment-${data.comment_id}`);
        if (oldDiv) oldDiv.outerHTML = data.html;
      }
    );
  }
});
