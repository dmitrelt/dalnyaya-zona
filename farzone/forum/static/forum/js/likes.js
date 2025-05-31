document.addEventListener('DOMContentLoaded', function () {
    const likeIcons = document.querySelectorAll('.like-icon');
    console.log('Found like icons:', likeIcons.length);

    likeIcons.forEach(icon => {
        icon.addEventListener('click', function (event) {
            event.preventDefault();
            console.log('Like icon clicked:', this);

            const postId = this.dataset.postId;
            const postSlug = this.dataset.postSlug;
            const categorySlug = this.dataset.categorySlug;

            if (!postId || !postSlug || !categorySlug) {
                console.error('Missing data attributes:', { postId, postSlug, categorySlug });
                return;
            }

            const url = `/category/${categorySlug}/${postSlug}/like/`;
            console.log('Sending AJAX request to:', url);

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'same-origin'
            })
            .then(response => {
                console.log('Response status:', response.status, 'URL:', url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.status === 'success') {
                    const likesCountElement = document.querySelector(`.likes-count[data-post-id="${postId}"]`);
                    if (likesCountElement) {
                        likesCountElement.textContent = data.likes_count;
                    } else {
                        console.error('Likes count element not found for postId:', postId);
                    }

                    if (data.action === 'liked') {
                        this.classList.remove('bi-heart');
                        this.classList.add('bi-heart-fill');
                        this.dataset.liked = 'true';
                    } else {
                        this.classList.remove('bi-heart-fill');
                        this.classList.add('bi-heart');
                        this.dataset.liked = 'false';
                    }
                } else {
                    console.error('Invalid response status:', data.status);
                }
            })
            .catch(error => console.error('Fetch error:', error));
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});