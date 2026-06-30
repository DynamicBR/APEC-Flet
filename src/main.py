import flet as ft
from router import AppRouter
from state.app_state import AppState

def main(page: ft.Page):
    # 1. Configurações da Janela
    page.title = "APEC - Controle de Gastos"
    page.theme_mode = ft.ThemeMode.DARK

    page.window.width = 400
    page.window.height = 800

    app_state = AppState()

    #Renderiza toda a aplicação passando a bola para o novo AppRouter!
    page.render_views(AppRouter)

if __name__ == '__main__':
    ft.run(main)
