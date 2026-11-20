# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loja.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_JanelaPrincipal(object):
    def setupUi(self, JanelaPrincipal):
        if not JanelaPrincipal.objectName():
            JanelaPrincipal.setObjectName(u"JanelaPrincipal")
        JanelaPrincipal.resize(950, 620)
        self.centralwidget = QWidget(JanelaPrincipal)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutPrincipal = QVBoxLayout(self.centralwidget)
        self.layoutPrincipal.setObjectName(u"layoutPrincipal")
        self.labelTitulo = QLabel(self.centralwidget)
        self.labelTitulo.setObjectName(u"labelTitulo")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.labelTitulo.setFont(font)
        self.labelTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layoutPrincipal.addWidget(self.labelTitulo)

        self.abas = QTabWidget(self.centralwidget)
        self.abas.setObjectName(u"abas")
        self.abaProdutos = QWidget()
        self.abaProdutos.setObjectName(u"abaProdutos")
        self.layoutProdutos = QVBoxLayout(self.abaProdutos)
        self.layoutProdutos.setObjectName(u"layoutProdutos")
        self.grupoProduto = QGroupBox(self.abaProdutos)
        self.grupoProduto.setObjectName(u"grupoProduto")
        self.formProduto = QFormLayout(self.grupoProduto)
        self.formProduto.setObjectName(u"formProduto")
        self.labelProdNome = QLabel(self.grupoProduto)
        self.labelProdNome.setObjectName(u"labelProdNome")

        self.formProduto.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelProdNome)

        self.txtProdNome = QLineEdit(self.grupoProduto)
        self.txtProdNome.setObjectName(u"txtProdNome")

        self.formProduto.setWidget(0, QFormLayout.ItemRole.FieldRole, self.txtProdNome)

        self.labelProdPreco = QLabel(self.grupoProduto)
        self.labelProdPreco.setObjectName(u"labelProdPreco")

        self.formProduto.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelProdPreco)

        self.spinProdPreco = QDoubleSpinBox(self.grupoProduto)
        self.spinProdPreco.setObjectName(u"spinProdPreco")
        self.spinProdPreco.setMaximum(99999.990000000005239)

        self.formProduto.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinProdPreco)

        self.labelProdEstoque = QLabel(self.grupoProduto)
        self.labelProdEstoque.setObjectName(u"labelProdEstoque")

        self.formProduto.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelProdEstoque)

        self.spinProdEstoque = QSpinBox(self.grupoProduto)
        self.spinProdEstoque.setObjectName(u"spinProdEstoque")
        self.spinProdEstoque.setMaximum(99999)

        self.formProduto.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spinProdEstoque)

        self.labelProdFornecedor = QLabel(self.grupoProduto)
        self.labelProdFornecedor.setObjectName(u"labelProdFornecedor")

        self.formProduto.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelProdFornecedor)

        self.cbProdFornecedor = QComboBox(self.grupoProduto)
        self.cbProdFornecedor.setObjectName(u"cbProdFornecedor")

        self.formProduto.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cbProdFornecedor)


        self.layoutProdutos.addWidget(self.grupoProduto)

        self.botoesProduto = QHBoxLayout()
        self.botoesProduto.setObjectName(u"botoesProduto")
        self.btnProdSalvar = QPushButton(self.abaProdutos)
        self.btnProdSalvar.setObjectName(u"btnProdSalvar")

        self.botoesProduto.addWidget(self.btnProdSalvar)

        self.btnProdAlterar = QPushButton(self.abaProdutos)
        self.btnProdAlterar.setObjectName(u"btnProdAlterar")

        self.botoesProduto.addWidget(self.btnProdAlterar)

        self.btnProdExcluir = QPushButton(self.abaProdutos)
        self.btnProdExcluir.setObjectName(u"btnProdExcluir")

        self.botoesProduto.addWidget(self.btnProdExcluir)

        self.btnProdLimpar = QPushButton(self.abaProdutos)
        self.btnProdLimpar.setObjectName(u"btnProdLimpar")

        self.botoesProduto.addWidget(self.btnProdLimpar)


        self.layoutProdutos.addLayout(self.botoesProduto)

        self.tabelaProdutos = QTableWidget(self.abaProdutos)
        if (self.tabelaProdutos.columnCount() < 5):
            self.tabelaProdutos.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tabelaProdutos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tabelaProdutos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tabelaProdutos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tabelaProdutos.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tabelaProdutos.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tabelaProdutos.setObjectName(u"tabelaProdutos")
        self.tabelaProdutos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelaProdutos.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelaProdutos.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelaProdutos.horizontalHeader().setStretchLastSection(True)
        self.tabelaProdutos.verticalHeader().setVisible(False)

        self.layoutProdutos.addWidget(self.tabelaProdutos)

        self.abas.addTab(self.abaProdutos, "")
        self.abaFornecedores = QWidget()
        self.abaFornecedores.setObjectName(u"abaFornecedores")
        self.layoutFornecedores = QVBoxLayout(self.abaFornecedores)
        self.layoutFornecedores.setObjectName(u"layoutFornecedores")
        self.grupoFornecedor = QGroupBox(self.abaFornecedores)
        self.grupoFornecedor.setObjectName(u"grupoFornecedor")
        self.formFornecedor = QFormLayout(self.grupoFornecedor)
        self.formFornecedor.setObjectName(u"formFornecedor")
        self.labelFornNome = QLabel(self.grupoFornecedor)
        self.labelFornNome.setObjectName(u"labelFornNome")

        self.formFornecedor.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelFornNome)

        self.txtFornNome = QLineEdit(self.grupoFornecedor)
        self.txtFornNome.setObjectName(u"txtFornNome")

        self.formFornecedor.setWidget(0, QFormLayout.ItemRole.FieldRole, self.txtFornNome)

        self.labelFornContato = QLabel(self.grupoFornecedor)
        self.labelFornContato.setObjectName(u"labelFornContato")

        self.formFornecedor.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelFornContato)

        self.txtFornContato = QLineEdit(self.grupoFornecedor)
        self.txtFornContato.setObjectName(u"txtFornContato")

        self.formFornecedor.setWidget(1, QFormLayout.ItemRole.FieldRole, self.txtFornContato)

        self.labelFornEmail = QLabel(self.grupoFornecedor)
        self.labelFornEmail.setObjectName(u"labelFornEmail")

        self.formFornecedor.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelFornEmail)

        self.txtFornEmail = QLineEdit(self.grupoFornecedor)
        self.txtFornEmail.setObjectName(u"txtFornEmail")

        self.formFornecedor.setWidget(2, QFormLayout.ItemRole.FieldRole, self.txtFornEmail)

        self.labelFornEndereco = QLabel(self.grupoFornecedor)
        self.labelFornEndereco.setObjectName(u"labelFornEndereco")

        self.formFornecedor.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelFornEndereco)

        self.txtFornEndereco = QLineEdit(self.grupoFornecedor)
        self.txtFornEndereco.setObjectName(u"txtFornEndereco")

        self.formFornecedor.setWidget(3, QFormLayout.ItemRole.FieldRole, self.txtFornEndereco)


        self.layoutFornecedores.addWidget(self.grupoFornecedor)

        self.botoesFornecedor = QHBoxLayout()
        self.botoesFornecedor.setObjectName(u"botoesFornecedor")
        self.btnFornSalvar = QPushButton(self.abaFornecedores)
        self.btnFornSalvar.setObjectName(u"btnFornSalvar")

        self.botoesFornecedor.addWidget(self.btnFornSalvar)

        self.btnFornAlterar = QPushButton(self.abaFornecedores)
        self.btnFornAlterar.setObjectName(u"btnFornAlterar")

        self.botoesFornecedor.addWidget(self.btnFornAlterar)

        self.btnFornExcluir = QPushButton(self.abaFornecedores)
        self.btnFornExcluir.setObjectName(u"btnFornExcluir")

        self.botoesFornecedor.addWidget(self.btnFornExcluir)

        self.btnFornLimpar = QPushButton(self.abaFornecedores)
        self.btnFornLimpar.setObjectName(u"btnFornLimpar")

        self.botoesFornecedor.addWidget(self.btnFornLimpar)


        self.layoutFornecedores.addLayout(self.botoesFornecedor)

        self.tabelaFornecedores = QTableWidget(self.abaFornecedores)
        if (self.tabelaFornecedores.columnCount() < 5):
            self.tabelaFornecedores.setColumnCount(5)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tabelaFornecedores.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tabelaFornecedores.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tabelaFornecedores.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tabelaFornecedores.setHorizontalHeaderItem(3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tabelaFornecedores.setHorizontalHeaderItem(4, __qtablewidgetitem9)
        self.tabelaFornecedores.setObjectName(u"tabelaFornecedores")
        self.tabelaFornecedores.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelaFornecedores.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelaFornecedores.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelaFornecedores.horizontalHeader().setStretchLastSection(True)
        self.tabelaFornecedores.verticalHeader().setVisible(False)

        self.layoutFornecedores.addWidget(self.tabelaFornecedores)

        self.abas.addTab(self.abaFornecedores, "")
        self.abaClientes = QWidget()
        self.abaClientes.setObjectName(u"abaClientes")
        self.layoutClientes = QVBoxLayout(self.abaClientes)
        self.layoutClientes.setObjectName(u"layoutClientes")
        self.grupoCliente = QGroupBox(self.abaClientes)
        self.grupoCliente.setObjectName(u"grupoCliente")
        self.formCliente = QFormLayout(self.grupoCliente)
        self.formCliente.setObjectName(u"formCliente")
        self.labelCliNome = QLabel(self.grupoCliente)
        self.labelCliNome.setObjectName(u"labelCliNome")

        self.formCliente.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCliNome)

        self.txtCliNome = QLineEdit(self.grupoCliente)
        self.txtCliNome.setObjectName(u"txtCliNome")

        self.formCliente.setWidget(0, QFormLayout.ItemRole.FieldRole, self.txtCliNome)

        self.labelCliContato = QLabel(self.grupoCliente)
        self.labelCliContato.setObjectName(u"labelCliContato")

        self.formCliente.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelCliContato)

        self.txtCliContato = QLineEdit(self.grupoCliente)
        self.txtCliContato.setObjectName(u"txtCliContato")

        self.formCliente.setWidget(1, QFormLayout.ItemRole.FieldRole, self.txtCliContato)

        self.labelCliEmail = QLabel(self.grupoCliente)
        self.labelCliEmail.setObjectName(u"labelCliEmail")

        self.formCliente.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelCliEmail)

        self.txtCliEmail = QLineEdit(self.grupoCliente)
        self.txtCliEmail.setObjectName(u"txtCliEmail")

        self.formCliente.setWidget(2, QFormLayout.ItemRole.FieldRole, self.txtCliEmail)

        self.labelCliEndereco = QLabel(self.grupoCliente)
        self.labelCliEndereco.setObjectName(u"labelCliEndereco")

        self.formCliente.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelCliEndereco)

        self.txtCliEndereco = QLineEdit(self.grupoCliente)
        self.txtCliEndereco.setObjectName(u"txtCliEndereco")

        self.formCliente.setWidget(3, QFormLayout.ItemRole.FieldRole, self.txtCliEndereco)


        self.layoutClientes.addWidget(self.grupoCliente)

        self.botoesCliente = QHBoxLayout()
        self.botoesCliente.setObjectName(u"botoesCliente")
        self.btnCliSalvar = QPushButton(self.abaClientes)
        self.btnCliSalvar.setObjectName(u"btnCliSalvar")

        self.botoesCliente.addWidget(self.btnCliSalvar)

        self.btnCliAlterar = QPushButton(self.abaClientes)
        self.btnCliAlterar.setObjectName(u"btnCliAlterar")

        self.botoesCliente.addWidget(self.btnCliAlterar)

        self.btnCliExcluir = QPushButton(self.abaClientes)
        self.btnCliExcluir.setObjectName(u"btnCliExcluir")

        self.botoesCliente.addWidget(self.btnCliExcluir)

        self.btnCliLimpar = QPushButton(self.abaClientes)
        self.btnCliLimpar.setObjectName(u"btnCliLimpar")

        self.botoesCliente.addWidget(self.btnCliLimpar)


        self.layoutClientes.addLayout(self.botoesCliente)

        self.tabelaClientes = QTableWidget(self.abaClientes)
        if (self.tabelaClientes.columnCount() < 5):
            self.tabelaClientes.setColumnCount(5)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tabelaClientes.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tabelaClientes.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tabelaClientes.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tabelaClientes.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tabelaClientes.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        self.tabelaClientes.setObjectName(u"tabelaClientes")
        self.tabelaClientes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelaClientes.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelaClientes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelaClientes.horizontalHeader().setStretchLastSection(True)
        self.tabelaClientes.verticalHeader().setVisible(False)

        self.layoutClientes.addWidget(self.tabelaClientes)

        self.abas.addTab(self.abaClientes, "")
        self.abaCompras = QWidget()
        self.abaCompras.setObjectName(u"abaCompras")
        self.layoutCompras = QVBoxLayout(self.abaCompras)
        self.layoutCompras.setObjectName(u"layoutCompras")
        self.grupoCompra = QGroupBox(self.abaCompras)
        self.grupoCompra.setObjectName(u"grupoCompra")
        self.formCompra = QFormLayout(self.grupoCompra)
        self.formCompra.setObjectName(u"formCompra")
        self.labelCompraCliente = QLabel(self.grupoCompra)
        self.labelCompraCliente.setObjectName(u"labelCompraCliente")

        self.formCompra.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCompraCliente)

        self.cbCompraCliente = QComboBox(self.grupoCompra)
        self.cbCompraCliente.setObjectName(u"cbCompraCliente")

        self.formCompra.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbCompraCliente)

        self.labelCompraProduto = QLabel(self.grupoCompra)
        self.labelCompraProduto.setObjectName(u"labelCompraProduto")

        self.formCompra.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelCompraProduto)

        self.cbCompraProduto = QComboBox(self.grupoCompra)
        self.cbCompraProduto.setObjectName(u"cbCompraProduto")

        self.formCompra.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbCompraProduto)

        self.labelCompraQtd = QLabel(self.grupoCompra)
        self.labelCompraQtd.setObjectName(u"labelCompraQtd")

        self.formCompra.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelCompraQtd)

        self.spinCompraQtd = QSpinBox(self.grupoCompra)
        self.spinCompraQtd.setObjectName(u"spinCompraQtd")
        self.spinCompraQtd.setMinimum(1)
        self.spinCompraQtd.setMaximum(99999)

        self.formCompra.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spinCompraQtd)

        self.labelCompraFiado = QLabel(self.grupoCompra)
        self.labelCompraFiado.setObjectName(u"labelCompraFiado")

        self.formCompra.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelCompraFiado)

        self.checkCompraFiado = QCheckBox(self.grupoCompra)
        self.checkCompraFiado.setObjectName(u"checkCompraFiado")

        self.formCompra.setWidget(3, QFormLayout.ItemRole.FieldRole, self.checkCompraFiado)

        self.labelCompraTotalTexto = QLabel(self.grupoCompra)
        self.labelCompraTotalTexto.setObjectName(u"labelCompraTotalTexto")

        self.formCompra.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelCompraTotalTexto)

        self.labelCompraTotal = QLabel(self.grupoCompra)
        self.labelCompraTotal.setObjectName(u"labelCompraTotal")
        font1 = QFont()
        font1.setBold(True)
        self.labelCompraTotal.setFont(font1)

        self.formCompra.setWidget(4, QFormLayout.ItemRole.FieldRole, self.labelCompraTotal)


        self.layoutCompras.addWidget(self.grupoCompra)

        self.botoesCompra = QHBoxLayout()
        self.botoesCompra.setObjectName(u"botoesCompra")
        self.btnCompraRegistrar = QPushButton(self.abaCompras)
        self.btnCompraRegistrar.setObjectName(u"btnCompraRegistrar")

        self.botoesCompra.addWidget(self.btnCompraRegistrar)

        self.btnCompraCancelar = QPushButton(self.abaCompras)
        self.btnCompraCancelar.setObjectName(u"btnCompraCancelar")

        self.botoesCompra.addWidget(self.btnCompraCancelar)


        self.layoutCompras.addLayout(self.botoesCompra)

        self.tabelaCompras = QTableWidget(self.abaCompras)
        if (self.tabelaCompras.columnCount() < 6):
            self.tabelaCompras.setColumnCount(6)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tabelaCompras.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tabelaCompras.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tabelaCompras.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tabelaCompras.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tabelaCompras.setHorizontalHeaderItem(4, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tabelaCompras.setHorizontalHeaderItem(5, __qtablewidgetitem20)
        self.tabelaCompras.setObjectName(u"tabelaCompras")
        self.tabelaCompras.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelaCompras.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelaCompras.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelaCompras.horizontalHeader().setStretchLastSection(True)
        self.tabelaCompras.verticalHeader().setVisible(False)

        self.layoutCompras.addWidget(self.tabelaCompras)

        self.abas.addTab(self.abaCompras, "")
        self.abaDevedores = QWidget()
        self.abaDevedores.setObjectName(u"abaDevedores")
        self.layoutDevedores = QVBoxLayout(self.abaDevedores)
        self.layoutDevedores.setObjectName(u"layoutDevedores")
        self.layoutGruposDevedores = QHBoxLayout()
        self.layoutGruposDevedores.setObjectName(u"layoutGruposDevedores")
        self.grupoNovaDivida = QGroupBox(self.abaDevedores)
        self.grupoNovaDivida.setObjectName(u"grupoNovaDivida")
        self.formNovaDivida = QFormLayout(self.grupoNovaDivida)
        self.formNovaDivida.setObjectName(u"formNovaDivida")
        self.labelDevCliente = QLabel(self.grupoNovaDivida)
        self.labelDevCliente.setObjectName(u"labelDevCliente")

        self.formNovaDivida.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelDevCliente)

        self.cbDevCliente = QComboBox(self.grupoNovaDivida)
        self.cbDevCliente.setObjectName(u"cbDevCliente")

        self.formNovaDivida.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbDevCliente)

        self.labelDevValor = QLabel(self.grupoNovaDivida)
        self.labelDevValor.setObjectName(u"labelDevValor")

        self.formNovaDivida.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelDevValor)

        self.spinDevValor = QDoubleSpinBox(self.grupoNovaDivida)
        self.spinDevValor.setObjectName(u"spinDevValor")
        self.spinDevValor.setMaximum(99999.990000000005239)

        self.formNovaDivida.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinDevValor)

        self.labelDevDescricao = QLabel(self.grupoNovaDivida)
        self.labelDevDescricao.setObjectName(u"labelDevDescricao")

        self.formNovaDivida.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelDevDescricao)

        self.txtDevDescricao = QLineEdit(self.grupoNovaDivida)
        self.txtDevDescricao.setObjectName(u"txtDevDescricao")

        self.formNovaDivida.setWidget(2, QFormLayout.ItemRole.FieldRole, self.txtDevDescricao)

        self.btnDevRegistrar = QPushButton(self.grupoNovaDivida)
        self.btnDevRegistrar.setObjectName(u"btnDevRegistrar")

        self.formNovaDivida.setWidget(3, QFormLayout.ItemRole.FieldRole, self.btnDevRegistrar)


        self.layoutGruposDevedores.addWidget(self.grupoNovaDivida)

        self.grupoPagamento = QGroupBox(self.abaDevedores)
        self.grupoPagamento.setObjectName(u"grupoPagamento")
        self.formPagamento = QFormLayout(self.grupoPagamento)
        self.formPagamento.setObjectName(u"formPagamento")
        self.labelDevPagamento = QLabel(self.grupoPagamento)
        self.labelDevPagamento.setObjectName(u"labelDevPagamento")

        self.formPagamento.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelDevPagamento)

        self.spinDevPagamento = QDoubleSpinBox(self.grupoPagamento)
        self.spinDevPagamento.setObjectName(u"spinDevPagamento")
        self.spinDevPagamento.setMaximum(99999.990000000005239)

        self.formPagamento.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spinDevPagamento)

        self.btnDevPagar = QPushButton(self.grupoPagamento)
        self.btnDevPagar.setObjectName(u"btnDevPagar")

        self.formPagamento.setWidget(1, QFormLayout.ItemRole.FieldRole, self.btnDevPagar)


        self.layoutGruposDevedores.addWidget(self.grupoPagamento)


        self.layoutDevedores.addLayout(self.layoutGruposDevedores)

        self.tabelaDevedores = QTableWidget(self.abaDevedores)
        if (self.tabelaDevedores.columnCount() < 5):
            self.tabelaDevedores.setColumnCount(5)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tabelaDevedores.setHorizontalHeaderItem(0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tabelaDevedores.setHorizontalHeaderItem(1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tabelaDevedores.setHorizontalHeaderItem(2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tabelaDevedores.setHorizontalHeaderItem(3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tabelaDevedores.setHorizontalHeaderItem(4, __qtablewidgetitem25)
        self.tabelaDevedores.setObjectName(u"tabelaDevedores")
        self.tabelaDevedores.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelaDevedores.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelaDevedores.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelaDevedores.horizontalHeader().setStretchLastSection(True)
        self.tabelaDevedores.verticalHeader().setVisible(False)

        self.layoutDevedores.addWidget(self.tabelaDevedores)

        self.labelDevTotal = QLabel(self.abaDevedores)
        self.labelDevTotal.setObjectName(u"labelDevTotal")
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.labelDevTotal.setFont(font2)
        self.labelDevTotal.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.layoutDevedores.addWidget(self.labelDevTotal)

        self.abas.addTab(self.abaDevedores, "")

        self.layoutPrincipal.addWidget(self.abas)

        JanelaPrincipal.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(JanelaPrincipal)
        self.statusbar.setObjectName(u"statusbar")
        JanelaPrincipal.setStatusBar(self.statusbar)

        self.retranslateUi(JanelaPrincipal)

        self.abas.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(JanelaPrincipal)
    # setupUi

    def retranslateUi(self, JanelaPrincipal):
        JanelaPrincipal.setWindowTitle(QCoreApplication.translate("JanelaPrincipal", u"Loja de Pipas", None))
        self.labelTitulo.setText(QCoreApplication.translate("JanelaPrincipal", u"Loja de Pipas", None))
        self.grupoProduto.setTitle(QCoreApplication.translate("JanelaPrincipal", u"Dados do produto", None))
        self.labelProdNome.setText(QCoreApplication.translate("JanelaPrincipal", u"Nome:", None))
        self.labelProdPreco.setText(QCoreApplication.translate("JanelaPrincipal", u"Pre\u00e7o:", None))
        self.spinProdPreco.setPrefix(QCoreApplication.translate("JanelaPrincipal", u"R$ ", None))
        self.labelProdEstoque.setText(QCoreApplication.translate("JanelaPrincipal", u"Estoque:", None))
        self.labelProdFornecedor.setText(QCoreApplication.translate("JanelaPrincipal", u"Fornecedor:", None))
        self.btnProdSalvar.setText(QCoreApplication.translate("JanelaPrincipal", u"Cadastrar", None))
        self.btnProdAlterar.setText(QCoreApplication.translate("JanelaPrincipal", u"Alterar", None))
        self.btnProdExcluir.setText(QCoreApplication.translate("JanelaPrincipal", u"Excluir", None))
        self.btnProdLimpar.setText(QCoreApplication.translate("JanelaPrincipal", u"Limpar", None))
        ___qtablewidgetitem = self.tabelaProdutos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("JanelaPrincipal", u"ID", None))
        ___qtablewidgetitem1 = self.tabelaProdutos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("JanelaPrincipal", u"Nome", None))
        ___qtablewidgetitem2 = self.tabelaProdutos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("JanelaPrincipal", u"Pre\u00e7o", None))
        ___qtablewidgetitem3 = self.tabelaProdutos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("JanelaPrincipal", u"Estoque", None))
        ___qtablewidgetitem4 = self.tabelaProdutos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("JanelaPrincipal", u"Fornecedor", None))
        self.abas.setTabText(self.abas.indexOf(self.abaProdutos), QCoreApplication.translate("JanelaPrincipal", u"Produtos", None))
        self.grupoFornecedor.setTitle(QCoreApplication.translate("JanelaPrincipal", u"Dados do fornecedor", None))
        self.labelFornNome.setText(QCoreApplication.translate("JanelaPrincipal", u"Nome:", None))
        self.labelFornContato.setText(QCoreApplication.translate("JanelaPrincipal", u"Contato:", None))
        self.labelFornEmail.setText(QCoreApplication.translate("JanelaPrincipal", u"Email:", None))
        self.labelFornEndereco.setText(QCoreApplication.translate("JanelaPrincipal", u"Endere\u00e7o:", None))
        self.btnFornSalvar.setText(QCoreApplication.translate("JanelaPrincipal", u"Cadastrar", None))
        self.btnFornAlterar.setText(QCoreApplication.translate("JanelaPrincipal", u"Alterar", None))
        self.btnFornExcluir.setText(QCoreApplication.translate("JanelaPrincipal", u"Excluir", None))
        self.btnFornLimpar.setText(QCoreApplication.translate("JanelaPrincipal", u"Limpar", None))
        ___qtablewidgetitem5 = self.tabelaFornecedores.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("JanelaPrincipal", u"ID", None))
        ___qtablewidgetitem6 = self.tabelaFornecedores.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("JanelaPrincipal", u"Nome", None))
        ___qtablewidgetitem7 = self.tabelaFornecedores.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("JanelaPrincipal", u"Contato", None))
        ___qtablewidgetitem8 = self.tabelaFornecedores.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("JanelaPrincipal", u"Email", None))
        ___qtablewidgetitem9 = self.tabelaFornecedores.horizontalHeaderItem(4)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("JanelaPrincipal", u"Endere\u00e7o", None))
        self.abas.setTabText(self.abas.indexOf(self.abaFornecedores), QCoreApplication.translate("JanelaPrincipal", u"Fornecedores", None))
        self.grupoCliente.setTitle(QCoreApplication.translate("JanelaPrincipal", u"Dados do cliente", None))
        self.labelCliNome.setText(QCoreApplication.translate("JanelaPrincipal", u"Nome:", None))
        self.labelCliContato.setText(QCoreApplication.translate("JanelaPrincipal", u"Contato:", None))
        self.labelCliEmail.setText(QCoreApplication.translate("JanelaPrincipal", u"Email:", None))
        self.labelCliEndereco.setText(QCoreApplication.translate("JanelaPrincipal", u"Endere\u00e7o:", None))
        self.btnCliSalvar.setText(QCoreApplication.translate("JanelaPrincipal", u"Cadastrar", None))
        self.btnCliAlterar.setText(QCoreApplication.translate("JanelaPrincipal", u"Alterar", None))
        self.btnCliExcluir.setText(QCoreApplication.translate("JanelaPrincipal", u"Excluir", None))
        self.btnCliLimpar.setText(QCoreApplication.translate("JanelaPrincipal", u"Limpar", None))
        ___qtablewidgetitem10 = self.tabelaClientes.horizontalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("JanelaPrincipal", u"ID", None))
        ___qtablewidgetitem11 = self.tabelaClientes.horizontalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("JanelaPrincipal", u"Nome", None))
        ___qtablewidgetitem12 = self.tabelaClientes.horizontalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("JanelaPrincipal", u"Contato", None))
        ___qtablewidgetitem13 = self.tabelaClientes.horizontalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("JanelaPrincipal", u"Email", None))
        ___qtablewidgetitem14 = self.tabelaClientes.horizontalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("JanelaPrincipal", u"Endere\u00e7o", None))
        self.abas.setTabText(self.abas.indexOf(self.abaClientes), QCoreApplication.translate("JanelaPrincipal", u"Clientes", None))
        self.grupoCompra.setTitle(QCoreApplication.translate("JanelaPrincipal", u"Nova compra", None))
        self.labelCompraCliente.setText(QCoreApplication.translate("JanelaPrincipal", u"Cliente:", None))
        self.labelCompraProduto.setText(QCoreApplication.translate("JanelaPrincipal", u"Produto:", None))
        self.labelCompraQtd.setText(QCoreApplication.translate("JanelaPrincipal", u"Quantidade:", None))
        self.labelCompraFiado.setText(QCoreApplication.translate("JanelaPrincipal", u"Pagamento:", None))
        self.checkCompraFiado.setText(QCoreApplication.translate("JanelaPrincipal", u"Fiado (lan\u00e7ar como d\u00edvida do cliente)", None))
        self.labelCompraTotalTexto.setText(QCoreApplication.translate("JanelaPrincipal", u"Total:", None))
        self.labelCompraTotal.setText(QCoreApplication.translate("JanelaPrincipal", u"R$ 0.00", None))
        self.btnCompraRegistrar.setText(QCoreApplication.translate("JanelaPrincipal", u"Registrar compra", None))
        self.btnCompraCancelar.setText(QCoreApplication.translate("JanelaPrincipal", u"Cancelar compra selecionada", None))
        ___qtablewidgetitem15 = self.tabelaCompras.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("JanelaPrincipal", u"ID", None))
        ___qtablewidgetitem16 = self.tabelaCompras.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("JanelaPrincipal", u"Data", None))
        ___qtablewidgetitem17 = self.tabelaCompras.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("JanelaPrincipal", u"Cliente", None))
        ___qtablewidgetitem18 = self.tabelaCompras.horizontalHeaderItem(3)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("JanelaPrincipal", u"Produto", None))
        ___qtablewidgetitem19 = self.tabelaCompras.horizontalHeaderItem(4)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("JanelaPrincipal", u"Quantidade", None))
        ___qtablewidgetitem20 = self.tabelaCompras.horizontalHeaderItem(5)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("JanelaPrincipal", u"Total", None))
        self.abas.setTabText(self.abas.indexOf(self.abaCompras), QCoreApplication.translate("JanelaPrincipal", u"Compras", None))
        self.grupoNovaDivida.setTitle(QCoreApplication.translate("JanelaPrincipal", u"Nova d\u00edvida", None))
        self.labelDevCliente.setText(QCoreApplication.translate("JanelaPrincipal", u"Cliente:", None))
        self.labelDevValor.setText(QCoreApplication.translate("JanelaPrincipal", u"Valor:", None))
        self.spinDevValor.setPrefix(QCoreApplication.translate("JanelaPrincipal", u"R$ ", None))
        self.labelDevDescricao.setText(QCoreApplication.translate("JanelaPrincipal", u"Descri\u00e7\u00e3o:", None))
        self.btnDevRegistrar.setText(QCoreApplication.translate("JanelaPrincipal", u"Registrar d\u00edvida", None))
        self.grupoPagamento.setTitle(QCoreApplication.translate("JanelaPrincipal", u"Pagamento da d\u00edvida selecionada", None))
        self.labelDevPagamento.setText(QCoreApplication.translate("JanelaPrincipal", u"Valor pago:", None))
        self.spinDevPagamento.setPrefix(QCoreApplication.translate("JanelaPrincipal", u"R$ ", None))
        self.btnDevPagar.setText(QCoreApplication.translate("JanelaPrincipal", u"Registrar pagamento", None))
        ___qtablewidgetitem21 = self.tabelaDevedores.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("JanelaPrincipal", u"ID", None))
        ___qtablewidgetitem22 = self.tabelaDevedores.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("JanelaPrincipal", u"Cliente", None))
        ___qtablewidgetitem23 = self.tabelaDevedores.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("JanelaPrincipal", u"Valor", None))
        ___qtablewidgetitem24 = self.tabelaDevedores.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("JanelaPrincipal", u"Data", None))
        ___qtablewidgetitem25 = self.tabelaDevedores.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("JanelaPrincipal", u"Descri\u00e7\u00e3o", None))
        self.labelDevTotal.setText(QCoreApplication.translate("JanelaPrincipal", u"Total a receber: R$ 0.00", None))
        self.abas.setTabText(self.abas.indexOf(self.abaDevedores), QCoreApplication.translate("JanelaPrincipal", u"Devedores", None))
    # retranslateUi

