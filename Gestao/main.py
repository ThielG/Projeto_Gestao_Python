import sys

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtGui import QPalette, QColor, Qt

from view.main_ui import Ui_MainWindow
from view.emprestimo_ui import Ui_Dialog
from infra.config.connection import DBConnectionHandler
from services.main_window_service import MainWindowService
from services.funcionario_service import FuncionarioService
from services.uniforme_service import UniformeService
from services.emprestimo_service import EmprestimoService


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.btn_emprestar.clicked.connect(self.adicionar_emprestimo)
        data_base = DBConnectionHandler()
        self.uniforme_to_update = None

        self.setWindowIcon(QtGui.QIcon('uniforme-policial-removebg-preview'))

        self.main_window_service = MainWindowService()
        self.funcionario_service = FuncionarioService()
        self.uniforme_service = UniformeService()
        self.emprestimo_service = EmprestimoService()
        self.main_window_service.populate_table_uniforme(self)
        self.main_window_service.populate_table_funcionario(self)
        self.main_window_service.populate_table_emprestimos_ativos(self)

        self.btn_emprestar.clicked.connect(self.adicionar_emprestimo)
        self.btn_receber.clicked.connect(self.finalizar_emprestimo)

        self.btn_adicionar_uniforme.clicked.connect(self.adicionar_uniforme)
        self.btn_editar_uniforme.clicked.connect(self.atualizar_uniforme)
        self.btn_remover_uniforme.clicked.connect(self.remover_uniforme)

        self.btn_adicionar_funcionario.clicked.connect(self.adicionar_funcionario)
        self.btn_editar_funcionario.clicked.connect(self.atualizar_funcionario)
        self.btn_remover_funcionario.clicked.connect(self.remover_funcionario)

        self.btn_consultar.clicked.connect(self.consultar_periodo)
        self.btn_exportar.clicked.connect(self.exportar_relatorio)

    def adicionar_funcionario(self):
        self.funcionario_service.insert_funcionario(self)

    def atualizar_funcionario(self):
        self.funcionario_service.update_funcionario(self)

    def remover_funcionario(self):
        self.funcionario_service.delete_funcionario(self)

    def adicionar_uniforme(self):
        self.uniforme_service.insert_uniforme(self)

    def atualizar_uniforme(self):
        self.uniforme_service.update_uniforme(self)

    def remover_uniforme(self):
        self.uniforme_service.delete_uniforme(self)

    def finalizar_emprestimo(self):
        self.emprestimo_service.finalize_emprestimo(self)

    def consultar_periodo(self):
        self.main_window_service.populate_relatorio(self)

    def exportar_relatorio(self):
        self.main_window_service.export_relatorio(self)

    def adicionar_emprestimo(self):
        self.emprestimo_dialog = EmprestimoDialog(self)
        self.emprestimo_dialog.finished.connect(self.on_emprestimo_closed)
        self.emprestimo_dialog.show()
        self.emprestimo_dialog.finished.connect(
            lambda: self.main_window_service.populate_table_emprestimos_ativos(self))
        self.hide()

    def on_emprestimo_closed(self):
        self.show()


class EmprestimoDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(EmprestimoDialog, self).__init__(parent)
        self.setupUi(self)
        self.selected_funcionario = None
        self.unifromes = []
        self.main_window_service = MainWindowService()
        self.funcionario_service = FuncionarioService()
        self.uniforme_service = UniformeService()
        self.emprestimo_service = EmprestimoService()
        self.main_window_service.populate_uniformes_combo(self)

        self.btn_consulta_funcionario.clicked.connect(self.get_funcionario)
        self.btn_confirmar.clicked.connect(self.set_emprestimo)

    def get_funcionario(self):
        self.funcionario_service.select_funcionario(self)

    def set_emprestimo(self):
        self.emprestimo_service.insert_emprestimo(self)


if __name__ == '__main__':
    app = QApplication()
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))
    palette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(127, 127, 127))

    app.setPalette(palette)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
