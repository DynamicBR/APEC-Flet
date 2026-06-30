import flet as ft
from views.welcome_view import WelcomeView
from views.home_view import HomeView

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
        ],
        manage_views=True  # Permite animações e botão de voltar no celular
    )
