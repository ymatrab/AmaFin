document.addEventListener('DOMContentLoaded', function () {
    // Lire les données Django injectées
    const dataContainer = document.getElementById('data-container');
    const series = JSON.parse(dataContainer.dataset.series);
    const categories = JSON.parse(dataContainer.dataset.categories);
    const weeklySeries = JSON.parse(dataContainer.dataset.weeklyseries);
    const weeklyCategories = JSON.parse(dataContainer.dataset.weeklycategories);
  
    // // 📈 Chart vertical groupé
    // const groupedChart = new ApexCharts(document.querySelector("#achatGroupedChart"), {
    //     series: weeklySeries,
    //     chart: {
    //       type: 'bar',
    //       height: 360,
    //       stacked: true,
    //       toolbar: {
    //         show: true
    //       },
    //       zoom: {
    //         enabled: true
    //       }
    //     },
    //     responsive: [{
    //       breakpoint: 480,
    //       options: {
    //         legend: {
    //           position: 'bottom',
    //           offsetX: -10,
    //           offsetY: 0
    //         }
    //       }
    //     }],
    //     plotOptions: {
    //       bar: {
    //         horizontal: false,
    //         borderRadius: 5,
    //         borderRadiusApplication: 'end',
    //         borderRadiusWhenStacked: 'last',
    //         dataLabels: {
    //           total: {
    //             enabled: false,
    //             style: {
    //               fontSize: '13px',
    //               fontWeight: 900
    //             }
    //           }
    //         }
    //       }
    //     },
    //     dataLabels: {
    //         enabled: true,
    //         formatter: function (val) {
    //           return val.toFixed(2) + ' M';
    //         },
    //         style: {
    //           fontSize: '12px',
    //           colors: ['#000']
    //         }
    //       },
    //     xaxis: {
    //       type: 'category',
    //       categories: weeklyCategories,
    //       labels: {
    //         rotate: -45 , // meilleure lisibilité des dates
    //         style: {
    //             fontSize: '12px',
    //             fontFamily: 'inherit',
    //             colors: []
    //           }
    //       }
    //     },
    //     yaxis: {
    //       labels: {
    //         formatter: val => val.toFixed(2) + ' M'
    //       },
    //       title: {
    //         text: 'Montant (en Millions DHS)'
    //       }
    //     },
    //     legend: {
    //       position: 'right',
    //       offsetY: 40
    //     },
    //     tooltip: {
    //       y: {
    //         formatter: val => val.toFixed(2) + ' M DHS'
    //       }
    //     },
    //     fill: {
    //       opacity: 1
    //     },
    //     colors: ['#2a9fd6', '#f39c12', '#16a085']
    //   });
      
    //   groupedChart.render();
      
    const groupedChart = new ApexCharts(document.querySelector("#achatGroupedChart"), {
  series: weeklySeries,
  chart: {
    type: 'bar',
    height: 400,
    stacked: true,
    toolbar: { show: true },
    zoom: { enabled: true }
  },
  responsive: [{
    breakpoint: 480,
    options: {
      legend: {
        position: 'bottom',
        offsetX: -10,
        offsetY: 0
      }
    }
  }],
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 6,
      borderRadiusApplication: 'end',
      borderRadiusWhenStacked: 'last'
    }
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return val.toFixed(2) + ' M';
    },
    style: {
      fontSize: '12px',
      colors: ['#000']
    }
  },
  xaxis: {
    type: 'category',
    categories: weeklyCategories,
    labels: {
      rotate: -45,
      style: {
        fontSize: '12px',
        fontFamily: 'Inter, sans-serif',
        colors: []
      }
    }
  },
  yaxis: {
    labels: {
      formatter: val => val.toFixed(2) + ' M'
    },
    title: {
      text: 'Montant (en Millions DHS)'
    }
  },
  legend: {
    position: 'bottom',
    horizontalAlign: 'center',
    fontSize: '14px',
    fontWeight: 500,
    markers: {
      width: 12,
      height: 12,
      radius: 4
    },
    itemMargin: {
      horizontal: 10,
      vertical: 5
    }
  },
  tooltip: {
    y: {
      formatter: val => val.toFixed(2) + ' M DHS'
    }
  },
  fill: {
    opacity: 0.8
  },
colors: [
  'rgba(0, 123, 255, 0.7)',    // Bleu vif Enosis
  'rgba(255, 166, 0, 0.7)',    // Orange Enosis
  'rgba(100, 100, 100, 0.3)'   // Gris neutre ou fond discret
]
});

