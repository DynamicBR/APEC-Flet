import flet as ft
from state.app_state import AppState
from components.custom_navigation_bar import CustomNavigationBar
from models.configuracao import Configuracao

@ft.component
def SettingsView():
    """
    Componente da tela de configurações para definir orçamento/salário e preferências.
    """
    app_state = AppState()
    config_atual = app_state.config

    salario_ref = ft.Ref[ft.TextField]()
    periodo_ref = ft.Ref[ft.Dropdown]()

    def salvar_configuracoes(e):
        try:
            novo_salario = float(salario_ref.current.value.replace(",", "."))
        except ValueError:
            ft.context.page.overlay.append(
                ft.SnackBar(ft.Text("Valor inválido! Digite apenas números."), open=True, bgcolor=ft.Colors.RED_700)
            )
            ft.context.page.update()
            return

        if config_atual is None:
            nova_config = Configuracao(id=1, salario=novo_salario, periodo=periodo_ref.current.value)
            app_state.salvar_configuracao(nova_config)
        else:
            config_atual.salario = novo_salario
            config_atual.periodo = periodo_ref.current.value
            app_state.salvar_configuracao(config_atual)

        ft.context.page.overlay.append(
            ft.SnackBar(ft.Text("Configurações atualizadas com sucesso!"), open=True, bgcolor=ft.Colors.GREEN_700)
        )
        ft.context.page.update()
        ft.context.page.navigate("/home")

    return ft.View(
        route="/settings",
        navigation_bar=CustomNavigationBar(),
        controls=[
            ft.SafeArea(
                ft.Container(
                    padding=20,
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Text("Configurações", size=28, weight=ft.FontWeight.BOLD),

                            ft.Container(height=20),

                            ft.Text("Minhas Finanças", size=18, weight=ft.FontWeight.BOLD),

                            ft.TextField(
                                ref=salario_ref,
                                label="Meu Salário / Orçamento (R$)",
                                value=f"{config_atual.salario:.2f}" if config_atual else "0.00",
                                keyboard_type=ft.KeyboardType.NUMBER
                            ),

                            ft.Dropdown(
                                ref=periodo_ref,
                                label="Período do Orçamento",
                                value=config_atual.periodo if config_atual else "Mensal",
                                options=[
                                    ft.dropdown.Option("Mensal"),
                                    ft.dropdown.Option("Quinzenal"),
                                    ft.dropdown.Option("Semanal"),
                                ]
                            ),

                            ft.Container(height=30),

                            ft.Button(
                                "Salvar Configurações",
                                on_click=salvar_configuracoes,
                                expand=True,
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                icon=ft.Icons.SAVE
                            )
                        ]
                    )
                )
            )
        ]
    )
