// This file contains JavaScript that runs on every page of our website

// Wait until the webpage is fully loaded before running our code
document.addEventListener('DOMContentLoaded', function() {

    // ===== DROPDOWN MENUS =====
    // Make dropdown menus work when hovering over them
    const dropdowns = document.querySelectorAll('.dropdown');  // Find all dropdown elements

    dropdowns.forEach(dropdown => {  // Set up each dropdown individually
        dropdown.addEventListener('mouseenter', function() {  // When mouse enters dropdown
            this.querySelector('.dropdown-content').style.display = 'block';  // Show menu
        });

        dropdown.addEventListener('mouseleave', function() {  // When mouse leaves dropdown
            this.querySelector('.dropdown-content').style.display = 'none';  // Hide menu
        });
    });

    // ===== SEARCH FORM ENHANCEMENT =====
    // Make search forms more user-friendly
    const searchForm = document.querySelector('form[method="get"]');  // Find search forms

    if (searchForm) {  // If we found a search form on this page
        const searchInput = searchForm.querySelector('input[name="search"]');  // Get search box

        searchInput.addEventListener('keypress', function(e) {  // When user types in search
            if (e.key === 'Enter') {  // If they press Enter key
                searchForm.submit();  // Submit the form automatically
            }
        });
    }

