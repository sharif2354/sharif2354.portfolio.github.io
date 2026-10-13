const API = 'http://localhost:8000';

// Navigation & Initialization
document.addEventListener('DOMContentLoaded', () => {
    const bar = document.getElementById('bar');
    const close = document.getElementById('close');
    const nav = document.getElementById('navbar');

    if (bar && nav) bar.addEventListener('click', () => nav.classList.add('active'));
    if (close && nav) close.addEventListener('click', (e) => { e.preventDefault(); nav.classList.remove('active'); });

    updateCartBadge();
    renderCart();
    initUserSession();
});

// Cart Helpers
function getCart() {
    return JSON.parse(localStorage.getItem('gv_cart')) || [];
}

function saveCart(cart) {
    localStorage.setItem('gv_cart', JSON.stringify(cart));
    updateCartBadge();
}

function updateCartBadge() {
    const count = getCart().reduce((sum, item) => sum + item.quantity, 0);
    const badges = document.querySelectorAll('#cart-count, .cart-badge');
    badges.forEach(b => { b.textContent = count; });
}

function addToCart(name, price, img = 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500', size = 'Normal') {
    const cart = getCart();
    const existing = cart.find(i => i.name === name && i.size === size);

    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ name, price: parseFloat(price), quantity: 1, size, image: img });
    }

    saveCart(cart);
    alert(`${name} has been added to your bag!`);
}

// Render Cart on cart.html
function renderCart() {
    const tbody = document.querySelector('#cart tbody');
    const subtotalEl = document.getElementById('subtotal-val');
    const totalEl = document.getElementById('total-val');
    if (!tbody) return;

    const cart = getCart();
    tbody.innerHTML = '';

    if (cart.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 30px;">Your shopping cart is empty.</td></tr>`;
        if (subtotalEl) subtotalEl.innerText = '$0.00';
        if (totalEl) totalEl.innerText = '$0.00';
        return;
    }

    let subtotal = 0;
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;

        const row = document.createElement('tr');
        row.innerHTML = `
            <td><a href="#" onclick="removeItem(${index}); return false;"><i class="fa-solid fa-trash-can" style="color: #dc3545;"></i></a></td>
            <td><img src="${item.image}" alt="${item.name}"></td>
            <td>${item.name} (${item.size})</td>
            <td>$${item.price.toFixed(2)}</td>
            <td><input type="number" value="${item.quantity}" min="1" onchange="updateQty(${index}, this.value)"></td>
            <td>$${itemTotal.toFixed(2)}</td>
        `;
        tbody.appendChild(row);
    });

    if (subtotalEl) subtotalEl.innerText = `$${subtotal.toFixed(2)}`;
    if (totalEl) totalEl.innerText = `$${subtotal.toFixed(2)}`;
}

function updateQty(index, qty) {
    const cart = getCart();
    const parsedQty = parseInt(qty, 10);
    if (parsedQty > 0) {
        cart[index].quantity = parsedQty;
        saveCart(cart);
        renderCart();
    }
}

function removeItem(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    renderCart();
}

// User Session UI
function initUserSession() {
    const user = JSON.parse(localStorage.getItem('gv_user'));
    const navUl = document.getElementById('navbar');

    if (user && navUl) {
        const authLi = document.createElement('li');
        authLi.innerHTML = `
            <span style="font-weight:700; color:#088178; padding: 0 10px;">Hi, ${user.fullName.split(' ')[0]}</span>
            <a href="#" id="gv-logout-btn" style="color:#dc3545; font-size:13px;">(Logout)</a>
        `;
        navUl.appendChild(authLi);

        document.getElementById('gv-logout-btn').addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('gv_user');
            localStorage.removeItem('gv_token');
            window.location.reload();
        });
    } else if (navUl) {
        const signLi = document.createElement('li');
        signLi.innerHTML = `<a href="login.html"><i class="fa-regular fa-user"></i> Sign In</a>`;
        navUl.appendChild(signLi);
    }

    const custName = document.getElementById('cust-name');
    const custPhone = document.getElementById('cust-phone');
    if (user) {
        if (custName && !custName.value) custName.value = user.fullName;
        if (custPhone && !custPhone.value) custPhone.value = user.phone;
    }
}

// Chatbot Assistant
const chatToggle = document.getElementById('gv-chat-toggle');
const chatWindow = document.getElementById('gv-chat-window');
const chatClose = document.getElementById('gv-chat-close');
const chatForm = document.getElementById('gv-chat-form');
const userInput = document.getElementById('gv-user-input');
const chatMessages = document.getElementById('gv-chat-messages');

if (chatToggle && chatWindow) {
    chatToggle.addEventListener('click', () => { chatWindow.classList.toggle('gv-hidden'); });
    if (chatClose) chatClose.addEventListener('click', () => { chatWindow.classList.add('gv-hidden'); });

    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = userInput.value.trim();
            if (!text) return;

            appendMsg(text, 'gv-user-msg');
            userInput.value = '';

            setTimeout(() => {
                let botReply = "I can help with sizes, orders, and products! Explore our Shop page or checkout your cart.";
                const lower = text.toLowerCase();
                if (lower.includes('price') || lower.includes('cost')) {
                    botReply = "Our staple tees start at $78, and premium cotton items are $139.";
                } else if (lower.includes('ship') || lower.includes('delivery')) {
                    botReply = "We provide free express delivery across Dhaka and campus regions!";
                } else if (lower.includes('contact') || lower.includes('location')) {
                    botReply = "We are located at Green University of Bangladesh campus, Dhaka. Reach us at +880 1889604070.";
                }
                appendMsg(botReply, 'gv-bot-msg');
            }, 500);
        });
    }
}

function appendMsg(text, className) {
    if (!chatMessages) return;
    const msg = document.createElement('div');
    msg.className = `gv-msg ${className}`;
    msg.innerText = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}