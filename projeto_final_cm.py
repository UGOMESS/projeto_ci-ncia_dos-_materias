import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton

class App(QWidget):
    def __init__(self, materiais):
        super().__init__()
        self.materiais = materiais
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label e combobox para selecionar o tipo de material
        self.label_tipo = QLabel('Selecione o tipo de material:')
        layout.addWidget(self.label_tipo)

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(['Metais', 'Cerâmicas', 'Polímeros', 'Compósitos'])
        self.combo_tipo.currentIndexChanged.connect(self.atualizar_tabela)
        layout.addWidget(self.combo_tipo)

        # Seleção de dois materiais para comparação
        self.label_material_A = QLabel('Selecione o Material A:')
        layout.addWidget(self.label_material_A)

        self.combo_material_A = QComboBox()
        layout.addWidget(self.combo_material_A)

        self.label_material_B = QLabel('Selecione o Material B:')
        layout.addWidget(self.label_material_B)

        self.combo_material_B = QComboBox()
        layout.addWidget(self.combo_material_B)

        # Label e combobox para selecionar a propriedade do gráfico de barras
        self.label_propriedade_barras = QLabel('Selecione a propriedade para o gráfico de barras:')
        layout.addWidget(self.label_propriedade_barras)

        self.combo_grafico_barras = QComboBox()
        self.combo_grafico_barras.addItems(['Densidade (g/cm³)', 'Resistência à Tração (MPa)', 
                                             'Módulo de Young (GPa)', 'Resistência Específica (kN·m/kg)', 
                                             'Rigidez Específica (MN·m/kg)'])
        self.combo_grafico_barras.currentIndexChanged.connect(self.atualizar_grafico_barras)
        layout.addWidget(self.combo_grafico_barras)

        # Label e combobox para selecionar as duas propriedades do gráfico de dispersão
        self.label_grafico = QLabel('Selecione duas propriedades para o gráfico de dispersão:')
        layout.addWidget(self.label_grafico)

        h_layout_props = QHBoxLayout()

        self.combo_prop_x = QComboBox()
        self.combo_prop_x.addItems(['Densidade (g/cm³)', 'Resistência à Tração (MPa)', 
                                     'Módulo de Young (GPa)', 'Resistência Específica (kN·m/kg)', 
                                     'Rigidez Específica (MN·m/kg)'])
        h_layout_props.addWidget(self.combo_prop_x)

        self.combo_prop_y = QComboBox()
        self.combo_prop_y.addItems(['Densidade (g/cm³)', 'Resistência à Tração (MPa)', 
                                     'Módulo de Young (GPa)', 'Resistência Específica (kN·m/kg)', 
                                     'Rigidez Específica (MN·m/kg)'])
        h_layout_props.addWidget(self.combo_prop_y)

        layout.addLayout(h_layout_props)

        # Botão para gerar o gráfico de comparação
        self.btn_gerar_grafico = QPushButton('Gerar Gráfico de Comparação')
        self.btn_gerar_grafico.clicked.connect(self.atualizar_grafico_comparacao)
        layout.addWidget(self.btn_gerar_grafico)

        # Tabela de materiais
        self.tabela_materiais = QTableWidget()
        layout.addWidget(self.tabela_materiais)

        # Adicionando canvas para o gráfico
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.setWindowTitle('Visualizador de Materiais')
        self.show()

        # Inicializa a tabela de materiais
        self.atualizar_tabela()

    def atualizar_tabela(self):
        tipo_selecionado = self.combo_tipo.currentText()
        materiais_filtrados = self.materiais[self.materiais['Tipo'] == tipo_selecionado]

        # Preenche as opções de materiais nos comboboxes
        self.combo_material_A.clear()
        self.combo_material_B.clear()
        self.combo_material_A.addItems(materiais_filtrados['Material'].tolist())
        self.combo_material_B.addItems(materiais_filtrados['Material'].tolist())

        # Atualiza a tabela
        self.tabela_materiais.setRowCount(len(materiais_filtrados))
        self.tabela_materiais.setColumnCount(len(materiais_filtrados.columns))

        # Define os cabeçalhos da tabela
        self.tabela_materiais.setHorizontalHeaderLabels(materiais_filtrados.columns.tolist())

        for row in range(len(materiais_filtrados)):
            for col in range(len(materiais_filtrados.columns)):
                item = QTableWidgetItem(str(materiais_filtrados.iloc[row, col]))
                self.tabela_materiais.setItem(row, col, item)

        # Ajusta a largura das colunas automaticamente
        self.tabela_materiais.resizeColumnsToContents()

        # Atualiza o gráfico de barras após a tabela
        self.atualizar_grafico_barras()

    def atualizar_grafico_barras(self):
        tipo_selecionado = self.combo_tipo.currentText()
        materiais_filtrados = self.materiais[self.materiais['Tipo'] == tipo_selecionado]

        # Verifica qual propriedade foi selecionada para o gráfico de barras
        propriedade_selecionada = self.combo_grafico_barras.currentText()
        self.plotar_grafico_barras(materiais_filtrados, propriedade_selecionada)

    def atualizar_grafico_comparacao(self):
        tipo_selecionado = self.combo_tipo.currentText()
        materiais_filtrados = self.materiais[self.materiais['Tipo'] == tipo_selecionado]

        # Captura os materiais selecionados
        material_A = self.combo_material_A.currentText()
        material_B = self.combo_material_B.currentText()

        # Verifica se os dois materiais foram selecionados corretamente
        if material_A and material_B:
            dados_A = materiais_filtrados[materiais_filtrados['Material'] == material_A]
            dados_B = materiais_filtrados[materiais_filtrados['Material'] == material_B]

            # Captura as propriedades selecionadas
            propriedade_x = self.combo_prop_x.currentText()
            propriedade_y = self.combo_prop_y.currentText()

            self.plotar_grafico_comparacao(dados_A, dados_B, propriedade_x, propriedade_y)

    def plotar_grafico_barras(self, materiais_filtrados, propriedade_selecionada):
        self.figure.clear()  # Limpa o gráfico anterior

        # Criar gráfico de barras com a propriedade selecionada
        indices_materiais = list(range(1, len(materiais_filtrados) + 1))  # Reiniciar a contagem a partir de 1
        propriedade = materiais_filtrados[propriedade_selecionada].apply(self.processar_valores)

        ax = self.figure.add_subplot(111)
        ax.bar(indices_materiais, propriedade, color='lightblue')
        ax.set_xlabel('Índice do Material na Tabela')
        ax.set_ylabel(propriedade_selecionada)
        ax.set_title(f'{propriedade_selecionada} dos {self.combo_tipo.currentText()}')

        # Configura os números das linhas no eixo X
        ax.set_xticks(indices_materiais)
        ax.set_xticklabels(indices_materiais, rotation=0)

        # Renderiza o gráfico no canvas
        self.canvas.draw()

    def plotar_grafico_comparacao(self, dados_A, dados_B, prop_x, prop_y):
        self.figure.clear()  # Limpa o gráfico anterior

        # Processa os valores das propriedades
        x_A = self.processar_valores(dados_A[prop_x].values[0])
        y_A = self.processar_valores(dados_A[prop_y].values[0])
        x_B = self.processar_valores(dados_B[prop_x].values[0])
        y_B = self.processar_valores(dados_B[prop_y].values[0])

        ax = self.figure.add_subplot(111)

        # Plota os dois materiais como pontos
        ax.scatter([x_A], [y_A], color='blue', label=f'{dados_A["Material"].values[0]}', s=100, marker='o')
        ax.scatter([x_B], [y_B], color='red', label=f'{dados_B["Material"].values[0]}', s=100, marker='o')

        ax.set_xlabel(prop_x)
        ax.set_ylabel(prop_y)
        ax.set_title(f'Comparação entre {dados_A["Material"].values[0]} e {dados_B["Material"].values[0]}')
        ax.legend()

        # Renderiza o gráfico no canvas
        self.canvas.draw()

    def processar_valores(self, valor):
        # Verifica se o valor contém um intervalo (ex: "2.33-3.44")
        if '-' in str(valor):
            partes = valor.split('-')
            # Converte as partes para float e retorna a média
            return (float(partes[0]) + float(partes[1])) / 2
        else:
            # Se não for intervalo, retorna o valor como float
            return float(valor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    caminho_arquivo = r'D:\Documentos_GOMES\workspace_code\ciencia_dos_materiais_python\dados_projeto_cm.xlsx'
    dados_materiais = pd.read_excel(caminho_arquivo)  # Carregar os dados
    ex = App(dados_materiais)
    sys.exit(app.exec_())
