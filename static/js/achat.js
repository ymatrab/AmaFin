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


document.addEventListener('DOMContentLoaded', function () {
  // DataTable initialization
  $(document).ready(function () {
      const table = $('#achat-table').DataTable({
          pageLength: 20,
          dom: `
          <'datatable-toolbar d-flex justify-content-between align-items-center mb-2'
            <'left-side'B>
            <'right-side d-flex align-items-center gap-2'f <'#custom-filter-button'>>
          >
          t
          <'d-flex justify-content-between mt-2'lip>
        `,
          buttons: [
              'colvis',
              'searchPanes'
          ],
          language: {
              search: "Rechercher :",
              lengthMenu: "Afficher _MENU_ lignes",
              info: "Affichage _START_ à _END_ de _TOTAL_ entrées",
              paginate: {
                  first: "Premier", last: "Dernier", next: "Suivant", previous: "Précédent"
              },
              zeroRecords: "Aucun enregistrement trouvé",
              infoEmpty: "Aucune donnée disponible",
              buttons: {
                  colvis: 'Afficher/Masquer Colonnes',
                  searchPanes: 'Filtres'
              }
          },
          columnDefs: [
              { targets: -1, orderable: false },
              { targets: [0, 7, 8, 9, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], visible: false },
              { searchPanes: { show: true }, targets: [1, 2, 4, 5, 10, 16] }
          ]
      });

      const filters = [];

      // Colonnes à filtrer par select dropdown
      const selectColumns = [0, 1, 2, 3, 4, 5, 6, 9, 12, 13, 14, 15, 16, 18, 27, 32];
      selectColumns.forEach(i =>
          filters.push({ column_number: i, filter_type: "select" })
      );

      // Ajout du bouton avec icône filtre Bootstrap
      $('#custom-filter-button').html(`
          <button id="toggle-filters" class="btn btn-outline-secondary ms-3">
            <i class="bi bi-funnel"></i> Filtres
          </button>
      `);

      // Action du bouton pour afficher/masquer les filtres
      $('#toggle-filters').on('click', function () {
          $('.yadcf-filter-wrapper').toggle();
      });

      // Cacher les filtres au chargement initial
      $('.yadcf-filter-wrapper').hide();

      // Initialisation finale
      yadcf.init(table, filters);
  });

  // Filter toggle functionality
  const toggleBtn = document.getElementById('toggle-filters');
  let filtersVisible = false;

  if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
          const wrappers = document.querySelectorAll('.yadcf-filter-wrapper');

          filtersVisible = !filtersVisible;
          wrappers.forEach(wrapper => {
              wrapper.style.display = filtersVisible ? 'block' : 'none';
          });
      });
  }

  // Hide filters initially with delay
  setTimeout(function () {
      document.querySelectorAll('.yadcf-filter-wrapper').forEach(wrapper => {
          wrapper.style.display = 'none';
      });
      filtersVisible = false;
  }, 300);

  // **NEW: Add new achat functionality**
  const addBtn = document.getElementById("add-new-achat");
  const formContainer = document.getElementById("achat-form-container");

  if (addBtn && formContainer) {
      addBtn.addEventListener("click", function () {
          fetch("/achat/new/ajax/", {
              headers: { "X-Requested-With": "XMLHttpRequest" }
          })
          .then(res => res.json())
          .then(data => {
              formContainer.innerHTML = data.form_html;
              formContainer.style.display = "block";
              formContainer.scrollIntoView({ behavior: "smooth" });

              togglePaymentFields();  // Remet l'état initial si nécessaire

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
  }

  // **NEW: Edit achat functionality**
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
});
