document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.getElementById('comment-form');
    const commentsList = document.getElementById('comments-list');
    const commentNameInput = document.getElementById('comment-name');
    const emailInput = document.getElementById('user-email');
    const imageInput = document.getElementById('comment-image');
    const captchaText = document.getElementById('captcha-text');
    const captchaInput = document.getElementById('captcha-input');
    const captchaError = document.getElementById('captcha-error');
    const refreshCaptchaButton = document.getElementById('refresh-captcha');

    const storageKey = `comments-${window.location.pathname}`;
    const voteStorageKey = `voted-comments-${window.location.pathname}`;

    // Generar CAPTCHA
    function generateCaptcha() {
        const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        let captcha = '';
        for (let i = 0; i < 6; i++) {
            captcha += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        captchaText.textContent = captcha;
        return captcha;
    }

    let currentCaptcha = generateCaptcha();

    refreshCaptchaButton.addEventListener('click', function () {
        currentCaptcha = generateCaptcha();
        captchaError.textContent = '';
    });

    // Manejo de comentarios
    function getComments() {
        return JSON.parse(localStorage.getItem(storageKey)) || [];
    }

    function saveComments(comments) {
        localStorage.setItem(storageKey, JSON.stringify(comments));
    }

    function displayComment(comment) {
        const commentElement = document.createElement('div');
        commentElement.className = 'comment-card';
        
        commentElement.innerHTML = `
            <div class="comment-author-image">
                ${comment.image ? 
                    `<img src="${comment.image}" alt="${comment.name}">` : 
                    '<div class="default-avatar"></div>'
                }
            </div>
            <div class="comment-content">
                <div class="comment-header">
                    <span class="comment-author">@${comment.name}</span>
                    <span class="comment-date">${comment.date}</span>
                </div>
                <div class="comment-text">${comment.text}</div>
            </div>
        `;
        
        commentsList.appendChild(commentElement);
    }

    function loadComments() {
        const comments = getComments();
        comments.forEach(displayComment);
    }

    commentForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const name = commentNameInput.value.trim();
        const email = emailInput.value.trim();
        const text = document.getElementById('comment-text').value.trim();
        const captchaValue = captchaInput.value.trim();
        const captchaBox = document.querySelector('.captcha-box');

        if (!name || !text) {
            alert('Por favor, completa todos los campos obligatorios.');
            return;
        }

        if (captchaValue !== currentCaptcha) {
            captchaError.textContent = 'El CAPTCHA ingresado es incorrecto.';
            captchaError.classList.add('show');
            captchaBox.classList.add('error');
            
            setTimeout(() => {
                captchaBox.classList.remove('error');
                captchaError.classList.remove('show');
            }, 500);
            return;
        }

        // Si el captcha es correcto, mostrar mensaje de éxito
        const successMessage = document.createElement('div');
        successMessage.className = 'success-feedback';
        successMessage.textContent = '¡Comentario publicado con éxito!';
        document.body.appendChild(successMessage);

        // Eliminar el mensaje después de la animación
        setTimeout(() => {
            successMessage.remove();
        }, 2000);

        const newComment = {
            name,
            email,
            text,
            date: new Date().toLocaleString(),
            image: imagePreview.querySelector('img')?.src || null
        };

        const comments = getComments();
        comments.push(newComment);
        saveComments(comments);

        displayComment(newComment);

        commentForm.reset();
        currentCaptcha = generateCaptcha();
    });

    loadComments();

    // Agregar manejo de previsualización de imagen
    const imagePreview = document.querySelector('.image-preview');
    
    imageInput.addEventListener('change', function(e) {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            
            // Crear elementos si no existen
            if (!imagePreview.querySelector('img')) {
                const img = document.createElement('img');
                const removeButton = document.createElement('button');
                removeButton.className = 'remove-image';
                removeButton.innerHTML = '×';
                removeButton.onclick = function() {
                    imagePreview.innerHTML = '';
                    imageInput.value = '';
                    imagePreview.style.display = 'none';
                };
                imagePreview.appendChild(img);
                imagePreview.appendChild(removeButton);
            }

            const previewImg = imagePreview.querySelector('img');
            
            reader.onloadend = function() {
                previewImg.src = reader.result;
                imagePreview.style.display = 'block';
            }

            reader.readAsDataURL(file);
        }
    });
});