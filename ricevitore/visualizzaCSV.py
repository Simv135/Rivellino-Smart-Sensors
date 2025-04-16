import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableView, QVBoxLayout,
    QWidget, QComboBox, QLabel, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QTimer


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None


class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizzatore CSV in tempo reale")
        self.setGeometry(100, 100, 1000, 700)

        # Widget centrale
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Selettore di file + checkbox scroll
        selector_layout = QHBoxLayout()
        self.label = QLabel("Seleziona un file CSV:")
        self.combo = QComboBox()
        self.combo.addItems([
            "allagamento.csv",
            "aria.csv",
            "batterie.csv",
            "temperatura_umidita.csv",
            "vibrazioni.csv"
        ])
        self.combo.currentIndexChanged.connect(self.update_selected_file)

        # Checkbox scroll automatico
        self.scroll_checkbox = QCheckBox("Scroll automatico")
        self.scroll_checkbox.setChecked(True)

        selector_layout.addWidget(self.label)
        selector_layout.addWidget(self.combo)
        selector_layout.addWidget(self.scroll_checkbox)
        self.layout.addLayout(selector_layout)

        # Tabella
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        self.df = None
        self.current_encoding = "iso-8859-1"
        self.current_file = self.combo.currentText()

        # Timer per aggiornamento automatico
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_file)
        self.timer.start(1000)  # ogni 1 secondo

        self.show()

    def update_selected_file(self):
        self.current_file = self.combo.currentText()
        self.load_file()

    def load_file(self):
        try:
            self.df = pd.read_csv(self.current_file, encoding=self.current_encoding)
            model = PandasModel(self.df)
            self.table_view.setModel(model)
            self.table_view.resizeColumnsToContents()
            self.setWindowTitle(f"CSV - {self.current_file}")

            # Scroll automatico se attivato
            if self.scroll_checkbox.isChecked() and self.df.shape[0] > 0:
                last_row_index = self.df.shape[0] - 1
                self.table_view.scrollToBottom()

        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Errore", f"Errore nell'apertura del file:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    sys.exit(app.exec_())
