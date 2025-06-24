document.addEventListener('DOMContentLoaded', function () {
    const paymentField = document.getElementById('id_payment_type');
    if (!paymentField) return;

    function toggleFields() {
        const val = paymentField.value;

        const all = [
            'priority','debit', 'date_debit',
            'Finex','date_paiement_fournisseur', 'nb_jours_finex', 'date_echeance_finex','statut_finex','interet','refine_used',
            'numero_effet', 'date_echeance_effet'
        ];

        all.forEach(id => {
            const row = document.getElementById('id_' + id)?.closest('.form-row');
            if (row) row.style.display = 'none';
        });

        const showFields = {
            courant: ['priority','debit', 'date_debit'],
            finex: ['Finex','date_paiement_fournisseur', 'nb_jours_finex', 'date_echeance_finex','statut_finex','interet','refine_used'],
            effet: ['numero_effet','priority','debit', 'date_debit']
        };

        (showFields[val] || []).forEach(id => {
            const row = document.getElementById('id_' + id)?.closest('.form-row');
            if (row) row.style.display = '';
        });
    }

    toggleFields(); // on load
    paymentField.addEventListener('change', toggleFields); // on change
});
