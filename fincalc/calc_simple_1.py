""" Простая версия калькулятора NPV
напишем основу класса CashFlow: 
можно ввести процентную ставку (поле ввода txt_rate),
есть кнопка "+" (button_plus) для добавления элементов денежного потока
при нажатии на кнопку добавляются элементы  методом add_fa():
новый виджет класса FutureAmount ставится в макет layout_famounts
CashFlow ведет список этих элементов в свойстве amounts 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton)


def discount(sum, period, rate):
    """ возвращает дисконтированную стоимость"""
    return sum  # заглушка, пока пробуем так


class FutureAmount(QWidget):
    """ Одна строчка таблицы.  """

    def __init__(self, amount=0, years=0, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)  # создаём базовый виджет
        # запоминаем параметры, с которыми создаётся экзмепляр:
        self.years = years
        self.amount = amount
        # размещаем визуальные элементы:
        self.create_widgets()
        # подключаем сигналы и показываем строку:
        self.recalc()  # один раз вызываем вручную, чтобы просчитать значения из конструктора
        self.connects()

    def create_widgets(self):
        """ создаёт внутренние виджеты и вызывает метод их размещения"""
        self.txt_amount = QLineEdit(str(self.amount))
        self.txt_years = QLineEdit(str(self.years))
        self.lbl_pv = QLabel()  # расчетную сумму (present value) нельзя редактировать
        self.lay_widgets()

    def lay_widgets(self):
        """ размещает внутренние виджеты в строку"""
        layout_h = QHBoxLayout()
        layout_h.addWidget(self.txt_years)
        layout_h.addStretch(1)
        layout_h.addWidget(self.txt_amount)
        layout_h.addStretch(1)
        layout_h.addWidget(self.lbl_pv)
        self.setLayout(layout_h)

    def connects(self):
        """ внутри строки пересчитывается текущая стоимость, если изменено любое число"""
        self.txt_amount.editingFinished.connect(self.recalc)
        self.txt_years.editingFinished.connect(self.recalc)

    def recalc(self):
        """ пересчитывает значения свойств класса, устанавливает нужную сумму в соотв. надпись """
        sum = float(self.txt_amount.text())
        period = int(self.txt_years.text())
        result = discount(sum, period, 0)  # расчет (ставку пока не делаем)
        self.lbl_pv.setText(str(result))  # отрисовка


class CashFlow(QWidget):
    """ класс "Поток" хранит строки, из которых складывается денежный поток """

    def __init__(self, rate=0.0, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        # запоминаем параметры:
        self.rate = rate
        self.NPV = 0
        # список будущих сумм:
        self.amounts = []

        # размещаем визуальные элементы:
        self.create_widgets()
        # подключаем сигналы и показываем:
        self.connects()
        self.show()

    def add_fa(self):
        """ добавляет одну будущую сумму"""
        fa = FutureAmount()
        self.amounts.append(fa)  # держим список сумм
        self.layout_famounts.addWidget(fa)  # отрисовка

    def connects(self):
        """ подключает обработку действий пользователя """
        self.button_plus.clicked.connect(self.add_fa)

    def create_widgets(self):
        """ создаёт внутренние виджеты и вызывает метод их размещения"""
        # ввод ставки:
        self.lbl_rate1 = QLabel('ставка:')
        self.txt_rate = QLineEdit('0')
        self.lbl_rate2 = QLabel('процентов')
        # результат:
        self.lbl_result1 = QLabel('Итог:')
        self.lbl_npv = QLabel(str(self.NPV))
        self.lbl_result2 = QLabel(' рублей')
        # кнопки "OK" и "+" в конце всех строк:
        self.button_plus = QPushButton(' + ')
        # теперь разместить
        self.lay_widgets()

    def lay_widgets(self):
        """ размещает виджеты в столбец, 
        при этом одна из ячеек этого столбца - layout, 
        в который будут добавляться виджеты типа FutureAmount """
        self.layout_main = QVBoxLayout()
        self.layout_famounts = QVBoxLayout()
        layout_top = QHBoxLayout()  # верхняя строка
        layout_bottom = QHBoxLayout()  # нижняя строка
        # расставляем виджеты:
        layout_top.addWidget(self.lbl_rate1, alignment=Qt.AlignRight)
        layout_top.addWidget(self.txt_rate)
        layout_top.addWidget(self.lbl_rate2, alignment=Qt.AlignLeft)

        layout_bottom.addWidget(self.lbl_result1, alignment=Qt.AlignRight)
        layout_bottom.addWidget(self.lbl_npv)
        layout_bottom.addWidget(self.lbl_result2, alignment=Qt.AlignLeft)
        layout_bottom.addStretch(2)
        layout_bottom.addWidget(self.button_plus, alignment=Qt.AlignRight)

        # формируем общий макет:
        self.layout_main.addLayout(layout_top)
        self.layout_main.addLayout(layout_bottom)
        self.layout_main.addLayout(self.layout_famounts)

        self.setLayout(self.layout_main)


# Проверка, что пока все работает:
app = QApplication([])
main_w = CashFlow()

app.exec()
