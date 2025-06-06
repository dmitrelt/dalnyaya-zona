document.addEventListener('DOMContentLoaded', function () {
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (!isAuthenticated) {
        console.log('User is not authenticated, WebSocket disabled');
        return;
    }

    const postId = document.querySelector('.post-detail')?.dataset.postId;
    const userId = document.querySelector('.post-detail')?.dataset.userId;

    if (!postId) {
        console.error('Post ID is missing');
        return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const postSocket = new WebSocket(`${protocol}${window.location.host}/ws/post/${postId}/`);

    postSocket.onopen = function () {
        console.log(`WebSocket connected for post ${postId}`);
    };

    postSocket.onmessage = function (e) {
        console.log('WebSocket message received:', e.data);
        try {
            const data = JSON.parse(e.data);
            if (data.type === 'like_update') {
                const message = data.message;
                const likesCountElement = document.querySelector(`.likes-count[data-post-id="${message.post_id}"]`);
                if (likesCountElement) {
                    likesCountElement.textContent = message.likes_count;
                    const likeIcon = document.querySelector(`.like-icon[data-post-id="${message.post_id}"]`);
                    if (message.action === 'liked' && message.user_id == userId) {
                        likeIcon.classList.remove('bi-heart');
                        likeIcon.classList.add('bi-heart-fill');
                        likeIcon.dataset.liked = 'true';
                    } else if (message.action === 'unliked' && message.user_id == userId) {
                        likeIcon.classList.remove('bi-heart-fill');
                        likeIcon.classList.add('bi-heart');
                        likeIcon.dataset.liked = 'false';
                    }
                } else {
                    console.error(`Likes count element not found for post ${message.post_id}`);
                }
            }
        } catch (error) {
            console.error('WebSocket message parsing error:', error);
        }
    };

    postSocket.onclose = function (e) {
        console.error('WebSocket for post closed:', e);
    };

    postSocket.onerror = function (e) {
        console.error('WebSocket error:', e);
    };
});