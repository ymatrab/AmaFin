function togglePaymentFields() {
    const paymentField = document.getElementById('id_payment_type');
    if (!paymentField) return;

    const all = [
            'priority','debit', 'date_debit',
            'Finex','date_paiement_fournisseur', 'nb_jours_finex', 'date_echeance_finex','statut_finex','interet','refine_used',
            'numero_effet', 'date_echeance_effet'
        ];

    all.forEach(id => {
        const row = document.getElementById('id_' + id)?.closest('.col-md-12');
        if (row) row.style.display = 'none';
    });

    const showFields = {
            courant: ['priority','debit', 'date_debit'],
            finex: ['Finex','date_paiement_fournisseur', 'nb_jours_finex', 'date_echeance_finex','statut_finex','interet','refine_used'],
            effet: ['numero_effet','priority','debit', 'date_debit']
        };

    const val = paymentField.value;
    (showFields[val] || []).forEach(id => {
        const row = document.getElementById('id_' + id)?.closest('.col-md-12');
        if (row) row.style.display = '';
    });

    // Ensure this isn't bound multiple times
    paymentField.removeEventListener('change', togglePaymentFields);
    paymentField.addEventListener('change', togglePaymentFields);
}



document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".show-edit-form");
    const formContainer = document.getElementById("achat-form-container");

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
          togglePaymentFields(); 


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
  });
