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

    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const newComment = {
            id: Date.now(),
            name: commentNameInput.value.trim(),
            email: emailInput.value.trim(),
            text: document.getElementById('comment-text').value.trim(),
            date: new Date().toLocaleString('es-ES'),
            votes: { up: 0, down: 0 },
            replies: []
        };

        if (imageInput.files[0]) {
            reader.onload = (e) => {
                newComment.image = e.target.result;
                saveComment(newComment);
                displayComment(newComment);
                commentForm.reset();
                document.querySelector('.image-preview').innerHTML = '';
            };
            reader.readAsDataURL(imageInput.files[0]);
        } else {
            saveComment(newComment);
            displayComment(newComment);
            commentForm.reset();
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
            ${hasReplies ? `
                <button class="toggle-replies" data-shown="false">
                    Mostrar respuestas (${comment.replies.length})
                </button>
            ` : ''}
            <div class="replies" style="display:none;"></div>
        `;

        if (parentId) {
            const parentReplies = document.querySelector(`.comment-card[data-comment-id="${parentId}"] .replies`);
            if (parentReplies) {
                parentReplies.appendChild(commentElement);
            }
        } else {
            commentsList.appendChild(commentElement);
        }

        setupCommentEvents(commentElement, comment);

        if (hasReplies) {
            const toggleBtn = commentElement.querySelector('.toggle-replies');
            const repliesContainer = commentElement.querySelector('.replies');
            
            toggleBtn.addEventListener('click', () => {
                const isShown = toggleBtn.dataset.shown === 'true';
                
                if (!isShown) {
                    // Cargar respuestas si no se han cargado
                    if (repliesContainer.children.length === 0) {
                        comment.replies.forEach(reply => {
                            displayComment(reply, true, comment.id);
                        });
                    }
                    // Mostrar respuestas
                    repliesContainer.style.display = 'block';
                    toggleBtn.textContent = `Ocultar respuestas (${comment.replies.length})`;
                    toggleBtn.dataset.shown = 'true';
                } else {
                    // Ocultar respuestas
                    repliesContainer.style.display = 'none';
                    toggleBtn.textContent = `Mostrar respuestas (${comment.replies.length})`;
                    toggleBtn.dataset.shown = 'false';
                }
            });
        }
    }

    function setupCommentEvents(commentElement, comment) {
        const voteBtns = commentElement.querySelectorAll('.vote-btn');
        voteBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const voteType = btn.dataset.vote;
                const upBtn = commentElement.querySelector('[data-vote="up"]');
                const downBtn = commentElement.querySelector('[data-vote="down"]');
                handleVote(comment.id, voteType, upBtn, downBtn);
            });
        });
            
        const replyBtn = commentElement.querySelector('.reply-btn');
        replyBtn.addEventListener('click', () => {
            let replyForm = commentElement.querySelector('.reply-form');

            if (!replyForm.innerHTML) {
                replyForm.innerHTML = `
                    <input 
                        type="text" 
                        placeholder="Tu nombre" 
                        class="comment-input" 
                        required
                    >
                    <input 
                        type="email" 
                        placeholder="Correo electrónico (opcional)" 
                        class="comment-input email-input"
                    >
                    <textarea 
                        placeholder="Escribe tu respuesta..." 
                        class="reply-textarea"
                        required
                    ></textarea>
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

                    // Agregar clase sending al botón
                    submitBtn.classList.add('sending');
                    submitBtn.textContent = 'Enviando...';

                    // Simular delay de envío
                    await new Promise(resolve => setTimeout(resolve, 800));

                    const newReply = {
                        id: Date.now(),
                        name,
                        email: email || null,
                        text,
                        date: new Date().toLocaleString('es-ES'),
                        votes: { up: 0, down: 0 },
                        replies: []
                    };

                    // Agregar la respuesta y actualizar localStorage
                    if (!comment.replies) {
                        comment.replies = [];
                    }
                    comment.replies.push(newReply);
                    const comments = getComments();
                    updateComment(comments, comment);
                    localStorage.setItem(storageKey, JSON.stringify(comments));

                    // Mostrar mensaje de éxito
                    const successMessage = document.createElement('div');
                    successMessage.className = 'success-feedback';
                    successMessage.textContent = '¡Respuesta publicada!';
                    document.body.appendChild(successMessage);

                    // Eliminar mensaje después de la animación
                    setTimeout(() => {
                        successMessage.remove();
                    }, 1500);

                    // Mostrar la nueva respuesta
                    displayComment(newReply, true, comment.id);

                    // Restaurar el botón y limpiar el formulario
                    submitBtn.classList.remove('sending');
                    submitBtn.textContent = 'Responder';
                    replyForm.innerHTML = '';
                    replyForm.style.display = 'none';

                    // Actualizar contador de respuestas
                    const toggleBtn = commentElement.querySelector('.toggle-replies');
                    if (toggleBtn) {
                        toggleBtn.textContent = `Mostrar respuestas (${comment.replies.length})`;
                        toggleBtn.style.display = 'block';
                    }
                });

                cancelBtn.addEventListener('click', () => {
                    replyForm.innerHTML = '';
                    replyForm.style.display = 'none';
                });
            }

            replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
        });
    }

    function updateComment(comments, updatedComment) {
        for (let i = 0; i < comments.length; i++) {
            if (comments[i].id === updatedComment.id) {
                comments[i] = updatedComment;
                return true;
            }
            if (comments[i].replies && comments[i].replies.length > 0) {
                if (updateComment(comments[i].replies, updatedComment)) {
                    return true;
                }
            }
        }
        return false;
    }

    function handleVote(commentId, type, upBtn, downBtn) {
        const votes = JSON.parse(localStorage.getItem(voteStorageKey)) || {};
        const comments = getComments();
        const comment = findComment(comments, commentId);

        if (!comment) return;

        if (votes[commentId]) {
            const prevVote = votes[commentId];
            comment.votes[prevVote]--;
        }

        comment.votes[type]++;
        votes[commentId] = type;

        upBtn.classList.toggle('active', type === 'up');
        downBtn.classList.toggle('active', type === 'down');
        upBtn.innerHTML = `👍 ${comment.votes.up}`;
        downBtn.innerHTML = `👎 ${comment.votes.down}`;

        localStorage.setItem(voteStorageKey, JSON.stringify(votes));
        localStorage.setItem(storageKey, JSON.stringify(comments));
    }

    function loadComments() {
        const comments = getComments();
        comments.forEach(comment => {
            displayComment(comment);
        });
    }

    function getComments() {
        return JSON.parse(localStorage.getItem(storageKey)) || [];
    }

    function findComment(comments, id) {
        for (const comment of comments) {
            if (comment.id === id) return comment;
            if (comment.replies && comment.replies.length > 0) {
                const found = findComment(comment.replies, id);
                if (found) return found;
            }
        }
        return null;
    }
    // Removed redundant and misplaced code sections
});