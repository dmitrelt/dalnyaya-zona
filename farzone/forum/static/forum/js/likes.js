document.addEventListener('DOMContentLoaded', () => {
    const likeIcons = document.querySelectorAll('.like-icon');
    const isAuthenticated = document.body.dataset.authenticated === 'true';

    likeIcons.forEach(icon => {
        icon.addEventListener('click', async (e) => {
            if (!isAuthenticated) {
                window.location.href = '/users/login/';
                return;
            }

            const postId = icon.dataset.postId;
            const postSlug = icon.dataset.postSlug;
            const categorySlug = icon.dataset.categorySlug;
            const isLiked = icon.dataset.liked === 'true';

            if (!postId || !postSlug || !categorySlug) {
                console.error('Missing post data:', { postId, postSlug, categorySlug });
                return;
            }

            try {
                const response = await fetch(`/category/${categorySlug}/${postSlug}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin'
                });

                const data = await response.json();
                if (data.status === 'success') {
                    const likesCountElement = document.querySelector(`.likes-count[data-post-id="${postId}"]`);
                    if (likesCountElement) {
                        likesCountElement.textContent = data.likes_count;
                    }
                    icon.classList.toggle('bi-heart', data.action === 'unliked');
                    icon.classList.toggle('bi-heart-fill', data.action === 'liked');
                    icon.dataset.liked = data.action === 'liked' ? 'true' : 'false';
                } else {
                    alert(data.message || 'Ошибка при обработке лайка');
                }
            } catch (error) {
                console.error('Fetch error:', error);
                alert('Ошибка соединения');
            }
        });
    });

    function getCsrfToken() {
        const tokenElement = document.querySelector('meta[name="csrf-token"]');
        if (tokenElement) return tokenElement.content;
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }
});