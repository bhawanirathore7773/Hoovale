/**
 * HOOVALE - Premium Wall Clock Brand
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeMenuHighlight();
    initializeBottomNav();
    initializeLazyLoading();
    initializeSmoothScroll();
    initializeFormValidation();
});

/**
 * Highlight active menu item based on current page
 */
function initializeMenuHighlight() {
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
}

/**
 * Lazy load images for better performance
 */
function initializeBottomNav() {
    const items = document.querySelectorAll('[data-bottom-nav]');
    if (!items.length) return;

    const path = window.location.pathname.replace(/\/$/, '') || '/';

    items.forEach(item => {
        const type = item.dataset.bottomNav;
        const isHome = type === 'home' && path === '/';
        const isProducts = type === 'products' && path.startsWith('/products');
        const isCategories = type === 'categories' && path.startsWith('/categories');
        const isContact = type === 'contact' && path === '/contact';
        const isAbout = type === 'about' && path === '/about';
        item.classList.toggle('active', isHome || isProducts || isCategories || isContact || isAbout);
    });
}


function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

/**
 * Smooth scroll behavior for anchor links
 */
function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Simple form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Utility function to format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

/**
 * Add to cart functionality (for future use)
 */
function addToCart(productId) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        const currentCount = parseInt(cartCount.textContent) || 0;
        cartCount.textContent = currentCount + 1;
    }
}

/**
 * Handle scroll position for sticky header
 */
window.addEventListener('scroll', function() {
    const header = document.querySelector('.sticky-header');
    if (window.scrollY > 50) {
        header?.classList.add('scrolled');
    } else {
        header?.classList.remove('scrolled');
    }
});

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Search products dynamically
 */
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function(e) {
        const query = this.value.trim();
        if (query.length > 2) {
            // Could trigger live search here
            console.log('Searching for:', query);
        }
    }, 300));
}

/**
 * Initialize tooltips (if using Bootstrap tooltips)
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Handle responsive navigation
 */
function setupResponsiveNav() {
    const toggler = document.getElementById('hvMenuToggle');
    const drawer = document.getElementById('nav');
    const overlay = document.getElementById('hvMenuOverlay');
    const closeButton = document.getElementById('hvMenuClose');

    if (!toggler || !drawer) return;

    // Keep Bootstrap's collapse class from fighting the custom drawer.
    drawer.classList.remove('show');

    const isMobile = () => window.matchMedia('(max-width: 991px)').matches;

    function setMenu(open) {
        if (!isMobile()) open = false;

        drawer.classList.toggle('is-open', open);
        drawer.classList.remove('show');
        overlay?.classList.toggle('is-visible', open);
        toggler.classList.toggle('is-open', open);
        toggler.setAttribute('aria-expanded', String(open));
        toggler.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
        overlay?.setAttribute('aria-hidden', String(!open));
        document.body.classList.toggle('hv-menu-open', open);
    }

    // Remove duplicate handlers if this initializer is ever called again.
    if (toggler.dataset.hvNavBound === 'true') return;
    toggler.dataset.hvNavBound = 'true';

    toggler.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        setMenu(!drawer.classList.contains('is-open'));
    });

    closeButton?.addEventListener('click', () => setMenu(false));
    overlay?.addEventListener('click', () => setMenu(false));

    drawer.querySelectorAll('.nav-link, .nav-item .btn').forEach(link => {
        link.addEventListener('click', () => setMenu(false));
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') setMenu(false);
    });

    window.addEventListener('resize', () => {
        if (!isMobile()) setMenu(false);
    });

    setMenu(false);
}

// Initialize responsive navigation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupResponsiveNav);
} else {
    setupResponsiveNav();
}

/**
 * Price formatter for display
 */
function displayPrice(price) {
    if (!price) return 'Contact for Price';
    return '₹' + parseFloat(price).toLocaleString('en-IN', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Press '/' to focus search
    if (e.key === '/' && searchInput) {
        e.preventDefault();
        searchInput.focus();
    }
    // Press 'Esc' to close modals
    if (e.key === 'Escape') {
        const modal = bootstrap.Modal.getOrCreateInstance(document.querySelector('.modal.show'));
        if (modal) modal.hide();
    }
});

/**
 * Performance monitoring
 */
if (window.performance && window.performance.timing) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const timing = window.performance.timing;
            const loadTime = timing.loadEventEnd - timing.navigationStart;
            console.log('Page load time:', loadTime + 'ms');
        }, 0);
    });
}

/**
 * Service Worker registration for PWA (optional)
 */
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/static/js/service-worker.js');
    });
}

/**
 * Export functions for global use
 */
window.HOOVALE = {
    formatCurrency,
    addToCart,
    debounce,
    displayPrice
};
