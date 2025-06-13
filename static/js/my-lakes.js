// My Lakes Page JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchLakes');
    const statusFilter = document.getElementById('statusFilter');
    const sortBy = document.getElementById('sortBy');
    const lakesGrid = document.getElementById('lakesGrid');
    const lakeItems = document.querySelectorAll('.lake-item');

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', filterLakes);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterLakes);
    }
    
    if (sortBy) {
        sortBy.addEventListener('change', sortLakes);
    }

    function filterLakes() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const statusValue = statusFilter ? statusFilter.value : '';
        
        lakeItems.forEach(item => {
            const name = item.dataset.name || '';
            const location = item.dataset.location || '';
            const status = item.dataset.status || '';
            
            const matchesSearch = name.includes(searchTerm) || location.includes(searchTerm);
            const matchesStatus = !statusValue || status === statusValue;
            
            if (matchesSearch && matchesStatus) {
                item.style.display = 'block';
                item.style.animation = 'fadeIn 0.3s ease';
            } else {
                item.style.display = 'none';
            }
        });
        
        updateEmptyState();
    }

    function sortLakes() {
        if (!sortBy) return;
        
        const sortValue = sortBy.value;
        const lakesArray = Array.from(lakeItems);
        
        lakesArray.sort((a, b) => {
            switch (sortValue) {
                case 'name':
                    return (a.dataset.name || '').localeCompare(b.dataset.name || '');
                case 'created':
                    return new Date(b.dataset.created || 0) - new Date(a.dataset.created || 0);
                case 'reviews':
                    return parseInt(b.dataset.reviews || 0) - parseInt(a.dataset.reviews || 0);
                default:
                    return 0;
            }
        });
        
        // Reorder DOM elements
        if (lakesGrid) {
            lakesArray.forEach(item => {
                lakesGrid.appendChild(item);
            });
        }
    }

    function updateEmptyState() {
        const visibleItems = Array.from(lakeItems).filter(item => 
            item.style.display !== 'none'
        );
        
        let emptyState = document.querySelector('.empty-state');
        
        if (visibleItems.length === 0) {
            if (!emptyState) {
                emptyState = document.createElement('div');
                emptyState.className = 'col-12 empty-state';
                emptyState.innerHTML = `
                    <i class="fas fa-search"></i>
                    <h3>Nu s-au găsit bălți</h3>
                    <p>Încearcă să modifici criteriile de căutare sau filtrare.</p>
                `;
                if (lakesGrid) {
                    lakesGrid.appendChild(emptyState);
                }
            }
            emptyState.style.display = 'block';
        } else {
            if (emptyState) {
                emptyState.style.display = 'none';
            }
        }
    }

    // Add loading states to action buttons
    document.querySelectorAll('.btn-lake-action').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!this.classList.contains('btn-outline-success')) {
                // Don't show loading for view/edit buttons
                if (this.href && (this.href.includes('/edit') || this.href.includes('/view'))) {
                    return;
                }
                
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Se încarcă...';
                this.disabled = true;
                
                // Re-enable after 3 seconds if still on page
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 3000);
            }
        });
    });

    // Initialize filters on page load
    filterLakes();
    
    // Add smooth animations for cards
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    lakeItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(item);
    });
});
