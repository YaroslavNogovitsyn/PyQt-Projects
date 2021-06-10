""" Калькулятор NPV, версия с улучшенным интерфейсом: используется макет "таблица" (QGridLayout)

добавляем строки внутрь таблицы: 
объект класса FutureAmount должен получить макет типа QGridLayout и номер строки (в __init__() ),
он разместит свои виджеты в эту строку (поменяли lay_widgets и стали вызывать непосредственно из конструктора)

в классе CashFlow
-   метод add_table (вынесли туда часть lay_widgets, касающаяся таблицы) 
    создает макет layout_famounts, и он теперь таблица, а не столбец
    создает свойство rows (сколько строк уже есть)
-   поменяли метод add_fa (передаем нужные параметры)

"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton)


def discount(amount, periods, rate):
    """ возвращает дисконтированную стоимость"""
    rate = rate / 100  # перейдем от процентов к обычному числу
    compound = pow(1 + rate, periods)  # столько всего набежало сложных процентов за переданное число периодов
    return round(amount / compound, 4)


class FutureAmount(QWidget):
    """ Одна строчка таблицы.  """

    def __init__(self, grid, row, rate_widget, amount=0, years=0, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)  # создаём базовый виджет
        # запоминаем параметры, с которыми создаётся экзмепляр:
        # это поле ввода процентной ставки, будем каждый раз при пересчете брать оттуда число
        self.rate_widget = rate_widget
        self.years = years
        self.amount = amount
        # размещаем визуальные элементы:
        self.create_widgets()
        self.lay_widgets(grid, row)  # не вызываем больше этот метод из create_widgets, а
        # вызываем отсюда, чтобы удобнее было передать параметры
        # grid (макет типа таблица), row (номер строки)
        # подключаем сигналы и показываем строку:
        self.recalc()  # один раз вызываем вручную, чтобы просчитать значения из конструктора
        self.connects()

    def create_widgets(self):
        """ создаёт внутренние виджеты и вызывает метод их размещения"""
        self.txt_amount = QLineEdit(str(self.amount))
        self.txt_years = QLineEdit(str(self.years))
        self.lbl_pv = QLabel()  # расчетную сумму (present value) нельзя редактировать

    def lay_widgets(self, grid, row):
        """ размещает внутренние виджеты в строку номер row макета grid"""
        grid.addWidget(self.txt_years, row, 0)  # это - в столбец 0
        grid.addWidget(self.txt_amount, row, 2)  # столбец 1 - пустой (для разрывов), а это - в столбец 2
        grid.addWidget(self.lbl_pv, row, 4)  # аналогично, пропустили столбец 3

    def connects(self):
        """ внутри строки пересчитывается текущая стоимость, если изменено любое число"""
        self.txt_amount.editingFinished.connect(self.recalc)
        self.txt_years.editingFinished.connect(self.recalc)

    def recalc(self):
        """ пересчитывает значения свойств класса, устанавливает нужную сумму в соотв. надпись """
        rate = float(self.rate_widget.text())
        sum = float(self.txt_amount.text())
        period = int(self.txt_years.text())
        result = discount(sum, period, rate)  # расчет (ставку пока не делаем)
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

    def recalc(self):
        """ суммирует итог по всем строкам """
        self.NPV = 0
        for future_amount in self.amounts:
            self.NPV += float(future_amount.lbl_pv.text())
        self.lbl_npv.setText(str(round(self.NPV, 4)))

    def recalc_them_all(self):
        """ пересчитывает все промежуточные суммы и общую"""
        for future_amount in self.amounts:
            future_amount.recalc()
        self.recalc()

    def add_fa(self):
        """ добавляет одну будущую сумму"""
        # строка в нужный layout с номером строки, равным общему количеству строк:
        fa = FutureAmount(self.layout_famounts, self.rows, self.txt_rate)
        # добавили одну строку, посчитаем её:
        self.rows += 1

        # добавим связи в изменениях параметров строки с общей суммой:
        fa.txt_amount.editingFinished.connect(self.recalc)
        fa.txt_years.editingFinished.connect(self.recalc)
        # запоминаем в списке:
        self.amounts.append(fa)
        self.layout_famounts.addWidget(fa)  # отрисовка

    def connects(self):
        """ подключает обработку действий пользователя """
        self.button_plus.clicked.connect(self.add_fa)
        self.txt_rate.editingFinished.connect(self.recalc_them_all)

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

    def add_table(self):
        """ добавляет макет таблицы для будущих сумм - layout_famounts
        составляет первую строку с подписями """
        self.layout_famounts = QGridLayout()
        self.rows = 0  # запоминаем, сколько строк уже добавлено
        # добавляем в строку self.rows и в столбцы 0, 1, 2, 3, 4 нужные надписи
        lbc1 = QLabel('лет')
        self.layout_famounts.addWidget(lbc1, self.rows, 0, alignment=Qt.AlignHCenter)
        self.layout_famounts.addWidget(QLabel('  '), self.rows, 1)
        lbc2 = QLabel('сумма')
        self.layout_famounts.addWidget(lbc2, self.rows, 2, alignment=Qt.AlignHCenter)
        self.layout_famounts.addWidget(QLabel('  '), self.rows, 3)
        lbc3 = QLabel('итог:')
        self.layout_famounts.addWidget(lbc3, self.rows, 4, alignment=Qt.AlignRight)
        # добавили одну строку:
        self.rows += 1

    def lay_widgets(self):
        """ размещает виджеты в столбец, 
        при этом одна из ячеек этого столбца - layout, 
        в который будут добавляться виджеты типа FutureAmount """
        self.layout_main = QVBoxLayout()
        # self.layout_famounts = QGridLayout()  - эту строку заменяем на:
        self.add_table()
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