groupedChart.render();

      
  
    // 📉 Chart horizontal empilé
    const stackedChart = new ApexCharts(document.querySelector("#achatStackedChart"), {
      series: series,
      chart: { type: 'bar', height: 400, stacked: true },
      plotOptions: {
        bar: {
          horizontal: true,
          dataLabels: {
            total: {
              enabled: true,
              offsetX: 0,
              style: { fontSize: '13px', fontWeight: 600 }
            }
          }
        }
      },
      dataLabels: {
        enabled: true,
        formatter: function (val) {
          return val.toFixed(2) + ' M';
        },
        style: {
          fontSize: '12px',
          colors: ['#000']
        }
      },
      stroke: { width: 1, colors: ['#fff'] },
      xaxis: {
        categories: categories,
        labels: { formatter: val => val.toFixed(2) + " M" }
      },
      yaxis: { title: { text: 'Date' } },
      tooltip: { y: { formatter: val => val.toFixed(2) + " M DHS" } },
      fill: { opacity: 1 },
      legend: { position: 'top', horizontalAlign: 'center', offsetX: 40 },
colors: [
  'rgba(0, 123, 255, 0.7)',    // Bleu vif Enosis
  'rgba(255, 166, 0, 0.7)',    // Orange Enosis
  'rgba(100, 100, 100, 0.3)'   // Gris neutre ou fond discret
]


    });
    stackedChart.render();
  
    // 🧾 Initialise DataTables
    $(document).ready(function () {
        $('#table-top-achats').DataTable({
        pageLength: 7,
        order: [[2, 'desc']],
        language: {
            search: "Rechercher :",
            lengthMenu: "Afficher _MENU_ lignes",
            info: "Affichage _START_ à _END_ de _TOTAL_ entrées",
            paginate: {
            first: "Premier", last: "Dernier", next: "Suivant", previous: "Précédent"
            },
            zeroRecords: "Aucun fournisseur trouvé",
            infoEmpty: "Aucun enregistrement"
        }
        });
  
    // ⚙️ Lecture des données fixes Django
    const finexData = JSON.parse(dataContainer.dataset.finex); // Tableau de 2 objets
  
    // 🎯 Donut 1
    const chart1 = new ApexCharts(document.querySelector("#donutChart1"), {
      chart: {
        type: 'donut',
        height: 340,
        foreColor: '#000'
      },
      series: [
        finexData[0].montant_consomme,
        finexData[0].montant_planifie,
        finexData[0].limit_finex - finexData[0].montant_consomme - finexData[0].montant_planifie
      ],
      labels: ['Consommé', 'Planifié', 'Disponible'],
      title: {
        text: 'Finex',
        align: 'center',
        style: { fontSize: '16px', color: '#fff' }
      },
      tooltip: {
        y: {
          formatter: val => val.toFixed(2) + " DHS"
        },
        style: {
          fontSize: '14px'
        }
      },
      colors: ['#56DFCF', '#FFB823','#FF3FF3'],
      legend: {
        position: 'bottom',
        labels: { colors: ['#000'] }
      },
      dataLabels: {
        enabled: true,
        formatter: val => val.toFixed(1) + '%',
        style: {
          fontSize: '14px',
          colors: ['#000']
        }
      },
      plotOptions: {
        pie: {
          donut: {
            size: '65%'
          },
          expandOnClick: false,
          offsetY: 0,
          dataLabels: {
            offset: 0,
            minAngleToShowLabel: 10
          }
        }
      },
      stroke: {
        show: false
      }
    });
    chart1.render();
  
    // 🎯 Donut 2
    const chart2 = new ApexCharts(document.querySelector("#donutChart2"), {
      chart: {
        type: 'donut',
        height: 340,
        foreColor: '#000'
      },
      series: [
        finexData[1].montant_consomme,
        finexData[1].montant_planifie,
        finexData[1].limit_finex - finexData[1].montant_consomme - finexData[1].montant_planifie
      ],
      labels: ['Consommé','Planifié', 'Disponible'],
      title: {
        text: 'Finex',
        align: 'center',
        style: { fontSize: '16px', color: '#fff' }
      },
      tooltip: {
        y: {
          formatter: val => val.toFixed(2) + " DHS"
        },
        style: {
          fontSize: '14px'
        }
      },
      colors: ['#ED3500', '#FFA673','#687FE5'],
      legend: {
        position: 'bottom',
        labels: { colors: ['#000'] }
      },
      dataLabels: {
        enabled: true,
        formatter: val => val.toFixed(1) + '%',
        style: {
          fontSize: '14px',
          colors: ['#000']
        }
      },
      plotOptions: {
        pie: {
          donut: {
            size: '65%'
          },
          expandOnClick: false,
          offsetY: 0,
          dataLabels: {
            offset: 0,
            minAngleToShowLabel: 10
          }
        }
      },
      stroke: {
        show: false
      }
    });
    chart2.render();
  });
});