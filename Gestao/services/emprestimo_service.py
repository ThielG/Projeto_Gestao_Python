from PySide6.QtWidgets import QMessageBox

from infra.repository.emprestimo_repository import EmprestimoRepository
from infra.repository.funcionario_repository import FuncionarioRepository
from infra.repository.uniforme_repository import UniformeRepository
from services.main_window_service import MainWindowService


class EmprestimoService:
    def __init__(self):
        self.service_main_window = MainWindowService()
        self.emprestimo_repository = EmprestimoRepository()
        self.uniforme_repository = UniformeRepository()
        self.funcionario_repository = FuncionarioRepository()

    def insert_emprestimo(self, emprestimo_ui):
        texto = emprestimo_ui.cb_tipo_uniforme.currentText()
        if emprestimo_ui.cb_tipo_uniforme.currentText() != 'Selecione um item' and emprestimo_ui.selected_funcionario is not None:
            uniforme = self.uniforme_repository.select_uniforme_by_name(emprestimo_ui.cb_tipo_uniforme.currentText())
            try:
                self.emprestimo_repository.insert_emprestimo(emprestimo_ui.selected_funcionario, uniforme)
                QMessageBox.information(emprestimo_ui, 'Empréstimos', 'Empréstimo cadastrado com sucesso!')
            except Exception as e:
                QMessageBox.warning(emprestimo_ui, 'Empréstimos', f'Erro ao cadastrar emprestimo! \nErro: {e}')
        else:
            if emprestimo_ui.cb_tipo_uniforme.currentText() == 'Selecione um item':
                QMessageBox.warning(emprestimo_ui, 'Empréstimos', 'Selecione um uniforme.')
            else:
                QMessageBox.warning(emprestimo_ui, 'Empréstimos', 'Selecione um funcionário.')


    def finalize_emprestimo(self, main_window):
        select_rows = main_window.tb_emprestismos_ativos.selectionModel().selectedRows()
        if not select_rows:
            QMessageBox.warning(main_window, 'Empréstimos', 'Selecione um empréstimo.')
            return
        select_row = select_rows[0].row()
        cpf_funcionario = main_window.tb_emprestismos_ativos.item(select_row, 1).text()
        uniforme_selecionado = main_window.tb_emprestismos_ativos.item(select_row, 3).text()

        msg_box = QMessageBox(main_window)
        msg_box.setWindowTitle('Finalizar empréstimo')
        msg_box.setText('Tem certeza que deseja finalizar este esmpréstimo?')
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton('Sim', QMessageBox.YesRole)
        no_button = msg_box.addButton('No', QMessageBox.NoRole)
        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            funcionario = self.funcionario_repository.select_funcionario_by_cpf(cpf_funcionario)
            uniforme = self.uniforme_repository.select_uniforme_by_name(uniforme_selecionado)
            try:
                self.emprestimo_repository.finalize_emprestimo(funcionario, uniforme)
                QMessageBox.warning(main_window, 'Empréstimos', f'Empréstimo finalziado com sucesso.')
                self.service_main_window.populate_table_emprestimos_ativos(main_window)
            except Exception as e:
                QMessageBox.warning(main_window, 'Empréstimos', f'Erro ao finalizar empréstimo. \nErro: {e}')
