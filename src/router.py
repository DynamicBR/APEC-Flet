import flet as ft
from views.welcome_view import WelcomeView
from views.home_view import HomeView
from views.add_expense_view import AddExpenseView
from views.stats_view import StatsView
from views.settings_view import SettingsView

@ft.component
def AppRouter():
    """
    Mapeia automaticamente os componentes para as URLs.
    """
    return ft.Router(
        routes=[
            ft.Route(index=True, component=WelcomeView),
            ft.Route(path="welcome", component=WelcomeView),
            ft.Route(path="home", component=HomeView),
            ft.Route(path="add_expense", component=AddExpenseView),
            ft.Route(path="stats", component=StatsView),
            ft.Route(path="settings", component=SettingsView)
        ],
        manage_views=True  # Permite animações e botão de voltar no celular
    )
