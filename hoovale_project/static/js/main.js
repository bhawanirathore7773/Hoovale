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
    initializeFastNavigation();
    initializePageTransitions();
    initializeProductEnquiry();
    initializeContactForm();
    initializeProductFilters();
    initializeProductCardLinks();
});

/**
 * Highlight active menu item based on current page
 */
function initializeMenuHighlight() {
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        const normalizedHref = href ? href.replace(/\/$/, '') || '/' : '';
        const normalizedLocation = currentLocation.replace(/\/$/, '') || '/';
        link.classList.toggle('active', normalizedHref === normalizedLocation);
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
 * Fast same-site navigation
 *
 * Starts fetching important pages before the user taps them. This is
 * especially useful on mobile and on Render's free tier where a sleeping
 * instance can make the first request feel slow.
 */
function initializeFastNavigation() {
    const links = document.querySelectorAll(
        'a[href]:not([target="_blank"]):not([download]):not([href^="#"]):not([href^="mailto:"]):not([href^="tel:"])'
    );

    const prefetched = new Set();

    function isSameOriginPage(link) {
        try {
            const url = new URL(link.href, window.location.href);
            return (
                url.origin === window.location.origin &&
                url.pathname !== window.location.pathname &&
                !url.pathname.startsWith('/admin') &&
                !url.pathname.startsWith('/media/') &&
                !url.pathname.startsWith('/static/')
            );
        } catch (error) {
            return false;
        }
    }

    function prefetch(link) {
        if (!link || !isSameOriginPage(link)) return;

        const url = new URL(link.href, window.location.href);
        const key = url.href;

        if (prefetched.has(key)) return;
        prefetched.add(key);

        const prefetchLink = document.createElement('link');
        prefetchLink.rel = 'prefetch';
        prefetchLink.href = url.href;
        prefetchLink.as = 'document';
        prefetchLink.fetchPriority = 'low';
        document.head.appendChild(prefetchLink);
    }

    links.forEach(link => {
        link.addEventListener('mouseenter', () => prefetch(link), { passive: true });
        link.addEventListener('focus', () => prefetch(link), { passive: true });
        link.addEventListener('touchstart', () => prefetch(link), {
            passive: true,
            once: true
        });
    });

    // These are the most frequently used mobile destinations.
    ['/products/', '/categories/'].forEach(path => {
        const link = document.querySelector('a[href="' + path + '"]');
        if (link) prefetch(link);
    });
}

/**
 * Add a lightweight page transition so navigation feels intentional instead
 * of showing a sudden white flash while the next Django page loads.
 */
function initializePageTransitions() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    document.addEventListener('click', function(event) {
        const link = event.target.closest('a[href]');
        if (!link || event.defaultPrevented) return;
        if (link.target === '_blank' || link.hasAttribute('download')) return;
        if (link.href.startsWith('mailto:') || link.href.startsWith('tel:')) return;

        let url;
        try {
            url = new URL(link.href, window.location.href);
        } catch (error) {
            return;
        }

        if (url.origin !== window.location.origin) return;
        if (url.pathname === window.location.pathname && !url.hash) return;
        if (url.pathname.startsWith('/admin') || url.pathname.startsWith('/media/')) return;

        document.body.classList.add('hv-page-leaving');
    }, { passive: true });
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

/* ============================================================
   PRODUCT FILTER DRAWER
   ============================================================ */
function initializeProductFilters() {
    const toggle = document.getElementById('productsFilterToggle');
    const drawer = document.getElementById('productsFilterDrawer');
    const backdrop = document.getElementById('productsFilterBackdrop');
    const close = document.getElementById('productsFilterClose');
    if (!toggle || !drawer || !backdrop) return;
    if (toggle.dataset.hvFilterBound === '1') return;

    toggle.dataset.hvFilterBound = '1';

    const setOpen = (open) => {
        document.body.classList.toggle('hv-filter-open', open);
        drawer.setAttribute('aria-hidden', String(!open));
        backdrop.setAttribute('aria-hidden', String(!open));
        toggle.setAttribute('aria-expanded', String(open));
    };

    toggle.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        setOpen(true);
    });

    backdrop.addEventListener('click', function(event) {
        event.preventDefault();
        setOpen(false);
    });

    close?.addEventListener('click', function(event) {
        event.preventDefault();
        setOpen(false);
    });

    drawer.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => setOpen(false));
    });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && document.body.classList.contains('hv-filter-open')) {
            setOpen(false);
        }
    });
}


