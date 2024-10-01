import sys
import numpy as np
import math_lib
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QPushButton, QWidget, QMessageBox, QLineEdit, QLabel
)

#второе окно, где происходит сама игра
class SecondWindow(QWidget):
    def __init__(self, rows, columns, mines):
        super().__init__()
        self.game = math_lib.Math_lib(rows, columns, mines)
        self.counter = 0
        self.visited = np.full((self.game.rows, self.game.columns), False)
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        for i in range(self.game.rows):
            for j in range(self.game.columns):
                button = QPushButton()
                self.grid.addWidget(button, i, j)
                button.clicked.connect(partial(self.push_button, i, j))

    def push_button(self, i, j):
        if self.visited[i][j] == True:
            return
        self.visited[i][j] = True
        self.counter = np.sum(self.visited)
        if self.game.field[i, j] == -1:
            self.grid.itemAtPosition(i, j).widget().setText("💣")
            self.end_game(False)

        else:
            mines = self.game.calculate_mines(i, j)
            if mines != 0:
                self.grid.itemAtPosition(i, j).widget().setText(str(mines))
                if self.counter == self.game.rows*self.game.columns - self.game.mines:
                    self.end_game(True)
            else:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if k == 0 and l == 0:
                            continue
                        if 0 <= i + k < self.game.rows and 0 <= j + l < self.game.columns:
                            mines2 = self.game.calculate_mines(i+k, j+l)
                            if mines2 == 0:
                                self.grid.itemAtPosition(i+k, j+l).widget().setText(str(mines2))
                                if self.counter == self.game.rows * self.game.columns - self.game.mines:
                                    self.end_game(True)
                                self.push_button(i+k, j+l)

                            else:
                                self.visited[i+k][j+l] = True
                                self.counter = np.sum(self.visited)
                                self.grid.itemAtPosition(i + k, j + l).widget().setText(str(mines2))
                                if self.counter == self.game.rows * self.game.columns - self.game.mines:
                                    self.end_game(True)

        return

    def end_game(self, result: bool):
        if result == False:
            QMessageBox.critical(self, 'Поражение', 'Поражение. Вы попали в мину')
            self.setEnabled(False)

            #отображение всех мин при поражении
            indices = np.where(self.game.field == -1)
            id = list(zip(indices[0], indices[1]))
            for i in id:
                self.grid.itemAtPosition(i[0], i[1]).widget().setText("💣")

            #очищение данных
            self.counter = 0
            self.game = None

        if result == True:
            QMessageBox.information(self, 'Победа', 'Победа! Вы избежали попадания в мину')
            self.setEnabled(False)

            #очищение данных
            self.counter = 0
            self.game = None



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #задание сетки
        grid = QGridLayout()
        self.setLayout(grid)

        self.label1 = QLabel('Кол-во строк')
        self.label2 = QLabel('Кол-во столбцов')
        self.label3 = QLabel('Кол-во мин')
        grid.addWidget(self.label1, 0, 0)
        grid.addWidget(self.label2, 0, 1)
        grid.addWidget(self.label3, 0, 2)


        #создание Line_Edit для задания размеров поля
        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        grid.addWidget(self.line1, 1, 0)
        grid.addWidget(self.line2, 1, 1)
        grid.addWidget(self.line3, 1, 2)

        #кнопка для открытия второго окна и начала игры
        self.button = QPushButton('Начать игру')
        grid.addWidget(self.button, 2, 0, 1, 3)
        self.button.clicked.connect(self.open_second_window)

        self.setWindowTitle('Minesweeper')
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def open_second_window(self):
        rows = int(self.line1.text())
        columns = int(self.line2.text())
        mines = int(self.line3.text())

        self.second_window = SecondWindow(rows, columns, mines)
        self.second_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start = MainWindow()
    sys.exit(app.exec_())
