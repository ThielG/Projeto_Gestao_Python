from PySide6.QtWidgets import QMessageBox

from infra.entities.uniforme import Uniforme
from infra.repository.emprestimo_repository import EmprestimoRepository
from infra.repository.funcionario_repository import FuncionarioRepository
from infra.repository.uniforme_repository import UniformeRepository
from services.main_window_service import MainWindowService


class UniformeService:
    def __init__(self):
        self.service_main_window = MainWindowService()
        self.emprestimo_repository = EmprestimoRepository()
        self.uniforme_repository = UniformeRepository()
        self.funcionario_repository = FuncionarioRepository()

    def insert_uniforme(self, main_window):
        uniforme = Uniforme()
        uniforme.nome = main_window.txt_nome_uniforme.text()
        uniforme.ativo = True
        try:
            self.uniforme_repository.insert_one_uniforme(uniforme)
            main_window.txt_nome_uniforme.setText('')
            self.service_main_window.populate_table_uniforme(main_window)
            QMessageBox.information(main_window, 'Uniformes', f'Uniforme cadastrado com sucesso.')
        except Exception as e:
            QMessageBox.warning(main_window, 'Uniforme', f'Erro ao cadastrar. \nErro: {e}')

    def update_uniforme(self, main_window):
        if main_window.btn_editar_uniforme.text() == 'Editar':
            selected_rows = main_window.tb_uniformes.selectionModel().selectedRows()
            if not selected_rows:
                return
            selected_row = selected_rows[0].row()
            main_window.txt_nome_uniforme.setText(main_window.tb_uniformes.item(selected_row, 0).text())
            self.uniforme_to_update = self.uniforme_repository.select_uniforme_by_name(
                main_window.tb_uniformes.item(selected_row, 0).text())
            main_window.btn_editar_uniforme.setText('Atualizar')
        else:
            self.uniforme_to_update.nome = main_window.txt_nome_uniforme.text()
            try:
                self.uniforme_repository.update_uniforme(self.uniforme_to_update)
                QMessageBox.information(main_window, 'Uniformes', f'Uniforme atualizado com sucesso.')
                main_window.btn_editar_uniforme.setText('Editar')
                main_window.txt_nome_uniforme.setText('')
                self.service_main_window.populate_table_uniforme(main_window)
            except Exception as e:
                QMessageBox.warning(main_window, 'Uniforme', f'Erro ao atualizar. \nErro: {e}')

    def delete_uniforme(self, main_window):
        selected_rows = main_window.tb_uniformes.selectionModel().selectedRows()
        if not selected_rows:
            return
        selected_row = selected_rows[0].row()
        self.uniforme_to_update = self.uniforme_repository.select_uniforme_by_name(
            main_window.tb_uniformes.item(selected_row, 0).text())
        msg_box = QMessageBox(main_window)
        msg_box.setWindowTitle('Remover uniforme')
        msg_box.setText(f'Tem certeza que deseja remover o uniforme {self.uniforme_to_update.nome}?')
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton('Sim', QMessageBox.YesRole)
        no_button = msg_box.addButton('Não', QMessageBox.NoRole)
        msg_box.exec()
        if msg_box.clickedButton() == yes_button:
            try:
                self.uniforme_repository.delete_uniforme(self.uniforme_to_update)
                QMessageBox.information(main_window, 'Uniformes', f'Uniforme removido com sucesso.')
                self.service_main_window.populate_table_uniforme(main_window)
            except Exception as e:
                QMessageBox.warning(main_window, 'Atenção', f'Erro ao remover uniforme. \nErro: {e}')
