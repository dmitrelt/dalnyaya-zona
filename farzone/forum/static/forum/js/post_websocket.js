document.addEventListener('DOMContentLoaded', () => {
    const postDetail = document.querySelector('.post-detail');
    if (!postDetail) return;

    const postId = postDetail.dataset.postId;
    const userId = postDetail.dataset.userId;

    if (!postId) {
        console.error('Missing post ID');
        return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws/post/${postId}/`;
    console.log('Connecting to WebSocket:', wsUrl);

    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        console.log(`WebSocket connected for post ${postId}`);
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === 'like_update') {
                const message = data.message;
                const likesCountElement = document.querySelector(`.likes-count[data-post-id="${message.post_id}"]`);
                const likeIcon = document.querySelector(`.like-icon[data-post-id="${message.post_id}"]`);

                if (likesCountElement) {
                    likesCountElement.textContent = message.likes_count;
                }

                if (likeIcon && message.user_id !== userId) {
                    likeIcon.classList.toggle('bi-heart', message.action === 'unliked');
                    likeIcon.classList.toggle('bi-heart-fill', message.action === 'liked');
                    likeIcon.dataset.liked = message.action === 'liked' ? 'true' : 'false';
                }
            }
        } catch (error) {
            console.error('WebSocket message error:', error);
        }
    };

    socket.onclose = (event) => {
        console.warn(`WebSocket closed for post ${postId}:`, event);
    };

    socket.onerror = (error) => {
        console.error(`WebSocket error for post ${postId}:`, error);
    };
});