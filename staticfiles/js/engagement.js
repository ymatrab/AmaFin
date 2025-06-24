document.addEventListener("DOMContentLoaded", function () {
    
    // **Edit Form Functionality**
    const editButtons = document.querySelectorAll(".show-edit-form");
    const formContainer = document.getElementById("achat-form-container");

    if (editButtons.length > 0 && formContainer) {
        editButtons.forEach(btn => {
            btn.addEventListener("click", function () {
                const url = this.dataset.url;

                fetch(url, {
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                .then(res => res.json())
                .then(data => {
                    formContainer.innerHTML = data.form_html;
                    formContainer.style.display = "block";
                    formContainer.scrollIntoView({ behavior: "smooth" });

                    // Inject the toggle logic here
                    togglePaymentFields();

                    const cancelBtn = document.getElementById("cancel-edit");
                    if (cancelBtn) {
                        cancelBtn.addEventListener("click", function (e) {
                            e.preventDefault();
                            formContainer.style.display = "none";
                            formContainer.innerHTML = "";
                        });
                    }
                });
            });
        });
    }

    // **Column Toggle Functionality - Initial Hide**
    const toggleCheckboxes = document.querySelectorAll(".toggle-col");
    
    // Hide all columns initially
    toggleCheckboxes.forEach(checkbox => {
        const colClass = "col-" + checkbox.dataset.col;
        const cells = document.querySelectorAll("." + colClass);
        cells.forEach(cell => {
            cell.style.display = "none";
        });
    });

    // **Column Toggle Apply Button**
    const applyBtn = document.getElementById("applyColumnToggle");
    
    if (applyBtn) {
        applyBtn.addEventListener("click", function () {
            const checkboxes = document.querySelectorAll(".toggle-col");

            checkboxes.forEach(checkbox => {
                const colClass = "col-" + checkbox.dataset.col;
                const cells = document.querySelectorAll("." + colClass);
                cells.forEach(cell => {
                    cell.style.display = checkbox.checked ? "" : "none";
                });
            });

            // Close the dropdown programmatically
            const dropdownEl = document.getElementById('toggleColumnsBtn');
            if (dropdownEl) {
                const dropdown = bootstrap.Dropdown.getInstance(dropdownEl);
                if (dropdown) {
                    dropdown.hide();
                }
            }
        });
    }
});