function initializeProductPriceRange() {
    const slider = document.getElementById('dualPriceSlider');
    const minRange = document.getElementById('minPriceRange');
    const maxRange = document.getElementById('maxPriceRange');
    const minInput = document.getElementById('minPriceInput');
    const maxInput = document.getElementById('maxPriceInput');
    const minOutput = document.getElementById('minPriceOutput');
    const maxOutput = document.getElementById('maxPriceOutput');
    const fill = document.getElementById('dualPriceFill');
    const form = document.getElementById('productsFilterForm');
    if (!slider || !minRange || !maxRange || !minInput || !maxInput) return;
    if (slider.dataset.bound === '1') return;
    slider.dataset.bound = '1';

    const min = Number(slider.dataset.min || minRange.min || 0);
    const max = Number(slider.dataset.max || maxRange.max || 0);
    const step = Number(minRange.step || 10);
    const clamp = v => Math.min(max, Math.max(min, Number(v) || min));

    const sync = source => {
        let lo = clamp(minRange.value);
        let hi = clamp(maxRange.value);
        if (lo > hi) {
            if (source === 'min') lo = hi;
            else hi = lo;
        }
        minRange.value = lo;
        maxRange.value = hi;
        minInput.value = lo === min ? '' : Math.round(lo);
        maxInput.value = hi === max ? '' : Math.round(hi);
        if (minOutput) minOutput.textContent = Math.round(lo).toLocaleString('en-IN');
        if (maxOutput) maxOutput.textContent = Math.round(hi).toLocaleString('en-IN');
        const span = Math.max(1, max - min);
        const left = ((lo - min) / span) * 100;
        const right = ((hi - min) / span) * 100;
        if (fill) {
            fill.style.left = left + '%';
            fill.style.right = (100 - right) + '%';
        }
    };

    minRange.addEventListener('input', () => sync('min'));
    maxRange.addEventListener('input', () => sync('max'));

    minInput.addEventListener('input', () => {
        if (minInput.value === '') { minRange.value = min; sync('min'); return; }
        minRange.value = clamp(Math.round(Number(minInput.value) / step) * step);
        sync('min');
    });
    maxInput.addEventListener('input', () => {
        if (maxInput.value === '') { maxRange.value = max; sync('max'); return; }
        maxRange.value = clamp(Math.round(Number(maxInput.value) / step) * step);
        sync('max');
    });

    document.querySelectorAll('[data-reset-group="price"]').forEach(btn => {
        btn.addEventListener('click', () => {
            minRange.value = min;
            maxRange.value = max;
            minInput.value = '';
            maxInput.value = '';
            sync();
        });
    });

    document.querySelectorAll('[data-reset-group="category"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const radio = document.querySelector('input[name="category"][value=""]');
            if (radio) radio.checked = true;
        });
    });
    document.querySelectorAll('[data-reset-group="badge"]').forEach(btn => {
        btn.addEventListener('click', () => document.querySelectorAll('input[name="badge"]').forEach(i => i.checked = false));
    });
    document.querySelectorAll('[data-reset-group="availability"]').forEach(btn => {
        btn.addEventListener('click', () => document.querySelectorAll('input[name="availability"]').forEach(i => i.checked = false));
    });

    const updateCount = () => {
        let count = 0;
        if (document.querySelector('input[name="category"]:checked')?.value) count++;
        if (minInput.value || maxInput.value) count++;
        if (document.querySelector('input[name="badge"]:checked')) count++;
        if (document.querySelector('input[name="availability"]:checked')) count++;
        const sort = document.querySelector('select[name="sort"]')?.value;
        if (sort && sort !== 'featured') count++;
        const apply = document.getElementById('filterApplyButton');
        if (apply) apply.textContent = count ? `Apply Filters(${count})` : 'Apply Filters';
    };
    form?.addEventListener('input', updateCount);
    form?.addEventListener('change', updateCount);
    sync();
    updateCount();
}

/* Fallback delegated handler:
   keeps the mobile filter working even if the page is restored from cache
   or another script initializes after the normal DOM-ready pass. */
if (!window.__hoovaleFilterDelegationBound) {
    window.__hoovaleFilterDelegationBound = true;

    document.addEventListener('click', function(event) {
        const toggle = event.target.closest('#productsFilterToggle');
        if (toggle) {
            const drawer = document.getElementById('productsFilterDrawer');
            const backdrop = document.getElementById('productsFilterBackdrop');
            if (!drawer || !backdrop) return;

            event.preventDefault();
            event.stopPropagation();

            document.body.classList.add('hv-filter-open');
            drawer.setAttribute('aria-hidden', 'false');
            backdrop.setAttribute('aria-hidden', 'false');
            toggle.setAttribute('aria-expanded', 'true');
            return;
        }

        if (event.target.closest('#productsFilterClose, #productsFilterBackdrop')) {
            const drawer = document.getElementById('productsFilterDrawer');
            const backdrop = document.getElementById('productsFilterBackdrop');
            const toggle = document.getElementById('productsFilterToggle');

            document.body.classList.remove('hv-filter-open');
            drawer?.setAttribute('aria-hidden', 'true');
            backdrop?.setAttribute('aria-hidden', 'true');
            toggle?.setAttribute('aria-expanded', 'false');
        }
    }, true);
}

/* ============================================================
   PRODUCT CARD KEYBOARD NAVIGATION
   ============================================================ */
function initializeProductCardLinks() {
    document.querySelectorAll('.product-card-link[role="link"]').forEach(card => {
        if (card.dataset.hvCardBound === '1') return;
        card.dataset.hvCardBound = '1';
        card.addEventListener('keydown', event => {
            if ((event.key === 'Enter' || event.key === ' ') && !event.target.closest('a,button')) {
                event.preventDefault();
                const url = card.dataset.productUrl;
                if (url) window.location.href = url;
            }
        });
    });
}

/* ============================================================
   CONTACT ENQUIRY FORM
   Works after instant page swaps as well as normal page loads.
   ============================================================ */
function initializeContactForm() {
    const form = document.getElementById('contactForm');
    if (!form || form.dataset.hvContactBound === '1') return;

    form.dataset.hvContactBound = '1';
    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const responseDiv = document.getElementById('formResponse');
        const submitBtn = form.querySelector('button[type="submit"]');
        if (!submitBtn) return;

        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            });
            const data = await response.json();

            if (response.ok && data.success) {
                if (responseDiv) {
                    responseDiv.innerHTML =
                        '<div class="alert alert-success"> <i class="fas fa-check-circle"></i> ' +
                        (data.message || 'Enquiry sent successfully!') +
                        ' We will contact you soon.</div>';
                }
                form.reset();
            } else {
                if (responseDiv) {
                    responseDiv.innerHTML =
                        '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> ' +
                        (data.error || 'Please check the details and try again.') +
                        '</div>';
                }
            }
        } catch (error) {
            if (responseDiv) {
                responseDiv.innerHTML =
                    '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> ' +
                    'Network error. Please WhatsApp us directly.</div>';
            }
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

