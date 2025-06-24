from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_view, name='home'),
    path("factures/", views.factures, name="factures"),
    path("table/", views.InvoiceListView.as_view()),

    path("banks/", views.bankView, name="bank-table"),
    path("banks/edit/<int:pk>/", views.bank_edit_view, name="bank-edit"),
    
    path("fx/", views.fx_table_view, name="fx-table"),
    path("fx/edit/<int:pk>/", views.fx_edit_view, name="fx-edit"),
    path("fx/delete/<int:pk>/", views.fx_delete_view, name="fx-delete"),
    path("fx/new/ajax/", views.fx_create_ajax, name="fx-create-ajax"),

    
    path("incomes/", views.incomes_table_view, name="incomes-table"),
    path("incomes/edit/<int:pk>/", views.incomes_edit_view, name="incomes-edit"),
    path("incomes/delete/<int:pk>/", views.incomes_delete_view, name="incomes-delete"),
    path("incomes/new/ajax/", views.incomes_create_ajax, name="incomes-create-ajax"),


    path("achats/", views.achat_table_view, name="achat-table"),
    path("achats/edit/<int:pk>/", views.achat_edit_view, name="achat-edit"),
    path("achats/delete/<int:pk>/", views.achat_delete_view, name="achat-delete"),
    path("achat/new/ajax/", views.achat_create_ajax, name="achat-create-ajax"),


    path("engags/", views.achat_table_view, name="engags-table"),
    path("engags/edit/<int:pk>/", views.achat_edit_view, name="engags-edit"),
    path("engags/delete/<int:pk>/", views.achat_delete_view, name="engags-delete"),

    path("impots/", views.impots_table_view, name="impots-table"),
    path("impots/edit/<int:pk>/", views.impots_edit_view, name="impots-edit"),
    path("impots/delete/<int:pk>/", views.impots_delete_view, name="impots-delete"),
    path("impots/new/ajax/", views.impots_create_ajax, name="impots-create-ajax"),
        
    path("salaires/", views.salaires_table_view, name="salaires-table"),
    path("salaires/edit/<int:pk>/", views.salaires_edit_view, name="salaires-edit"),
    path("salaires/delete/<int:pk>/", views.salaires_delete_view, name="salaires-delete"),
    path("salaires/new/ajax/", views.salaires_create_ajax, name="salaires-create-ajax"),

    path("financement/", views.financement_table_view, name="financement-table"),
    path("financement/edit/<int:pk>/", views.financement_edit_view, name="financement-edit"),
    path("financement/delete/<int:pk>/", views.financement_delete_view, name="financement-delete"),
    path("financement/new/ajax/", views.financement_create_ajax, name="financement-create-ajax"),

    path("escomptes/", views.escompte_table_view, name="escompte-table"),
    path("escomptes/edit/<int:pk>/", views.escompte_edit_view, name="escompte-edit"),
    path("escomptes/delete/<int:pk>/", views.escompte_delete_view, name="escompte-delete"),
    path("escompte/new/ajax/", views.escompte_create_ajax, name="escompte-create-ajax"),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]
