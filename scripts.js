// Confirm before performing a delete action
function confirmDelete(message) {
    return confirm(message || "Are you sure you want to delete this?");
}

// Validate form inputs
document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll("form");
    
    forms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            let valid = true;
            const inputs = form.querySelectorAll("input[required], select[required]");
            
            inputs.forEach((input) => {
                if (!input.value.trim()) {
                    // Highlight the border red if the input is empty
                    input.style.borderColor = "red";
                    valid = false;
                } else {
                    // Reset the border color if the input is filled correctly
                    input.style.borderColor = "#ccc";
                }
            });

            // Prevent form submission if not valid
            if (!valid) {
                alert("Please fill in all required fields.");
                event.preventDefault();
            }
        });
    });
});

// Highlight table rows on hover
document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("table tr");

    rows.forEach((row) => {
        row.addEventListener("mouseenter", () => {
            // Change background color on hover
            row.style.backgroundColor = "#e8f4ff";
        });

        row.addEventListener("mouseleave", () => {
            // Reset the background color when hover ends
            row.style.backgroundColor = "";
        });
    });
});

// Add delete button confirmation
document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-button");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            if (!confirmDelete()) {
                event.preventDefault();
            }
        });
    });
});



