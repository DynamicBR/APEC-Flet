import flet as ft
from viewmodels.estatisticas_viewmodel import EstatisticasViewModel
from components.custom_navigation_bar import CustomNavigationBar

@ft.component
def StatsView():
    vm = EstatisticasViewModel()
    filtro, set_filtro = ft.use_state("Todos")
    vm.carregar_dados(filtro_strategy=filtro)

    categorias_dict = vm.categorias
    top5_gastos = vm.maiores_gastos
    total_gasto = vm.total

    barras_categoria = []
    paleta_cores = [
        ft.Colors.BLUE_400, ft.Colors.RED_400, ft.Colors.GREEN_400,
        ft.Colors.AMBER_400, ft.Colors.PURPLE_400, ft.Colors.CYAN_400
    ]

    if total_gasto > 0:
        for i, (categoria, valor) in enumerate(categorias_dict.items()):
            porcentagem = valor / total_gasto
            cor = paleta_cores[i % len(paleta_cores)]

            barras_categoria.append(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(categoria, weight=ft.FontWeight.BOLD),
                                ft.Text(f"R$ {valor:.2f} ({porcentagem * 100:.0f}%)", color=ft.Colors.WHITE70)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.ProgressBar(value=porcentagem, color=cor, bgcolor=ft.Colors.WHITE_12)
                    ]
                )
            )
            barras_categoria.append(ft.Container(height=10))
    else:
        barras_categoria.append(
            ft.Container(
                content=ft.Text("Nenhum gasto neste período.", color=ft.Colors.WHITE_54, italic=True),
                padding=10,
                alignment=ft.Alignment.CENTER
            )
        )

    controles_top5 = []
    for gasto in top5_gastos:
        controles_top5.append(
            ft.ListTile(
                leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER_400),
                title=ft.Text(gasto.descricao, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(gasto.categoria),
                trailing=ft.Text(f"R$ {gasto.valor:.2f}", color=ft.Colors.RED_400, size=16),
            )
        )

    if not controles_top5:
        controles_top5.append(ft.Text("Nenhum gasto registrado.", color=ft.Colors.WHITE54))

    def handle_swipe(e):
        if e.primary_velocity > 300:
            ft.context.page.navigate("/home")
        elif e.primary_velocity < -300:
            ft.context.page.navigate("/settings")

    return ft.View(
        route="/stats",
        navigation_bar=CustomNavigationBar(),
        controls=[
            ft.GestureDetector(
                on_horizontal_drag_end=handle_swipe,
                expand=True,
                content=ft.SafeArea(
                    ft.Container(
                        padding=20,
                        expand=True,
                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            controls=[
                                ft.Text("Estatísticas", size=28, weight=ft.FontWeight.BOLD),
                                ft.Dropdown(
                                    label="Filtrar Período",
                                    value=filtro,
                                    options=[
                                        ft.dropdown.Option("Todos"),
                                        ft.dropdown.Option("Este Mês"),
                                        ft.dropdown.Option("Esta Semana"),
                                    ],
                                    on_select=lambda e: set_filtro(e.control.value)
                                ),
                                ft.Container(height=10),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Total Gasto no Período", size=14, color=ft.Colors.WHITE_70),
                                        ft.Text(f"R$ {total_gasto:.2f}", size=32, weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.RED_400),
                                    ]),
                                    padding=20,
                                    bgcolor=ft.Colors.BLUE_GREY_900,
                                    border_radius=10,
                                    width=float("inf")
                                ),
                                ft.Container(height=15),
                                ft.Text("Gastos por Categoria", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Column(controls=barras_categoria),
                                    padding=10
                                ),
                                ft.Container(height=15),
                                ft.Text("Maiores Gastos", size=18, weight=ft.FontWeight.BOLD),
                                ft.Column(
                                    controls=controles_top5
                                )
                            ]
                        )
                    )
                )
            )
        ]
    )
