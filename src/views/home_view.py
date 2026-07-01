import flet as ft
from viewmodels.home_viewmodel import HomeViewModel
from components.custom_navigation_bar import CustomNavigationBar
from models.gasto import Gasto


@ft.component
def GastoItem(gasto: Gasto, on_delete):
    """Componente visual de um único gasto."""

    def delete_clicked(e):
        on_delete(gasto)

    return ft.ListTile(
        leading=ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.RED_400),
        title=ft.Text(gasto.descricao, weight=ft.FontWeight.BOLD),
        subtitle=ft.Text(f"{gasto.categoria} • {gasto.data.strftime('%d/%m/%Y')}"),
        trailing=ft.Row(
            controls=[
                ft.Text(f"R$ {gasto.valor:.2f}", color=ft.Colors.RED_400, size=16),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.RED_300,
                    tooltip="Excluir gasto",
                    on_click=delete_clicked,
                )
            ],
            tight=True
        )
    )


@ft.component
def HomeView():
    """
    Componente da tela principal (Dashboard) do usuário.
    """
    vm = HomeViewModel()

    gastos_lista, set_gastos_lista = ft.use_state(vm.gastos)
    saldo, set_saldo = ft.use_state(vm.saldo_total)

    def handle_delete(gasto: Gasto):
        vm.handle_excluir(gasto.id)

        set_gastos_lista(vm.gastos)
        set_saldo(vm.saldo_total)

        ft.context.page.overlay.append(
            ft.SnackBar(ft.Text(f"'{gasto.descricao}' excluído!"), open=True, bgcolor=ft.Colors.GREEN_700)
        )
        ft.context.page.update()

    lista_gastos_controles = []
    for gasto in gastos_lista:
        lista_gastos_controles.append(
            GastoItem(gasto=gasto, on_delete=handle_delete)
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
