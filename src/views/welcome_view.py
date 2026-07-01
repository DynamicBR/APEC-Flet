import flet as ft


@ft.component
def WelcomeView():
    """
    Componente da tela de boas-vindas moderno e sem avisos de depreciação.
    """
    return ft.View(
        route="/welcome",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            ft.Icons.ACCOUNT_BALANCE_ROUNDED,
                            size=80,
                            color=ft.Colors.BLUE_400
                        ),
                        ft.Text(
                            value="Bem-vindo ao APEC",
                            size=32,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            value="Aplicativo de Planejamento Execução e Controle",
                            size=16,
                            color=ft.Colors.WHITE70
                        ),
                        ft.Container(height=20),

                        ft.Button(
                            "Começar",
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=lambda e: ft.context.page.navigate("/home")
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True
            )
        ]
    )