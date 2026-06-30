import flet as ft
import select

from flet.controls.core import icon


@ft.component
def CustomNavigationBar():
    """
    Componente do rodapé reutilizável que gerencia a navegação entre as telas principais
    """
    selected_index = 0
    if ft.is_route_active("/stats"):
        selected_index = 1
    elif ft.is_route_active("/settigns"):
        selected_index = 2

    def handle_nav_change(e):
        """Muda a rota quando o usuário clica em um botão do rodapé"""
        index = e.control.selected_index

        if index == 0:
            ft.context.page.navigate("/home")
        elif index == 1:
            ft.context.page.navigate("/stats")
        elif index == 2:
            ft.context.page.navigate("/settings")

    return ft.NavigationBar(
        selected_index=selected_index,
        on_change=handle_nav_change,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PIE_CHART_OUTLINE,
                selected_icon=ft.Icons.PIE_CHART,
                label="Estatísticas"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Ajustes"
            )
        ]
    )
