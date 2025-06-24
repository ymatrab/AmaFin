document.addEventListener('DOMContentLoaded', function () {
    const table = $('#bank-table').DataTable({
      pageLength: 10,
      dom: 'Bfrtip',
      buttons: [
        {
          extend: 'colvis',
          text: 'Afficher/Masquer Colonnes'
        }
      ],
      language: {
        search: "Rechercher :",
        lengthMenu: "Afficher _MENU_ lignes",
        info: "Affichage _START_ à _END_ de _TOTAL_ entrées",
        paginate: {
          first: "Premier", last: "Dernier", next: "Suivant", previous: "Précédent"
        },
        zeroRecords: "Aucune banque trouvée",
        infoEmpty: "Aucun enregistrement",
        buttons: {
          colvis: 'Afficher/Masquer Colonnes'
        }
      },

    });

    yadcf.init(table, [
        { column_number: 0, filter_type: "select" },  // Banque
      ]);
  });
  
  document.addEventListener('DOMContentLoaded', function () {
    const table = $('#incomes-table').DataTable({
      pageLength: 10,
      dom: 'Bfrtip',
      buttons: [
        {
          extend: 'colvis',
          text: 'Afficher/Masquer Colonnes'
        }
      ],
      language: {
        search: "Rechercher :",
        lengthMenu: "Afficher _MENU_ lignes",
        info: "Affichage _START_ à _END_ de _TOTAL_ entrées",
        paginate: {
          first: "Premier", last: "Dernier", next: "Suivant", previous: "Précédent"
        },
        zeroRecords: "Aucune banque trouvée",
        infoEmpty: "Aucun enregistrement",
        buttons: {
          colvis: 'Afficher/Masquer Colonnes'
        }
      },

    });

    yadcf.init(table, [
        { column_number: 2, filter_type: "select" }, 
        { column_number: 3, filter_type: "select" }, 
        { column_number: 4, filter_type: "select" },  
      ]);
  });
  