document.addEventListener('DOMContentLoaded', () => {
    const postDetail = document.querySelector('.post-detail');
    if (!postDetail) return;

    const postId = postDetail.dataset.postId;
    const userId = postDetail.dataset.userId;
    const isAuthenticated = document.body.dataset.authenticated === 'true';

    if (!postId) {
        console.error('Missing post ID');
        return;
    }

    let socket = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    const reconnectDelay = 3000;

    function connectWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/post/${postId}/`;
        console.log('Attempting WebSocket connection:', wsUrl);

        socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            console.log(`WebSocket connected for post ${postId}`);
            reconnectAttempts = 0;
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'like_update') {
                    const { post_id, likes_count, action, user_id } = data;
                    const likesCountElement = document.querySelector(`.likes-count[data-post-id="${post_id}"]`);
                    const likeIcon = document.querySelector(`.like-icon[data-post-id="${post_id}"]`);

                    if (likesCountElement) {
                        likesCountElement.textContent = likes_count;
                    }

                    if (likeIcon && user_id !== userId && isAuthenticated) {
                        likeIcon.classList.toggle('bi-heart', action === 'unliked');
                        likeIcon.classList.toggle('bi-heart-fill', action === 'liked');
                        likeIcon.dataset.liked = action === 'liked' ? 'true' : 'false';
                    }
                    console.log(`Received like update: post ${post_id}, action ${action}, count ${likes_count}`);
                }
            } catch (error) {
                console.error('WebSocket message error:', error);
            }
        };

        socket.onclose = (event) => {
            console.warn(`WebSocket closed for post ${postId}: code ${event.code}, reason ${event.reason}`);
            if (reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;
                console.log(`Reconnecting WebSocket in ${reconnectDelay}ms... Attempt ${reconnectAttempts}`);
                setTimeout(connectWebSocket, reconnectDelay);
            } else {
                console.error('Max WebSocket reconnect attempts reached');
            }
        };

        socket.onerror = (error) => {
            console.error(`WebSocket error for post ${postId}:`, error);
            socket.close();
        };
    }

    connectWebSocket();
});