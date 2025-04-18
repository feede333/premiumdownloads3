document.addEventListener('DOMContentLoaded', function() {
    // Variables para el sistema de pago
    let stripe, elements, cardElement;
    let currentProduct = null;
    
    // Inicializar Stripe (reemplaza con tu clave pública de Stripe)
    const initializeStripe = () => {
        stripe = Stripe('pk_test_TuClavePublicaDeStripeAqui');
        elements = stripe.elements();
        
        // Crear el elemento de tarjeta de crédito
        cardElement = elements.create('card', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#32325d',
                    fontFamily: 'Arial, sans-serif',
                }
            }
        });
        
        // Montar el elemento de tarjeta en el DOM
        cardElement.mount('#card-element');
        
        // Manejar errores de validación en tiempo real
        cardElement.on('change', function(event) {
            const displayError = document.getElementById('card-errors');
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
        });
    };
    
    // Función para abrir el modal de pago
    window.openPaymentModal = function(productId, productName, price) {
        const modal = document.getElementById('paymentModal');
        const productDetails = document.getElementById('productDetails');
        const totalPrice = document.getElementById('totalPrice');
        
        // Guardar la información del producto actual
        currentProduct = {
            id: productId,
            name: productName,
            price: price
        };
        
        // Mostrar los detalles del producto
        productDetails.innerHTML = `<p>${productName}</p>`;
        totalPrice.textContent = `$${price.toFixed(2)}`;
        
        // Mostrar el modal
        modal.style.display = 'block';
        
        // Inicializar Stripe si aún no se ha hecho
        if (!stripe) {
            initializeStripe();
        }
    };
    
    // Cerrar el modal cuando se hace clic en el botón de cerrar
    document.querySelector('.close-payment-modal').addEventListener('click', function() {
        document.getElementById('paymentModal').style.display = 'none';
    });
    
    // Cerrar el modal si se hace clic fuera del contenido
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('paymentModal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Manejar el envío del formulario de pago
    document.getElementById('payment-form').addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const submitButton = document.getElementById('submit-payment');
        const buttonText = document.getElementById('button-text');
        const spinner = document.getElementById('spinner');
        
        // Deshabilitar el botón y mostrar el spinner
        submitButton.disabled = true;
        buttonText.textContent = 'Procesando...';
        spinner.classList.remove('hidden');
        
        try {
            // Ejemplo: Crear una intención de pago en tu servidor
            const paymentIntent = await createPaymentIntent(currentProduct.id, currentProduct.price);
            
            // Confirmar el pago con Stripe
            const result = await stripe.confirmCardPayment(paymentIntent.clientSecret, {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: document.getElementById('name').value,
                        email: document.getElementById('email').value
                    }
                }
            });
            
            if (result.error) {
                // Mostrar error
                const errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else if (result.paymentIntent.status === 'succeeded') {
                // Pago exitoso, redirigir a la página de descarga o mostrar mensaje de éxito
                window.location.href = `download.html?id=${currentProduct.id}&token=${result.paymentIntent.id}`;
            }
        } catch (error) {
            console.error('Error en el proceso de pago:', error);
            document.getElementById('card-errors').textContent = 'Ha ocurrido un error al procesar el pago. Por favor intenta de nuevo.';
        } finally {
            // Restaurar el botón
            submitButton.disabled = false;
            buttonText.textContent = 'Pagar ahora';
            spinner.classList.add('hidden');
        }
    });
    
    // Función para crear una intención de pago en el servidor
    async function createPaymentIntent(productId, amount) {
        // Esta función debería comunicarse con tu servidor para crear una intención de pago
        // Este es solo un ejemplo, deberías implementar la llamada real a tu backend
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    clientSecret: 'test_client_secret',
                    amount: amount,
                    id: 'pi_example'
                });
            }, 1000);
        });
    }

    // Ejemplo de cómo agregar un botón de compra a tus tarjetas de producto
    function createProgramCard(program) {
        // ...código existente...
        
        const buyButton = document.createElement('button');
        buyButton.className = 'buy-button';
        buyButton.innerHTML = '<i class="fas fa-shopping-cart"></i> Comprar';
        buyButton.addEventListener('click', function() {
            openPaymentModal(program.id, program.name, program.price);
        });
        
        cardActions.appendChild(buyButton);
        // ...código existente...
    }
});