document.addEventListener('DOMContentLoaded', function() {
    // Variables para el sistema de pago
    let currentProduct = null;
    
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
            // Obtener datos del formulario
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            
            // Crear solicitud de pago a Paykassa (a través de tu backend)
            const paymentResponse = await createPaykassaPayment({
                amount: currentProduct.price,
                currency: 'USD', // o la moneda que prefieras
                orderId: `order_${Date.now()}`, // generar un ID único para el pedido
                productId: currentProduct.id,
                productName: currentProduct.name,
                customerName: name,
                customerEmail: email
            });
            
            if (paymentResponse.success) {
                // Redirigir al usuario a la página de pago de Paykassa
                window.location.href = paymentResponse.redirectUrl;
            } else {
                // Mostrar error
                document.getElementById('card-errors').textContent = paymentResponse.message || 'Error al procesar el pago';
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
    
    // Función para crear una solicitud de pago a Paykassa (a través de tu backend)
    async function createPaykassaPayment(paymentData) {
        try {
            // Esta es una solicitud a tu propio backend, que luego se comunicará con Paykassa
            const response = await fetch('/api/create-paykassa-payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(paymentData)
            });
            
            return await response.json();
        } catch (error) {
            console.error('Error al crear la solicitud de pago:', error);
            return {
                success: false,
                message: 'Error de comunicación con el servidor'
            };
        }
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