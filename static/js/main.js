// =================================================================
// KUMPULAN FUNGSI-FUNGSI UTAMA
// (Semua fungsi didefinisikan di sini dulu)
// =================================================================

function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container');
    const toastId = 'toast-' + Math.random().toString(36).substr(2, 9);
    const toastHeaderClass = type === 'success' ? 'bg-success text-white' : 'bg-danger text-white';

    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${toastHeaderClass}">
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>`;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    toastElement.addEventListener('hidden.bs.toast', () => toastElement.remove());
}

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

function styleAllForms() {
    document.querySelectorAll('form input, form textarea, form select').forEach(field => {
        const type = field.getAttribute('type');
        if (type !== 'submit' && type !== 'checkbox' && type !== 'radio' && type !== 'hidden' && type !== 'file') {
            field.classList.add('form-control');
        }
    });
}

function createDeleteModal(product) {
    return `
    <div class="modal fade" id="deleteModal${product.pk}" tabindex="-1">
      <div class="modal-dialog"><div class="modal-content">
          <div class="modal-header"><h5 class="modal-title">Confirm Deletion</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
          <div class="modal-body">Are you sure you want to delete "<b>${product.name}</b>"?<br>This action cannot be undone.</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger btn-confirm-delete" data-product-id="${product.pk}">Yes, Delete</button>
          </div>
      </div></div>
    </div>`;
}

function createProductCard(product, filter, currentUser) {
    let actionButtonsHtml = '';
    
    // Logika Sederhana: Cuma cek kepemilikan. Tombol muncul di mana aja kalo produknya punya lu.
    if (filter === 'my' && (currentUser && product.user && currentUser.trim() === product.user.trim())) {
        actionButtonsHtml = `
            <div class="btn-group">
                <button type="button" class="btn btn-sm btn-outline-secondary btn-edit-product" data-bs-toggle="modal" data-bs-target="#editProductModal" data-product-id="${product.pk}">Edit</button>
                <button type="button" class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteModal${product.pk}">Delete</button>
            </div>`;
    }

    return `
        <div class="col" id="product-card-${product.pk}">
            <div class="card h-100 product-card shadow-sm">
                <img src="${product.thumbnail || 'https://placehold.co/600x400?text=No+Image'}" alt="${product.name}" class="card-img-top">
                <div class="card-body d-flex flex-column">
                    <h6 class="card-subtitle mb-2"><span class="badge bg-warning text-dark">${product.category}</span></h6>
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text small text-muted">${(product.description || '').substring(0, 100)}...</p>
                    <div class="mt-auto pt-3 d-flex justify-content-between align-items-center border-top">
                        <a href="/product/${product.pk}/" class="btn btn-primary-custom">View Details</a>
                        ${actionButtonsHtml}
                    </div>
                </div>
            </div>
        </div>`;
}

async function fetchProducts(filter) {
    const productGrid = document.getElementById('product-grid');
    const loadingState = document.getElementById('loading-state');
    const currentUser = productGrid.dataset.currentUser;
    
    productGrid.innerHTML = '';
    if (loadingState) loadingState.style.display = 'block';

    const baseUrl = productGrid.dataset.getUrl;
    const url = `${baseUrl}?filter=${filter}`;
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const products = await response.json();
        
        if (loadingState) loadingState.style.display = 'none';
        
        document.querySelectorAll('.modal.fade[id^="deleteModal"]').forEach(modal => modal.remove());

        if (products.length === 0) {
            productGrid.innerHTML = `<div class="text-center py-5 col-12"><h4 class="mt-3">No Products Found</h4><p class="text-muted">There are no products to display for this filter.</p></div>`;
        } else {
            products.forEach(product => {
                const cardHtml = createProductCard(product, filter, currentUser);
                productGrid.insertAdjacentHTML('beforeend', cardHtml);
                
                if (currentUser && product.user && currentUser.trim() === product.user.trim()) {
                    const modalHtml = createDeleteModal(product);
                    document.body.insertAdjacentHTML('beforeend', modalHtml);
                }
            });
        }
    } catch (error) {
        console.error('Error fetching products:', error);
        if (loadingState) loadingState.style.display = 'none';
        productGrid.innerHTML = `<div class="alert alert-danger col-12">Failed to load products. Please try again.</div>`;
    }
}

async function addProduct(formData) {
    const csrftoken = getCookie('csrftoken');
    const addProductForm = document.getElementById('add-product-form');
    const url = addProductForm.getAttribute('action');
    try {
        const response = await fetch(url, { method: "POST", body: formData, headers: { "X-CSRFToken": csrftoken } });
        const result = await response.json();
        if (result.status === "success") {
            const modalInstance = bootstrap.Modal.getInstance(document.getElementById('addProductModal'));
            modalInstance.hide();
            fetchProducts('all'); 
            document.getElementById('all-products-btn')?.classList.add('active');
            document.getElementById('my-products-btn')?.classList.remove('active');
            addProductForm.reset();
            showToast("Product successfully added!", "success");
        } else {
            showToast("Failed to add product. Please check the form.", "danger");
        }
    } catch (error) {
        console.error("Error:", error);
        showToast("An unexpected error occurred.", "danger");
    }
}

async function deleteProduct(productId) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(`/delete/${productId}/`, { method: 'POST', headers: { 'X-CSRFToken': csrftoken } });
    if (response.ok) {
        document.getElementById(`product-card-${productId}`)?.remove();
        const modalElement = document.getElementById(`deleteModal${productId}`);
        if(modalElement) {
            const modalInstance = bootstrap.Modal.getInstance(modalElement);
            if (modalInstance) modalInstance.hide();
            modalElement.remove();
        }
        showToast('Product successfully deleted!', 'success');
    } else {
        showToast('Failed to delete product.', 'danger');
    }
}

async function getProductDetails(productId) {
    try {
        const response = await fetch(`/get-product/${productId}/`);
        if (!response.ok) throw new Error('Failed to fetch product details.');
        const result = await response.json();
        if (result.status === 'success') {
            const product = result.data;
            const editForm = document.getElementById('edit-product-form');

            // Isi setiap field di form edit
            editForm.querySelector('#id_name').value = product.name;
            editForm.querySelector('#id_price').value = product.price;
            editForm.querySelector('#id_description').value = product.description;
            editForm.querySelector('#id_category').value = product.category;
            
            // Simpan URL untuk update di atribut action form-nya
            editForm.setAttribute('action', `/update-product-ajax/${product.pk}/`);

        } else {
            showToast(result.message, 'danger');
        }
    } catch (error) {
        console.error('Error getting product details:', error);
        showToast('Could not load product data for editing.', 'danger');
    }
}

// --- FUNGSI BARU: Mengirim data update ---
async function updateProduct(formElement) {
    const url = formElement.getAttribute('action');
    const formData = new FormData(formElement);
    const csrftoken = getCookie('csrftoken');

    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": csrftoken },
        });
        const result = await response.json();

        if (result.status === "success") {
            const modalInstance = bootstrap.Modal.getInstance(document.getElementById('editProductModal'));
            modalInstance.hide();
            showToast("Product updated successfully!", 'success');
            fetchProducts('my'); // Refresh list produknya biar nampilin data baru
        } else {
            showToast("Failed to update product. Please check the form.", "danger");
        }
    } catch (error) {
        console.error("Error updating product:", error);
        showToast("An unexpected error occurred while updating.", "danger");
    }
}

async function registerUser(formElement) {
    const url = formElement.getAttribute('action');
    const formData = new FormData(formElement);
    const csrftoken = formElement.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": csrftoken },
        });
        const result = await response.json();

        if (result.status === "success") {
            showToast(result.message, 'success');
            setTimeout(() => {
                window.location.href = "/login/"; 
            }, 2000);
        } else {
            showToast("Registration failed. Please check the form.", 'danger');
        }
    } catch (error) {
        console.error("Error during registration:", error);
        showToast("An unexpected error occurred.", "danger");
    }
}

async function loginUser(formElement) {
    const url = formElement.getAttribute('action');
    const formData = new FormData(formElement);
    const data = Object.fromEntries(formData.entries());
    const csrftoken = getCookie('csrftoken');

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (result.status === "success") {
            showToast(result.message, 'success');
            // Tunggu sebentar biar toast-nya kebaca, baru redirect
            setTimeout(() => {
                window.location.href = "/"; // Arahkan ke halaman utama
            }, 1500);
        } else {
            showToast(result.message, 'danger');
        }
    } catch (error) {
        console.error("Error during login:", error);
        showToast("An unexpected error occurred.", "danger");
    }
}

// =================================================================
// EVENT LISTENERS
// =================================================================

document.addEventListener('DOMContentLoaded', function() {
    styleAllForms();

    const allProductsBtn = document.getElementById('all-products-btn');
    if (allProductsBtn) {
        allProductsBtn.addEventListener('click', () => {
            fetchProducts('all');
            allProductsBtn.classList.add('active');
            document.getElementById('my-products-btn')?.classList.remove('active');
        });
    }

    const myProductsBtn = document.getElementById('my-products-btn');
    if (myProductsBtn) {
        myProductsBtn.addEventListener('click', () => {
            fetchProducts('my');
            myProductsBtn.classList.add('active');
            document.getElementById('all-products-btn')?.classList.remove('active');
        });
    }

    const addProductForm = document.getElementById('add-product-form');
    if (addProductForm) {
        addProductForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(addProductForm);
            await addProduct(formData);
        });
    }

    const editProductForm = document.getElementById('edit-product-form');
    if (editProductForm) {
        editProductForm.addEventListener('submit', function(event) {
            event.preventDefault();
            updateProduct(editProductForm);
        });
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            await registerUser(registerForm);
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            await loginUser(loginForm);
        });
    }
    
    document.addEventListener('click', function(event) {
        if (event.target && event.target.matches('.btn-confirm-delete')) {
            const productId = event.target.getAttribute('data-product-id');
            deleteProduct(productId);
        }

        if (event.target && event.target.matches('.btn-edit-product')) {
            const productId = event.target.getAttribute('data-product-id');
            getProductDetails(productId);
        }
    });
});