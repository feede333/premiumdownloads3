document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.querySelector('.comment-form');
    const commentsList = document.querySelector('.comments-list');
    const photoInput = document.querySelector('.photo-icon input');
    const imagePreview = document.querySelector('.image-preview');
    const captchaText = document.querySelector('.captcha-text');
    const refreshCaptcha = document.querySelector('.refresh-captcha');
    
    // Generar captcha
    function generateCaptcha() {
        const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        let captcha = '';
        for (let i = 0; i < 6; i++) {
            captcha += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        captchaText.textContent = captcha;
    }

    // Preview de imagen
    photoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <button type="button" class="remove-image">×</button>
                `;
            };
            reader.readAsDataURL(file);
        }
    });

    // Remover imagen
    imagePreview.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-image')) {
            imagePreview.innerHTML = '';
            photoInput.value = '';
        }
    });

    // Refrescar captcha
    refreshCaptcha.addEventListener('click', generateCaptcha);

    // Manejar envío de comentarios
    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('comment-name').value;
        const email = document.querySelector('.email-input').value;
        const comment = document.querySelector('.comment-textarea').value;
        const captchaInput = document.querySelector('.captcha-input').value;
        
        // Validar captcha
        if (captchaInput !== captchaText.textContent) {
            alert('El código captcha no coincide');
            return;
        }

        // Crear elemento de comentario
        const commentElement = document.createElement('div');
        commentElement.className = 'comment-card';
        
        let commentImage = '';
        if (photoInput.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                commentImage = `<img src="${e.target.result}" alt="Comment image" class="comment-image">`;
                finishCommentCreation();
            };
            reader.readAsDataURL(photoInput.files[0]);
        } else {
            finishCommentCreation();
        }

        function finishCommentCreation() {
            commentElement.innerHTML = `
                <div class="comment-header">
                    <span class="comment-author">${name}</span>
                    <span class="comment-date">${new Date().toLocaleDateString()}</span>
                </div>
                <div class="comment-text">${comment}</div>
                ${commentImage}
            `;
            
            commentsList.insertBefore(commentElement, commentsList.firstChild);
            commentForm.reset();
            imagePreview.innerHTML = '';
            generateCaptcha();
        }
    });

    // Generar captcha inicial
    generateCaptcha();
});