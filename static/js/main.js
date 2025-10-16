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
// ===== IMAGE ERROR HANDLING =====
    // If an image fails to load, show a placeholder instead of broken image icon
    document.querySelectorAll('img').forEach(img => {  // Find all images on page
        img.addEventListener('error', function() {  // If image fails to load
            this.src = '/static/images/placeholder.jpg';  // Use placeholder image
            this.alt = 'Image not available';  // Update alt text for accessibility
        });
    });

    // ===== FORM SUBMISSION ENHANCEMENT =====
    // Prevent double-clicks and show loading state when forms are submitted
    const forms = document.querySelectorAll('form');  // Find all forms on page

    forms.forEach(form => {  // Set up each form
        form.addEventListener('submit', function(e) {  // When form is submitted
            const submitBtn = this.querySelector('button[type="submit"]');  // Find submit button

            if (submitBtn) {  // If we found a submit button
                submitBtn.disabled = true;  // Disable button to prevent double-submission
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';  // Show loading text
            }
        });
    });

