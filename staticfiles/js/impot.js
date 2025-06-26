function toggleImpotFields() {
    const typeField = document.getElementById('id_type_impot');
    if (!typeField) return;

    const all = [
        'societe', 'banque', 'document', 'fournisseurs',
        'numero_facture', 'due_date', 'montant', 'devise',
        'montant_dhs', 'commentaire', 'statut_paiement',
        'date_echeance', 'taux_change'
    ];

    all.forEach(id => {
        const row = document.getElementById('id_' + id)?.closest('.col-md-3, .col-md-4');
        if (row) row.style.display = 'none';
    });

    const showFields = {
        tva: ['societe', 'montant', 'devise', 'montant_dhs', 'due_date', 'statut_paiement'],
        ir: ['societe', 'fournisseurs', 'montant', 'devise', 'montant_dhs', 'due_date'],
        is: ['societe', 'banque', 'montant', 'devise', 'montant_dhs', 'date_echeance'],
        cotisation: ['societe', 'numero_facture', 'montant', 'devise', 'montant_dhs', 'commentaire']
    };

    const val = typeField.value;
    (showFields[val] || all).forEach(id => {
        const row = document.getElementById('id_' + id)?.closest('.col-md-3, .col-md-4');
        if (row) row.style.display = '';
    });

    // Ensure this isn't bound multiple times
    typeField.removeEventListener('change', toggleImpotFields);
    typeField.addEventListener('change', toggleImpotFields);
}

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".show-edit-form");
    const formContainer = document.getElementById("impot-form-container");

    buttons.forEach(btn => {
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

                // ⬅️ Inject the toggle logic here
                toggleImpotFields();

                const cancelBtn = document.getElementById("cancel-edit");
                if (cancelBtn) {
                    cancelBtn.addEventListener("click", function (e) {
                        console.log("Cancel button clicked");
                        e.preventDefault();
                        formContainer.style.display = "none";
                        formContainer.innerHTML = "";
                    });
                }
            });
        });
    });

    // Handle add new impot button
    const addBtn = document.getElementById("add-impot-btn");
    if (addBtn) {
        addBtn.addEventListener("click", function () {
            const url = this.dataset.url;
            
            fetch(url, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
            .then(res => res.json())
            .then(data => {
                formContainer.innerHTML = data.form_html;
                formContainer.style.display = "block";
                formContainer.scrollIntoView({ behavior: "smooth" });

                toggleImpotFields();
                const cancelBtn = document.getElementById("cancel-edit");
                if (cancelBtn) {
                    cancelBtn.addEventListener("click", function (e) {
                        console.log("Cancel button clicked");
                        e.preventDefault();
                        formContainer.style.display = "none";
                        formContainer.innerHTML = "";
                    });
                }
            });
        });
    }
});
