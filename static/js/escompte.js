document.addEventListener("DOMContentLoaded", function () {
    const formContainer = document.getElementById("escompte-form-container");
    
    // ✅ Init DataTable pour tableau résumé
    const escompteSummaryTable = document.getElementById("table-escompte-summary");
    if (escompteSummaryTable) {
        $(escompteSummaryTable).DataTable({
            paging: false,
            searching: false,
            info: false,
            ordering: false,
            language: {
                emptyTable: "Aucune donnée disponible",
                zeroRecords: "Aucun résultat trouvé"
            }
        });
    }

    // ✅ Init DataTable pour le tableau top achats si existant
    const topAchatsTable = document.getElementById("table-top-achats");
    if (topAchatsTable) {
        $(topAchatsTable).DataTable({
            pageLength: 7,
            order: [[2, 'desc']],
            language: {
                search: "Rechercher :",
                lengthMenu: "Afficher _MENU_ lignes",
                info: "Affichage _START_ à _END_ de _TOTAL_ entrées",
                paginate: {
                    first: "Premier",
                    last: "Dernier",
                    next: "Suivant",
                    previous: "Précédent"
                },
                zeroRecords: "Aucun fournisseur trouvé",
                infoEmpty: "Aucun enregistrement"
            }
        });
    }

    // ✅ Gestion du formulaire édition
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

    // ✅ Formulaire ajout
    const addEscompteBtn = document.getElementById("add-new-escompte");

    if (addEscompteBtn && formContainer) {
        addEscompteBtn.addEventListener("click", function () {
            const createUrl = this.dataset.url;
            
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

    // ✅ Annuler formulaire
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
