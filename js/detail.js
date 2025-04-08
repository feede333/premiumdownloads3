document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.getElementById('comment-form');
    const commentsList = document.getElementById('comments-list');
    const commentNameInput = document.getElementById('comment-name');
    const emailInput = document.getElementById('user-email');
    const imageInput = document.getElementById('comment-image');
    const reader = new FileReader();

    const storageKey = `comments-${window.location.pathname}`;
    const voteStorageKey = `voted-comments-${window.location.pathname}`;

    loadComments();

    function generateCaptcha() {
        const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        let captcha = '';
        for (let i = 0; i < 6; i++) {
            captcha += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        document.getElementById('captcha-text').textContent = captcha;
        return captcha;
    }

    let currentCaptcha = '';

    // Generar CAPTCHA inicial
    currentCaptcha = generateCaptcha();

    // Refrescar CAPTCHA
    document.getElementById('refresh-captcha').addEventListener('click', () => {
        currentCaptcha = generateCaptcha();
    });

    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const captchaInput = document.getElementById('captcha-input');
        const captchaError = document.getElementById('captcha-error');

        if (captchaInput.value !== currentCaptcha) {
            captchaError.textContent = 'Código CAPTCHA incorrecto';
            captchaError.classList.add('show');
            currentCaptcha = generateCaptcha();
            captchaInput.value = '';
            return;
        }

        const name = commentNameInput.value.trim();
        const email = emailInput.value.trim();
        const text = document.getElementById('comment-text').value.trim();
        
        if (!name || !text) {
            alert('Nombre y comentario son obligatorios');
            return;
        }

        const newComment = {
            id: Date.now(),
            name,
            email: email || null,
            text,
            date: new Date().toLocaleString('es-ES'),
            replies: [],
            votes: { up: 0, down: 0 }
        };

        let imageBase64 = null;

        if (imageInput.files[0]) {
            reader.onload = (e) => {
                imageBase64 = e.target.result;
                newComment.image = imageBase64;
                saveComment(newComment);
                displayComment(newComment);
                commentForm.reset();
                document.querySelector('.image-preview').innerHTML = ''; // Limpiar preview
            };
            reader.readAsDataURL(imageInput.files[0]);
        } else {
            saveComment(newComment);
            displayComment(newComment);
            commentForm.reset();
        }

        // Después de publicar el comentario
        captchaInput.value = '';
        currentCaptcha = generateCaptcha();
        captchaError.classList.remove('show');
    });

    // Agregar manejo de previsualización de imagen
    const imagePreview = document.querySelector('.image-preview');
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.innerHTML = `
                    <div class="preview-container">
                        <img src="${e.target.result}" class="preview-image" alt="Vista previa">
                        <button type="button" class="remove-image" aria-label="Eliminar imagen">×</button>
                    </div>
                `;

                // Agregar evento para eliminar la imagen
                const removeBtn = imagePreview.querySelector('.remove-image');
                removeBtn.addEventListener('click', function() {
                    imageInput.value = '';
                    imagePreview.innerHTML = '';
                });
            };
            reader.readAsDataURL(file);
        }
    });

    function saveComment(comment) {
        const comments = getComments();
        comments.push(comment);
        localStorage.setItem(storageKey, JSON.stringify(comments));
    }

    function displayComment(comment, isReply = false, parentId = null) {
        const commentElement = document.createElement('div');
        commentElement.className = 'comment-card';
        commentElement.dataset.commentId = comment.id;

        const votes = JSON.parse(localStorage.getItem(voteStorageKey)) || {};
        const userVote = votes[comment.id];
        const hasReplies = comment.replies && comment.replies.length > 0;

        commentElement.innerHTML = `
            <div class="comment-header">
                <div class="comment-author-info">
                    <div class="comment-avatar" style="background-image: url('${comment.image || 'default-avatar.png'}');"></div>
                    <div class="author-details">
                        <span class="comment-author">${comment.name}</span>
                        ${comment.email ? `<span class="comment-email">${comment.email}</span>` : ''}
                        <span class="comment-date">${comment.date}</span>
                    </div>
                </div>
                <div class="comment-actions">
                    <button class="action-btn vote-btn ${userVote === 'up' ? 'active' : ''}" data-vote="up">
                        👍 ${comment.votes.up}
                    </button>
                    <button class="action-btn vote-btn ${userVote === 'down' ? 'active' : ''}" data-vote="down">
                        👎 ${comment.votes.down}
                    </button>
                    <button class="action-btn reply-btn">Responder</button>
                </div>
            </div>
            <div class="comment-text">${comment.text}</div>
            <div class="reply-form" style="display:none;"></div>
            <div class="replies-section">
                ${hasReplies ? `
                    <button class="toggle-replies" data-shown="false">
                        Mostrar respuestas (${comment.replies.length})
                    </button>
                ` : ''}
                <div class="replies" style="display:none;"></div>
            </div>
        `;

        if (parentId) {
            const parentReplies = document.querySelector(`.comment-card[data-comment-id="${parentId}"] .replies`);
            if (parentReplies) {
                parentReplies.style.display = 'block';
                parentReplies.appendChild(commentElement);
            }
        } else {
            commentsList.appendChild(commentElement);
        }

        setupCommentEvents(commentElement, comment);
    }

    function setupCommentEvents(commentElement, comment) {
        const replyBtn = commentElement.querySelector('.reply-btn');
        const replyForm = commentElement.querySelector('.reply-form');

        replyBtn.addEventListener('click', () => {
            if (!replyForm.innerHTML) {
                replyForm.innerHTML = `
                    <input type="text" placeholder="Tu nombre" class="comment-input" required>
                    <input type="email" placeholder="Correo electrónico (opcional)" class="comment-input email-input">
                    <textarea placeholder="Escribe tu respuesta..." class="reply-textarea" required></textarea>
                    <div class="reply-actions">
                        <button type="button" class="reply-submit">Responder</button>
                        <button type="button" class="reply-cancel">Cancelar</button>
                    </div>
                `;

                const submitBtn = replyForm.querySelector('.reply-submit');
                const cancelBtn = replyForm.querySelector('.reply-cancel');

                submitBtn.addEventListener('click', async () => {
                    const name = replyForm.querySelector('input[type="text"]').value.trim();
                    const email = replyForm.querySelector('input[type="email"]').value.trim();
                    const text = replyForm.querySelector('textarea').value.trim();

                    if (!name || !text) {
                        alert('Nombre y respuesta son obligatorios.');
                        return;
                    }

                    submitBtn.classList.add('sending');
                    submitBtn.textContent = 'Enviando...';

                    await new Promise(resolve => setTimeout(resolve, 800));

                    const newReply = {
                        id: Date.now(),
                        name,
                        email: email || null,
                        text,
                        date: new Date().toLocaleString('es-ES'),
                        votes: { up: 0, down: 0 },
                        replies: [] // Asegurarnos de que cada respuesta pueda tener sus propias respuestas
                    };

                    if (!comment.replies) comment.replies = [];
                    comment.replies.push(newReply);

                    const comments = getComments();
                    updateComment(comments, comment);
                    localStorage.setItem(storageKey, JSON.stringify(comments));

                    showSuccessMessage('¡Respuesta publicada!');
                    
                    // Asegurarnos de que el contenedor de respuestas exista y sea visible
                    const repliesSection = commentElement.querySelector('.replies-section');
                    const repliesContainer = commentElement.querySelector('.replies');
                    let toggleBtn = commentElement.querySelector('.toggle-replies');
                    
                    if (!toggleBtn) {
                        // Crear el botón si no existe
                        toggleBtn = document.createElement('button');
                        toggleBtn.className = 'toggle-replies';
                        toggleBtn.dataset.shown = 'true';
                        repliesSection.insertBefore(toggleBtn, repliesContainer);
                        
                        // Agregar el event listener al nuevo botón
                        setupToggleRepliesButton(toggleBtn, repliesContainer, comment);
                    }

                    // Actualizar el texto del botón
                    toggleBtn.textContent = `Ocultar respuestas (${comment.replies.length})`;
                    toggleBtn.dataset.shown = 'true';
                    
                    // Mostrar el contenedor de respuestas
                    repliesContainer.style.display = 'block';
                    
                    // Mostrar la nueva respuesta
                    displayComment(newReply, true, comment.id);

                    // Limpiar el formulario
                    replyForm.innerHTML = '';
                    replyForm.style.display = 'none';
                });

                cancelBtn.addEventListener('click', () => {
                    replyForm.innerHTML = '';
                    replyForm.style.display = 'none';
                });
            }

            replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
        });

        const toggleBtn = commentElement.querySelector('.toggle-replies');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const repliesContainer = commentElement.querySelector('.replies');
                const isShown = toggleBtn.dataset.shown === 'true';

                if (!isShown && comment.replies.length > 0) {
                    if (repliesContainer.children.length === 0) {
                        comment.replies.forEach(reply => {
                            displayComment(reply, true, comment.id);
                        });
                    }
                }

                repliesContainer.style.display = isShown ? 'none' : 'block';
                toggleBtn.textContent = isShown ? 
                    `Mostrar respuestas (${comment.replies.length})` : 
                    `Ocultar respuestas (${comment.replies.length})`;
                toggleBtn.dataset.shown = !isShown;
            });
        }

        // Configurar eventos de votos
        const voteBtns = commentElement.querySelectorAll('.vote-btn');
        voteBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const voteType = btn.dataset.vote;
                const upBtn = commentElement.querySelector('[data-vote="up"]');
                const downBtn = commentElement.querySelector('[data-vote="down"]');
                handleVote(comment.id, voteType, upBtn, downBtn);
            });
        });
    }

    function showSuccessMessage(message) {
        const successMessage = document.createElement('div');
        successMessage.className = 'success-feedback';
        successMessage.textContent = message;
        document.body.appendChild(successMessage);

        setTimeout(() => {
            successMessage.remove();
        }, 1500);
    }

    function handleVote(commentId, type, upBtn, downBtn) {
        const votes = JSON.parse(localStorage.getItem(voteStorageKey)) || {};
        const comments = getComments();
        const comment = findComment(comments, commentId);

        if (!comment) return;

        const previousVote = votes[commentId];

        // Si ya votó lo mismo, eliminar el voto
        if (previousVote === type) {
            comment.votes[type]--;
            delete votes[commentId];
        } 
        // Si ya votó pero diferente, cambiar el voto
        else if (previousVote) {
            comment.votes[previousVote]--;
            comment.votes[type]++;
            votes[commentId] = type;
        }
        // Si no había votado, agregar nuevo voto
        else {
            comment.votes[type]++;
            votes[commentId] = type;
        }

        // Actualizar visual de los botones
        upBtn.classList.toggle('active', votes[commentId] === 'up');
        downBtn.classList.toggle('active', votes[commentId] === 'down');
        
        // Actualizar contadores
        upBtn.innerHTML = `👍 ${comment.votes.up}`;
        downBtn.innerHTML = `👎 ${comment.votes.down}`;

        // Guardar en localStorage
        localStorage.setItem(voteStorageKey, JSON.stringify(votes));
        localStorage.setItem(storageKey, JSON.stringify(comments));
    }

    function loadComments() {
        const comments = getComments();
        comments.forEach(comment => displayComment(comment));
    }

    function getComments() {
        return JSON.parse(localStorage.getItem(storageKey)) || [];
    }

    function findComment(comments, id) {
        for (const comment of comments) {
            if (comment.id == id) return comment;
            if (comment.replies && comment.replies.length > 0) {
                const found = findComment(comment.replies, id);
                if (found) return found;
            }
        }
        return null;
    }

    function updateComment(comments, updatedComment) {
        for (let i = 0; i < comments.length; i++) {
            if (comments[i].id === updatedComment.id) {
                comments[i] = updatedComment;
                return;
            }
            if (comments[i].replies && comments[i].replies.length > 0) {
                updateComment(comments[i].replies, updatedComment);
            }
        }
    }

    // Función auxiliar para configurar el botón de toggle
    function setupToggleRepliesButton(toggleBtn, repliesContainer, comment) {
        toggleBtn.addEventListener('click', () => {
            const isShown = toggleBtn.dataset.shown === 'true';

            if (!isShown && comment.replies.length > 0) {
                if (repliesContainer.children.length === 0) {
                    comment.replies.forEach(reply => {
                        displayComment(reply, true, comment.id);
                    });
                }
            }

            repliesContainer.style.display = isShown ? 'none' : 'block';
            toggleBtn.textContent = isShown ? 
                `Mostrar respuestas (${comment.replies.length})` : 
                `Ocultar respuestas (${comment.replies.length})`;
            toggleBtn.dataset.shown = !isShown;
        });
    }
});