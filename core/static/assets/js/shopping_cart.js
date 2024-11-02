class ShoppingCart {
    constructor() {
        this.items = this.loadCart();
        this.bindEvents();
        this.updateCartUI();
        this.updateCartBadge();
    }

    loadCart() {
        const savedCart = localStorage.getItem('shopping-cart');
        return savedCart ? JSON.parse(savedCart) : [];
    }
    updateCartBadge() {
        const totalItems = this.items.reduce((sum, item) => sum + item.quantity, 0);
        const cartButton = document.querySelector('[data-bs-toggle="offcanvas"][data-bs-target="#shoppingCart"]');

        if (cartButton) {
            // Remove existing badge if any
            const existingBadge = cartButton.querySelector('.badge');
            if (existingBadge) {
                existingBadge.remove();
            }

            // Only add badge if there are items
            if (totalItems > 0) {
                const badge = document.createElement('span');
                badge.className = 'badge d-flex text-bg-info position-absolute top-0 start-100 translate-middle rounded-pill';
                badge.style.fontSize = '0.75rem';  // Adjust size to match your design
                badge.style.minWidth = '1.5rem';   // Ensure minimum width for single digits
                badge.innerHTML = totalItems > 99 ? '99+' : totalItems;

                // Add some extra styling for better positioning
                badge.style.transform = 'translate(-50%, -50%)';

                // Make sure the button has position relative for absolute positioning of badge
                cartButton.style.position = 'relative';

                cartButton.appendChild(badge);
            }
        }
    }
    saveCart() {
        localStorage.setItem('shopping-cart', JSON.stringify(this.items));
        this.updateCartUI();
        this.updateCartBadge();
    }

    formatPrice(price) {
        return '₹' + parseFloat(price).toLocaleString('en-IN');
    }

    async addItem(itemData, button) {
        // Show loading state
        this.setButtonLoading(button);

        try {
            // Simulate network delay (remove this in production)
            await new Promise(resolve => setTimeout(resolve, 800));

            const existingItem = this.items.find(item => item.id === itemData.id);

            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                this.items.push({
                    id: itemData.id,
                    name: itemData.name,
                    price: itemData.price,
                    image: itemData.image,
                    quantity: 1
                });
            }

            this.saveCart();
            this.setButtonSuccess(button);

            // Reset button after 2 seconds
            setTimeout(() => {
                this.resetButton(button);
            }, 2000);

        } catch (error) {
            console.error('Error adding item to cart:', error);
            this.setButtonError(button);
        }
    }

    setButtonLoading(button) {
        if (!button) return;

        const originalContent = button.innerHTML;
        if (!button.dataset.originalContent) {
            button.dataset.originalContent = originalContent;
        }

        button.classList.add('pe-none');
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Adding to cart...
        `;
    }

    setButtonSuccess(button) {
        if (!button) return;

        button.classList.remove('pe-none');
        button.innerHTML = `
            <i class="ci-check-circle me-2"></i>
            Added to cart!
        `;
        button.classList.remove('btn-dark');
        button.classList.add('btn-success');
    }

    setButtonError(button) {
        if (!button) return;

        button.classList.remove('pe-none');
        button.innerHTML = `
            <i class="ci-close-circle me-2"></i>
            Failed to add
        `;
        button.classList.remove('btn-dark');
        button.classList.add('btn-danger');

        setTimeout(() => {
            this.resetButton(button);
        }, 2000);
    }

    resetButton(button) {
        if (!button) return;

        button.classList.remove('pe-none');
        button.innerHTML = button.dataset.originalContent;
        button.classList.remove('btn-success', 'btn-danger');
        button.classList.add('btn-dark');
    }

    removeItem(itemId) {
        this.items = this.items.filter(item => item.id !== itemId);
        this.saveCart();
    }

    renderCartItem(item) {
        return `
            <div class="d-flex align-items-center mb-3" data-cart-item="${item.id}">
                <a class="flex-shrink-0" href="#">
                    <img src="${item.image}" class="bg-body-tertiary rounded" width="110" alt="${item.name}">
                </a>
                <div class="w-100 min-w-0 ps-3">
                    <h5 class="d-flex animate-underline mb-2">
                        <a class="d-block fs-sm fw-medium text-truncate animate-target" href="#">${item.name}</a>
                    </h5>
                    <div class="h6 pb-1 mb-2 text-start">
                        ${this.formatPrice(item.price)}
                    </div>
                    <div class="d-flex align-items-center justify-content-between">
                        <div class="count-input rounded-2">
                            <button type="button" class="btn btn-icon btn-sm" onclick="cart.updateQuantity('${item.id}', ${item.quantity - 1})" aria-label="Decrement quantity">
                                <i class="ci-minus"></i>
                            </button>
                            <input type="number" class="form-control form-control-sm" value="${item.quantity}" readonly>
                            <button type="button" class="btn btn-icon btn-sm" onclick="cart.updateQuantity('${item.id}', ${item.quantity + 1})" aria-label="Increment quantity">
                                <i class="ci-plus"></i>
                            </button>
                        </div>
                        <button type="button" class="btn-close fs-sm" onclick="cart.removeItem('${item.id}')" 
                                data-bs-toggle="tooltip" data-bs-custom-class="tooltip-sm" 
                                data-bs-title="Remove" aria-label="Remove from cart"></button>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        document.querySelectorAll('.btn-add-to-cart').forEach(button => {
            button.addEventListener('click', async (e) => {
                const button = e.currentTarget;
                const productContainer = button.closest('[data-product]');
                if (productContainer) {
                    const productData = {
                        id: productContainer.dataset.productId,
                        name: productContainer.dataset.productName,
                        price: parseFloat(productContainer.dataset.productPrice),
                        image: productContainer.dataset.productImage
                    };
                    await this.addItem(productData, button);
                }
            });
        });
    }

    updateQuantity(itemId, newQuantity) {
        if (newQuantity < 1) {
            this.removeItem(itemId);
            return;
        }

        const item = this.items.find(item => item.id === itemId);
        if (item) {
            item.quantity = newQuantity;
            this.saveCart();
        }
    }

    updateCartUI() {
        const cartContainer = document.querySelector('#shoppingCart .offcanvas-body');

        if (this.items.length === 0) {
            cartContainer.innerHTML = `
                        <svg class="d-block mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" width="60" viewBox="0 0 29.5 30">
            <path class="text-body-tertiary"
                  d="M17.8 4c.4 0 .8-.3.8-.8v-2c0-.4-.3-.8-.8-.8-.4 0-.8.3-.8.8v2c0 .4.3.8.8.8zm3.2.6c.4.2.8 0 1-.4l.4-.9c.2-.4 0-.8-.4-1s-.8 0-1 .4l-.4.9c-.2.4 0 .9.4 1zm-7.5-.4c.2.4.6.6 1 .4s.6-.6.4-1l-.4-.9c-.2-.4-.6-.6-1-.4s-.6.6-.4 1l.4.9z"
                  fill="currentColor"></path>
            <path class="text-body-emphasis"
                  d="M10.7 24.5c-1.5 0-2.8 1.2-2.8 2.8S9.2 30 10.7 30s2.8-1.2 2.8-2.8-1.2-2.7-2.8-2.7zm0 4c-.7 0-1.2-.6-1.2-1.2s.6-1.2 1.2-1.2 1.2.6 1.2 1.2-.5 1.2-1.2 1.2zm11.1-4c-1.5 0-2.8 1.2-2.8 2.8a2.73 2.73 0 0 0 2.8 2.8 2.73 2.73 0 0 0 2.8-2.8c0-1.6-1.3-2.8-2.8-2.8zm0 4c-.7 0-1.2-.6-1.2-1.2s.6-1.2 1.2-1.2 1.2.6 1.2 1.2-.6 1.2-1.2 1.2zM8.7 18h16c.3 0 .6-.2.7-.5l4-10c.2-.5-.2-1-.7-1H9.3c-.4 0-.8.3-.8.8s.4.7.8.7h18.3l-3.4 8.5H9.3L5.5 1C5.4.7 5.1.5 4.8.5h-4c-.5 0-.8.3-.8.7s.3.8.8.8h3.4l3.7 14.6a3.24 3.24 0 0 0-2.3 3.1C5.5 21.5 7 23 8.7 23h16c.4 0 .8-.3.8-.8s-.3-.8-.8-.8h-16a1.79 1.79 0 0 1-1.8-1.8c0-1 .9-1.6 1.8-1.6z"
                  fill="currentColor"></path>
        </svg>
                <h6 class="mb-2">Your shopping cart is empty!</h6>
                <p class="fs-sm mb-4">Explore our products and add items to your cart.</p>
                <a class="btn btn-dark rounded-pill" href="/">Continue shopping</a>
            `;
        } else {
            let cartHTML = '<div class="cart-items">';

            this.items.forEach(item => {
                cartHTML += this.renderCartItem(item);
            });

            const subtotal = this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            const shipping = 0;
            const total = subtotal + shipping;

            cartHTML += `
                <div class="border-top pt-3">
                    <div class="d-flex justify-content-between mb-2">
                        <span class="fw-normal">Subtotal:</span>
                        <span class="fw-medium">${this.formatPrice(subtotal)}</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span class="fw-normal">Shipping:</span>
                        <span class="fw-medium">${shipping === 0 ? 'Free' : this.formatPrice(shipping)}</span>
                    </div>
                    <div class="d-flex justify-content-between mb-3">
                        <span class="fw-medium">Total:</span>
                        <span class="fw-medium fs-lg">${this.formatPrice(total)}</span>
                    </div>
                    <button class="btn btn-dark rounded-pill w-100" onclick="cart.checkout()">
                        Proceed to Checkout
                    </button>
                </div>
            </div>`;

            cartContainer.innerHTML = cartHTML;

            const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltips.forEach(tooltip => {
                new bootstrap.Tooltip(tooltip);
            });
        }
    }

    checkout() {
        window.location.href = '/checkout/';
    }
}

// Add CSS for transitions
const style = document.createElement('style');
style.textContent = `
    .btn-add-to-cart {
        transition: all 0.3s ease;
    }
    
    .btn-add-to-cart.pe-none {
        opacity: 0.8;
    }
    
    .btn-add-to-cart i {
        transition: transform 0.3s ease;
    }
    
    .btn-success i {
        transform: scale(1.2);
    }
`;
document.head.appendChild(style);

// Initialize cart
const cart = new ShoppingCart();

// Add CSS for the cart badge
const cart_COUNT_style = document.createElement('style');
cart_COUNT_style.textContent = `
    [data-bs-toggle="offcanvas"][data-bs-target="#shoppingCart"] {
        position: relative;
    }

    .cart-count {
        position: absolute;
        top: -8px;
        right: -8px;
        background-color: #dc3545;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 500;
        transform: scale(1);
        animation: badgePop 0.3s ease-out;
    }
    
    @keyframes badgePop {
        0% {
            transform: scale(0.5);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
`;
document.head.appendChild(cart_COUNT_style);