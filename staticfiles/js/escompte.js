document.addEventListener("DOMContentLoaded", function () {
    const formContainer = document.getElementById("escompte-form-container");
    
    // **Edit Escompte Form Functionality**
    const editButtons = document.querySelectorAll(".show-edit-form");

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

                    setupCancelButton();
                });
            });
        });
    }

    // **Add New Escompte Functionality**
    const addEscompteBtn = document.getElementById("add-new-escompte");

    if (addEscompteBtn && formContainer) {
        addEscompteBtn.addEventListener("click", function () {
            const createUrl = this.dataset.url; // Get URL from data attribute
            
            fetch(createUrl, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
            .then(res => res.json())
            .then(data => {
                formContainer.innerHTML = data.form_html;
                formContainer.style.display = "block";
                formContainer.scrollIntoView({ behavior: "smooth" });

                setupCancelButton();
            });
        });
    }

    // **Shared Cancel Button Setup Function**
    function setupCancelButton() {
        const cancelBtn = document.getElementById("cancel-edit");
        if (cancelBtn) {
            cancelBtn.addEventListener("click", function (e) {
                e.preventDefault();
                formContainer.style.display = "none";
                formContainer.innerHTML = "";
            });
        }
    }
});
