import flet as ft
from views.welcome_view import WelcomeView


@ft.component
def AppRouter():
    """
    Mapeia automaticamente os componentes para as URLs.
    """
    return ft.Router(
        routes=[
            # A rota index=True significa que é a rota raiz ("/")
            ft.Route(index=True, component=WelcomeView),

            # A rota "/welcome" também leva para a mesma tela
            ft.Route(path="welcome", component=WelcomeView),
        ],
        manage_views=True  # Permite animações e botão de voltar no celular
    )
