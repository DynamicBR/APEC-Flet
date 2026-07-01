import flet as ft
from state.app_state import AppState
from models.gasto import Gasto

@ft.component
def AddExpenseView():
    """
    Componente da tela com o formulário para adicionar um novo gasto.
    """
    descricao_ref = ft.Ref[ft.TextField]()
    valor_ref = ft.Ref[ft.TextField]()
    categoria_ref = ft.Ref[ft.Dropdown]()

    def salvar_gasto(e):
        descricao = descricao_ref.current.value
        valor_str = valor_ref.current.value
        categoria = categoria_ref.current.value

        if not descricao or not valor_str or not categoria:
            ft.context.page.overlay.append(
                ft.SnackBar(ft.Text("Por favor, preencha todos os campos!"), open=True, bgcolor=ft.Colors.RED_700)
            )
            ft.context.page.update()
            return

        try:
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            ft.context.page.overlay.append(
                ft.SnackBar(ft.Text("Valor inválido! Digite apenas números."), open=True, bgcolor=ft.Colors.RED_700)
            )
            ft.context.page.update()
            return

        novo_gasto = Gasto(descricao=descricao, categoria=categoria, valor=valor)
        AppState().adicionar_gasto(novo_gasto)

        ft.context.page.overlay.append(
            ft.SnackBar(ft.Text("Gasto salvo com sucesso!"), open=True, bgcolor=ft.Colors.GREEN_700)
        )
        ft.context.page.update()
        ft.context.page.navigate("/home")

    def cancelar(e):
        ft.context.page.navigate("/home")

    return ft.View(
        route="/add_expense",
        appbar=ft.AppBar(
            title=ft.Text("Adicionar Gasto"),
            bgcolor=ft.Colors.SURFACE_BRIGHT
        ),
        controls=[
            ft.SafeArea(
                ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.TextField(
                                ref=descricao_ref,
                                label="Descrição",
                                hint_text="Ex: Pizza com amigos",
                                autofocus=True
                            ),

                            ft.TextField(
                                ref=valor_ref,
                                label="Valor (R$)",
                                hint_text="0.00",
                                keyboard_type=ft.KeyboardType.NUMBER
                            ),

                            ft.Dropdown(
                                ref=categoria_ref,
                                label="Categoria",
                                options=[
                                    ft.dropdown.Option("Alimentação"),
                                    ft.dropdown.Option("Transporte"),
                                    ft.dropdown.Option("Contas"),
                                    ft.dropdown.Option("Lazer"),
                                    ft.dropdown.Option("Saúde"),
                                    ft.dropdown.Option("Educação"),
                                    ft.dropdown.Option("Outros"),
                                ]
                            ),

                            ft.Container(height=30),

                            ft.Row(
                                controls=[
                                    ft.OutlinedButton("Cancelar", on_click=cancelar, expand=True),
                                    ft.Button(
                                        "Salvar",
                                        on_click=salvar_gasto,
                                        expand=True,
                                        bgcolor=ft.Colors.BLUE_600,
                                        color=ft.Colors.WHITE
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ]
                    )
                )
            )
        ]
    )
