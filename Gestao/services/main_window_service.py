import datetime

import pandas as pd
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem

from infra.repository.emprestimo_repository import EmprestimoRepository
from infra.repository.uniforme_repository import UniformeRepository
from infra.repository.funcionario_repository import FuncionarioRepository


class MainWindowService:
    def __init__(self):
        self.emprestimo_repository = EmprestimoRepository
        self.funcionario_repository = FuncionarioRepository
        self.uniforme_repository = UniformeRepository

    def populate_table_funcionario(self, main_window):
        main_window.tb_funcionarios.setRowCount(0)
        lista_funcionario = self.funcionario_repository.select_all_funcionario()
        for funcionario in lista_funcionario[:]:
            if not funcionario.ativo:
                lista_funcionario.remove(funcionario)
        main_window.tb_funcionarios.setRowCount(len(lista_funcionario))
        for linha, funcionario in enumerate(lista_funcionario):
            if funcionario.ativo:
                main_window.tb_funcionarios.setItem(linha, 0, QTableWidgetItem(funcionario.nome))
                main_window.tb_funcionarios.setItem(linha, 1, QTableWidgetItem(funcionario.cpf))

    def populate_table_uniforme(self, main_window):
        main_window.tb_uniformes.setRowCount(0)
        lista_uniforme = self.uniforme_repository.select_all_uniformes()
        for uniforme in lista_uniforme[:]:
            if not uniforme.ativo:
                lista_uniforme.remove(uniforme)
        main_window.tb_uniformes.setRowCount(len(lista_uniforme))
        for linha, uniforme in enumerate(lista_uniforme):
            if uniforme.ativo:
                main_window.tb_uniformes.setItem(linha, 0, QTableWidgetItem(uniforme.nome))

    def populate_table_emprestimos_ativos(self, main_window):
        main_window.tb_emprestismos_ativos.setRowCount(0)
        emprestimos_ativos = self.emprestimo_repository.select_emprestimo_ativos()
        main_window.tb_emprestismos_ativos.setRowCount(len(emprestimos_ativos))
        for linha, (emp, funcionario, uniforme) in enumerate(emprestimos_ativos):
            main_window.tb_emprestismos_ativos.setItem(linha, 0, QTableWidgetItem(funcionario.nome))
            main_window.tb_emprestismos_ativos.setItem(linha, 1, QTableWidgetItem(funcionario.cpf))
            main_window.tb_emprestismos_ativos.setItem(linha, 2, QTableWidgetItem(emp.data_emprestimo.strftime('%d/%m/%Y')))
            main_window.tb_emprestismos_ativos.setItem(linha, 3, QTableWidgetItem(uniforme.nome))

    def populate_uniformes_combo(self, emprestimo_ui):
        emprestimo_ui.cb_tipo_uniforme.clear()
        emprestimo_ui.cb_tipo_uniforme.addItem('Selecione um item')
        emprestimo_ui.uniformes = self.uniforme_repository.select_all_uniformes()
        for uniforme in emprestimo_ui.uniformes[:]:
            if not uniforme.ativo:
                emprestimo_ui.uniformes.remove(uniforme)
        for uniforme in emprestimo_ui.uniformes:
            emprestimo_ui.cb_tipo_uniforme.addItem(uniforme.nome)

    def populate_relatorio(self, main_window):
        try:
            main_window.tb_relatorio.setRowCount(0)
            emprestimos = self.emprestimo_repository.select_emprestimos_in_period(main_window.txt_data_inicial.text(),
                                                                                  main_window.txt_data_final.text())
            main_window.tb_relatorio.setRowCount(len(emprestimos))
            for linha, (emp, funcionario, uniforme) in enumerate(emprestimos):
                main_window.tb_relatorio.setItem(linha, 0, QTableWidgetItem(funcionario.nome))
                main_window.tb_relatorio.setItem(linha, 1, QTableWidgetItem(emp.data_emprestimo.strftime('%d/%m/%Y')))
                main_window.tb_relatorio.setItem(linha, 2, QTableWidgetItem(emp.data_devolucao.strftime('%d/%m/%Y')))
                main_window.tb_relatorio.setItem(linha, 3, QTableWidgetItem(uniforme.nome))
        except Exception as e:
            QMessageBox.warning(main_window, 'Atenção', f'Periodo de data incorreto!\nErro {e}')

    def export_relatorio(self, main_window):
        if main_window.tb_relatorio.rowCount() > 0:
            rows = main_window.tb_relatorio.rowCount()
            cols = main_window.tb_relatorio.columnCount()
            headers = ['Nome do funcionário', 'Data de emprestimo', 'Data de devolução', 'Tipo de uniforme']
            data = []
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    item = main_window.tb_relatorio.item(row, col)
                    if item and item.text():
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                data.append(row_data)
            try:
                df = pd.DataFrame(data, columns=headers)
            except Exception as e:
                pass

            try:
                df.to_excel(f'relatorio_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx', index=False,
                            engine='openpyxl')
                QMessageBox.information(main_window, "Empréstimos", f'Relatório exportado com sucesso! \n'
                                                                    f'Verifique na pasta do programa o arquivo:\n'
                                                                    f' relarorio_{datetime.datetime.now()}.xlsx')
            except Exception as e:
                QMessageBox.warning(main_window, 'Atenção', f'Erro ao gerar relatório!\nErro: {e}')
