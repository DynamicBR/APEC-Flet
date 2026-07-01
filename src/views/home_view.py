import flet as ft
from viewmodels.home_viewmodel import HomeViewModel
from components.custom_navigation_bar import CustomNavigationBar
from state.app_state import AppState


@ft.component
def HomeView():
    """
    Componente da tela principal (Dashboard) do usuário.
    """
    vm = HomeViewModel()
    app_state = AppState()

    _, set_atualizar = ft.use_state(False)

    def ao_receber_notificacao():
        set_atualizar(lambda x: not x)

    def gerenciar_inscricao():
        app_state.add_listener(ao_receber_notificacao)
        return lambda: app_state.remove_listener(ao_receber_notificacao)

    ft.use_effect(gerenciar_inscricao, [])

    saldo = vm.saldo_total
    gastos = vm.gastos

    def confirmar_exclusao(gasto_id, descricao):
        def deletar(e):
            vm.handle_excluir(gasto_id)

            dlg.open = False
            ft.context.page.overlay.append(
                ft.SnackBar(ft.Text(f"'{descricao}' excluído com sucesso!"), open=True, bgcolor=ft.Colors.GREEN_700)
            )
            ft.context.page.update()

        def fechar(e):
            dlg.open = False
            ft.context.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente excluir o gasto '{descricao}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar),
                ft.TextButton("Excluir", on_click=deletar, style=ft.ButtonStyle(color=ft.Colors.RED_400)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        ft.context.page.dialog = dlg
        dlg.open = True
        ft.context.page.update()

    lista_gastos_controles = []
    for gasto in gastos:
        lista_gastos_controles.append(
            ft.ListTile(
                leading=ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.RED_400),
                title=ft.Text(gasto.descricao, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"{gasto.categoria} • {gasto.data.strftime('%d/%m/%Y')}"),
                trailing=ft.Row(
                    controls=[
                        ft.Text(f"R$ {gasto.valor:.2f}", color=ft.Colors.RED_400, size=16),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINED,
                            icon_color=ft.Colors.RED_300,
                            tooltip="Excluir gasto",
                            on_click=lambda e, g_id=gasto.id, desc=gasto.descricao: confirmar_exclusao(g_id, desc)
                        )
                    ],
                    tight=True
                )
            )
        )

    if not lista_gastos_controles:
        lista_gastos_controles.append(
            ft.Container(
                content=ft.Text("Nenhum gasto registrado ainda.", color=ft.Colors.WHITE54, italic=True),
                padding=20,
                alignment=ft.Alignment.CENTER
            )
        )

    return ft.View(
        route="/home",
        navigation_bar=CustomNavigationBar(),

        floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.BLUE_500,
            on_click=lambda e: ft.context.page.navigate("/add_expense")
        ),

        controls=[
            ft.SafeArea(
                ft.Container(
                    padding=20,
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Meu Saldo", size=16, color=ft.Colors.WHITE70),
                                    ft.Text(f"R$ {saldo:.2f}", size=40, weight=ft.FontWeight.BOLD),
                                ]),
                                padding=20,
                                bgcolor=ft.Colors.BLUE_GREY_900,
                                border_radius=10,
                                width=float("inf")
                            ),

                            ft.Container(height=20),

                            ft.Text("Gastos Recentes", size=20, weight=ft.FontWeight.BOLD),

                            ft.Column(
                                controls=lista_gastos_controles,
                                scroll=ft.ScrollMode.AUTO,
                                expand=True
                            )
                        ],
                        expand=True
                    )
                )
            )
        ]
    )
