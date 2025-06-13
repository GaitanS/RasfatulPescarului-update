// Solunar Calendar JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize filter controls
    initializeFilterControls();
    
    // Initialize legend toggle
    initializeLegendToggle();
});

function initializeFilterControls() {
    const filterForm = document.getElementById('solunarFilterForm');
    const monthSelect = document.getElementById('monthSelect');
    const yearSelect = document.getElementById('yearSelect');
    const infoText = document.querySelector('.filter-info small');
    
    if (!filterForm || !monthSelect || !yearSelect) return;
    
    // Handle select changes without any animation or loading indicators
    function handleSelectChange(selectElement) {
        // Submit form immediately without any visual changes
        filterForm.submit();
    }
    
    // Add event listeners
    monthSelect.addEventListener('change', function() {
        handleSelectChange(this);
    });
    
    yearSelect.addEventListener('change', function() {
        handleSelectChange(this);
    });
    
    // Prevent double submissions
    let isSubmitting = false;
    filterForm.addEventListener('submit', function(e) {
        if (isSubmitting) {
            e.preventDefault();
            return false;
        }
        isSubmitting = true;
    });
}

function initializeLegendToggle() {
    const toggleBtn = document.getElementById('toggleLegend');
    const legendContent = document.querySelector('.legend-content');
    const legendIcon = toggleBtn?.querySelector('i');
    
    if (!toggleBtn || !legendContent || !legendIcon) return;
    
    let isLegendVisible = true;

    function toggleLegend() {
        isLegendVisible = !isLegendVisible;
        legendContent.style.display = isLegendVisible ? 'block' : 'none';
        legendIcon.style.transform = isLegendVisible ? 'rotate(0deg)' : 'rotate(180deg)';
        
        // Save preference to localStorage
        localStorage.setItem('solunarLegendVisible', isLegendVisible);
    }

    // Load saved preference
    const savedPreference = localStorage.getItem('solunarLegendVisible');
    if (savedPreference !== null) {
        isLegendVisible = savedPreference === 'true';
        legendContent.style.display = isLegendVisible ? 'block' : 'none';
        legendIcon.style.transform = isLegendVisible ? 'rotate(0deg)' : 'rotate(180deg)';
    }

    toggleBtn.addEventListener('click', toggleLegend);
}

// Utility functions for solunar calendar
function formatSolunarTime(timeString) {
    // Format time for display
    const time = new Date('1970-01-01T' + timeString + 'Z');
    return time.toLocaleTimeString('ro-RO', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}

function calculateMoonPhase(date) {
    // Simple moon phase calculation
    const knownNewMoon = new Date('2000-01-06T18:14:00Z');
    const lunarCycle = 29.53058867; // days
    
    const daysSinceNewMoon = (date - knownNewMoon) / (1000 * 60 * 60 * 24);
    const phase = (daysSinceNewMoon % lunarCycle) / lunarCycle;
    
    return phase;
}

function getMoonPhaseName(phase) {
    if (phase < 0.125) return 'Lună Nouă';
    if (phase < 0.375) return 'Primul Pătrar';
    if (phase < 0.625) return 'Lună Plină';
    if (phase < 0.875) return 'Ultimul Pătrar';
    return 'Lună Nouă';
}

// Export functions for use in other scripts
window.SolunarCalendar = {
    initializeFilterControls,
    initializeLegendToggle,
    formatSolunarTime,
    calculateMoonPhase,
    getMoonPhaseName
};
