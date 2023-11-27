from PySide6.QtWidgets import QMessageBox

from infra.entities.funcionario import Funcionario
from infra.repository.emprestimo_repository import EmprestimoRepository
from infra.repository.funcionario_repository import FuncionarioRepository
from infra.repository.uniforme_repository import UniformeRepository
from services.main_window_service import MainWindowService


class FuncionarioService:
    def __init__(self):
        self.service_main_window = MainWindowService()
        self.emprestimo_repository = EmprestimoRepository()
        self.uniforme_repository = UniformeRepository()
        self.funcionario_repository = FuncionarioRepository()

    def insert_funcionario(self, main_window):
        funcionario = Funcionario()
        funcionario.nome = main_window.txt_nome_funcionario.text()
        funcionario.cpf = main_window.txt_cpf_funcionario.text()
        funcionario.ativo = True
        try:
            self.funcionario_repository.insert_one_funcionario(funcionario)
            main_window.txt_nome_funcionario.setText('')
            main_window.txt_cpf_funcionario.setText('')
            self.service_main_window.populate_table_funcionario(main_window)
            QMessageBox.information(main_window, 'Funcionarios', 'Funcionario cadastrado com sucesso!')
        except Exception as e:
            QMessageBox.warning(main_window, 'Funcionarios', f'Erro ao cadastrar funcionario! \nErro: {e}')

    def select_funcionario(self, emprestimo_ui):
        if emprestimo_ui.btn_consulta_funcionario.text() == 'Limpar':
            emprestimo_ui.txt_nome_funcionario_emprestimo.setText('')
            emprestimo_ui.txt_cpf_funcionario_emprestimo.setText('')
            emprestimo_ui.txt_cpf_funcionario_emprestimo.setReadOnly(False)
            emprestimo_ui.select_funcionario = None
            emprestimo_ui.btn_consulta_funcionario.setText('Consultar')
        else:
            try:
                if emprestimo_ui.txt_cpf_funcionario_emprestimo.text() != '':
                    funcionario_emprestimo = self.funcionario_repository.select_funcionario_by_cpf(
                        emprestimo_ui.txt_cpf_funcionario_emprestimo.text())
                    emprestimo_ui.selected_funcionario = funcionario_emprestimo
                    emprestimo_ui.txt_nome_funcionario_emprestimo.setText(funcionario_emprestimo.nome)
                    emprestimo_ui.txt_cpf_funcionario_emprestimo.setReadOnly(True)
                    emprestimo_ui.btn_consulta_funcionario.setText('Limpar')
                else:
                    QMessageBox.warning(emprestimo_ui, 'Funcionarios', 'Insira um CPF valido.')
            except Exception as e:
                QMessageBox.warning(emprestimo_ui, 'Funcionarios', f'Erro ao consultar o funcionário. \nErro: {e}')
                emprestimo_ui.txt_nome_funcionario_emprestimo.clear()

    def update_funcionario(self, main_window):
        if main_window.btn_editar_funcionario.text() == 'Editar':
            selected_rows = main_window.tb_funcionarios.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(main_window, 'Funcionarios', 'Selecione um funcionario.')
                return
            selected_rows = selected_rows[0].row()
            main_window.txt_nome_funcionario.setText(main_window.tb_funcionarios.item(selected_rows, 0).text())
            main_window.txt_cpf_funcionario.setText(main_window.tb_funcionarios.item(selected_rows, 1).text())
            main_window.txt_cpf_funcionario.setReadOnly(True)
            main_window.btn_editar_funcionario.setText('Atualizar')
        else:
            cpf_funcionario = main_window.txt_cpf_funcionario.text()
            funcionario_updated = self.funcionario_repository.select_funcionario_by_cpf(cpf_funcionario)
            funcionario_updated.nome = main_window.txt_nome_funcionario.text()

            try:
                self.funcionario_repository.update_funcionario(funcionario_updated)
                QMessageBox.information(main_window, "Cadastro de funcionário", "Funcionário atualizado com sucesso!")
                main_window.btn_editar_funcionario.setText('Editar')
                main_window.txt_nome_funcionario.clear()
                main_window.txt_cpf_funcionario.clear()
                self.service_main_window.populate_table_funcionario(main_window)
            except Exception as e:
                QMessageBox.warning(main_window, "Atenção", f'Problema ao atualizar funcionário.\nErro: {e}')

    def delete_funcionario(self, main_window):
        selected_rows = main_window.tb_funcionarios.selectionModel().selectRows()
        if not selected_rows:
            return
        selected_row = selected_rows[0].row()
        funcionario_delete = self.funcionario_repository.select_funcionario_by_cpf(
            main_window.tb_funcionario.item(selected_row, 1).text()
        )
        msg_box = QMessageBox(main_window)
        msg_box.setWindowTitle('Remover funcionario')
        msg_box.setText(f'Tem certeza que deseja remover o funcionario {funcionario_delete.nome}?')
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton('Sim', QMessageBox.YesRole)
        no_button = msg_box.addButton('Não', QMessageBox.NoRole)
        msg_box.exec()
        if msg_box.clickedButton() == yes_button:
            try:
                self.funcionario_repository.delete_funcionio(funcionario_delete)
                self.service_main_window.populate_table_funcionario(main_window)
            except Exception as e:
                QMessageBox.warning(main_window, 'Atenção', f'Erro ao remover funcionario. \nErro: {e}')
