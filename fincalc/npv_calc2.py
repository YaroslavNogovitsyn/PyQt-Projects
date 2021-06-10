""" Программа помогает в расчете NPV (чистая приведенная стоимость) денежного потока. 
Пользователь указывает суммы в какое-то время (через столько-то лет/месяцев), 
программа приводит все эти суммы к настоящему моменту.
Можно посмотреть, когда окупится какой-то проект, если в настоящем нужны определенные затраты,
а доходы будут в будущем.
"""

from PyQt5.QtCore import Qt, QLocale  # Qt - пространство имен, нужно для использования констант
# QLocale - нужно, чтобы переключать формат числа на американский, который только и понимает Python
from PyQt5.QtGui import QDoubleValidator, QIntValidator  # проверка типов вводимых значений
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,
                             QSpinBox, QLabel, QLineEdit, QPushButton)

QSS_LabelBold = """QLabel { 
    font: bold 20px;
}"""
QSS_Columns = """QLabel { 
    font: bold 14px "Courier New";
}"""


def fix_point(amount):
    """ корректирует строку, чтобы в любом случае вернуть число """
    try:
        result = float(amount)
        return result
    except ValueError:
        try:
            result = float(amount.replace(',', '.'))  # Qt разрешает вводить запятые даже с английской локалью...
            return result
        except ValueError:
            return 0  # если пользователь всё удалил, Qt пропустит такую строку.


def discount(amount, years, months, base, rate):
    """ функция вычисляет текущую стоимость будущей суммы amount
    на время - через years лет и months месяцев от сего дня
    по процентной ставке rate (процентов годовых).
    Параметр base говорит, как часто начисляются проценты (ожидается число от 1 до 12 месяцев) """
    # посчитаем, сколько раз за это время начислялись проценты:
    total_months = 12 * years + months
    periods = total_months // base  # вот столько раз
    tail = total_months % base  # столько месяцев прошло в последнем периоде, к ним применим простой процент

    # считаем, что ставка - это процент, который платится за base месяцев (т.е. не всегда проценты годовых!)
    rate = rate / 100  # перейдем от процентов к обычному числу
    # начисления в последнем периоде - по правилу простых процентов, т.е. просто пропорционально
    simple = 1 + (tail * rate) / base
    compound = pow(1 + rate, periods)  # столько всего набежало сложных процентов

    return round(amount / (simple * compound), 4)


class FutureAmount(QWidget):
    """ Одна строчка таблицы. 
    В строке приведена сумма и время (через сколько лет/месяцев это будет)
    Дисконтированная сумма пишется автоматически при вводе этих значений
    Для расчета нужно знать процентную ставку, поэтому строка хранит указатель на соответствующее поле ввода
    """

    def __init__(self, grid, row, rate_widget, base_widget, amount=0, years=0, months=0, parent=None,
                 flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)  # создаём базовый виджет
        # запоминаем параметры, с которыми создаётся экзмепляр:
        self.years = years
        self.months = months
        self.amount = amount
        self.rate_widget = rate_widget
        self.base_widget = base_widget
        # размещаем визуальные элементы:
        self.create_widgets()
        self.lay_widgets(grid, row)
        # подключаем сигналы и показываем строку:
        self.recalc()  # один раз вызываем вручную, чтобы просчитать значения из конструктора
        self.connects()

    def create_widgets(self):
        """ создаёт внутренние виджеты и вызывает метод их размещения"""
        self.txt_amount = QLineEdit(str(self.amount))
        loc = QLocale(QLocale.English, QLocale.UnitedStates)  # язык, страна
        validator = QDoubleValidator()
        validator.setLocale(loc)
        self.txt_amount.setValidator(validator)  # денежная сумма должна быть числом!
        self.txt_years = QLineEdit(str(self.years))
        self.txt_years.setValidator(QIntValidator(0, 10000))  # надо же как-то ограничить ))
        self.txt_months = QLineEdit(str(self.months))
        self.txt_months.setValidator(QIntValidator(0, 11))  # это ограничит двумя десятичными знаками
        self.lbl_pv = QLabel()  # расчетную сумму (present value) нельзя редактировать

    def lay_widgets(self, grid: QGridLayout, row):
        """ размещает внутренние виджеты в строку"""
        grid.addWidget(self.txt_years, row, 0)
        grid.addWidget(self.txt_months, row, 1)
        grid.addWidget(self.txt_amount, row, 3)
        grid.addWidget(self.lbl_pv, row, 5)
        # layout_h = QHBoxLayout()
        # layout_h.setContentsMargins(20, 0, 20, 0)
        # layout_h.addWidget(self.txt_years)
        # layout_h.addWidget(self.txt_months)
        # layout_h.addStretch(1)
        # layout_h.addWidget(self.txt_amount)
        # layout_h.addStretch(1)
        # layout_h.addWidget(self.lbl_pv)
        # self.setLayout(layout_h)

    def connects(self):
        """ внутри строки пересчитывается текущая стоимость, если изменено любое число"""
        self.txt_amount.editingFinished.connect(self.recalc)
        self.txt_years.editingFinished.connect(self.recalc)
        self.txt_months.editingFinished.connect(self.recalc)

    def recalc(self):
        """ пересчитывает значения свойств класса, устанавливает нужную сумму в соотв. надпись """
        base = int(self.base_widget.text())  # берём частоту начисления из поля ввода
        rate = fix_point(self.rate_widget.text())  # берём нужную ставку из поля ввода
        # да, некрасиво, нет отделения уровня данных,
        # но в этой программе уровень данных отдельно нет смысла заводить
        # сохраняем значения из полей ввода:
        self.amount = fix_point(self.txt_amount.text())
        self.years = int(self.txt_years.text())
        self.months = int(self.txt_months.text())
        # вычисляем PV:
        result = discount(self.amount, self.years, self.months, base, rate)
        # self.lbl_pv.setText(str(result)) # отрисовка
        self.lbl_pv.setText("{0:.4f}".format(result))  # отрисовка - переделано, чтобы всегда было 4 знака после запятой


class CashFlow(QWidget):
    """ класс "Поток" хранит строки, из которых складывается денежный поток,
    а также показывает общие параметры потока: процентную ставку, частоту начисления процентов, собственно NPV """

    def __init__(self, rate=0.0, base=12, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        # запоминаем параметры, с которыми создаётся экзмепляр:
        self.rate = rate
        self.base = base
        # потока пока нет, заводим соответствующие свойства:
        self.NPV = 0
        self.amounts = []
        # размещаем визуальные элементы:
        self.create_widgets()
        # подключаем сигналы и показываем:
        self.connects()
        self.show()

    def add_fa(self):
        """ добавляет одну будущую сумму"""
        months = self.months_to_add()
        years, months = months // 12, months % 12
        # добавляем с подсчитанными параметрами:
        fa = FutureAmount(self.layout_famounts, self.rows, self.txt_rate, self.spin_base, self.last_amount(), years,
                          months)
        fa.setParent(self)
        self.rows += 1
        # self.layout_famounts.addWidget(fa) # отрисовка
        # у нас нет сигнала для изменения общей суммы, обойдемся так:
        fa.txt_amount.editingFinished.connect(self.recalc)
        fa.txt_years.editingFinished.connect(self.recalc)
        fa.txt_months.editingFinished.connect(self.recalc)
        # добавляем в список:
        self.amounts.append(fa)
        # пересчитываем общую сумму:
        self.recalc()

    def months_to_add(self):
        """ пытается предсказать, сколько месяцев добавить для новой строки"""
        total = len(self.amounts)
        if 0 == total:
            return 0  # ожидаем, что на первой строке будут начальные вложения
        elif 1 == total:
            return 12  # автоматически начинаем прибавлять года
        else:
            # когда есть две последние строки, то надо понять, сколько между ними месяцев, 
            # и прибавить это к последней
            fa_2 = self.amounts[total - 2]  # вторая строка с конца
            fa_1 = self.amounts[total - 1]  # первая с конца
            months_1 = int(fa_1.txt_years.text()) * 12 + int(fa_1.txt_months.text())
            months_2 = int(fa_2.txt_years.text()) * 12 + int(fa_2.txt_months.text())
            return months_1 + (months_1 - months_2)

    def last_amount(self):
        """ возвращает сумму в последней строчек, чтобы дублировать её в ново-добавляемой """
        total = len(self.amounts)
        if total:
            fa = self.amounts[total - 1]
            return fix_point(fa.txt_amount.text())
        return 0

    def recalc(self):
        """ суммирует итог по всем строкам """
        result = 0
        for future_amount in self.amounts:
            result += float(future_amount.lbl_pv.text())
        self.lbl_npv.setText(str(round(result, 4)))

    def recalc_them_all(self):
        """ пересчитывает все промежуточные суммы и общую"""
        for future_amount in self.amounts:
            future_amount.recalc()
        self.recalc()

    def connects(self):
        """ подключает обработку действий пользователя """
        self.button_plus.clicked.connect(self.add_fa)
        self.txt_rate.editingFinished.connect(self.recalc_them_all)
        self.spin_base.valueChanged.connect(self.recalc_them_all)

    def create_widgets(self):
        """ создаёт внутренние виджеты и вызывает метод их размещения"""
        # выбор частоты пересчета:
        self.lbl_base1 = QLabel('начисление раз в')
        self.spin_base = QSpinBox()
        # self.spin_base.
        # setValidator(QIntValidator(1, 13))
        self.spin_base.setValue(self.base)
        self.spin_base.setRange(1, 12)
        self.lbl_base2 = QLabel('месяцев')
        # ввод ставки:
        self.lbl_rate1 = QLabel('ставка:')
        self.txt_rate = QLineEdit('0')
        loc = QLocale(QLocale.English, QLocale.UnitedStates)  # вводить будем с разделителем-точкой, чтобы python понял
        validator = QDoubleValidator()
        validator.setLocale(loc)
        self.txt_rate.setValidator(validator)
        self.lbl_rate2 = QLabel('процентов')
        # результат:
        self.lbl_result1 = QLabel('Итог:')
        self.lbl_npv = QLabel(str(self.NPV))
        self.lbl_npv.setStyleSheet(QSS_LabelBold)
        self.lbl_result2 = QLabel(' рублей')
        # кнопки "OK" и "+" в конце всех строк:
        self.button_ok = QPushButton('OK')
        self.button_plus = QPushButton(' + ')
        # теперь разместить
        self.lay_widgets()

    def lay_widgets(self):
        """ размещает виджеты в столбец, 
        при этом одна из ячеек этого столбца - layout, 
        в который будут добавляться виджеты типа FutureAmount """
        self.layout_main = QVBoxLayout()
        self.layout_famounts = QVBoxLayout()
        layout_h1 = QHBoxLayout()  # результат
        layout_h2 = QHBoxLayout()  # процент
        layout_h3 = QHBoxLayout()  # частота
        layout_top = QHBoxLayout()  # верхняя строка
        layout_bottom = QHBoxLayout()  # нижняя строка
        # поехали:
        layout_h1.addWidget(self.lbl_result1, alignment=Qt.AlignRight)
        layout_h1.addWidget(self.lbl_npv)
        layout_h1.addWidget(self.lbl_result2, alignment=Qt.AlignLeft)
        layout_h2.addWidget(self.lbl_rate1, alignment=Qt.AlignRight)
        layout_h2.addWidget(self.txt_rate)
        layout_h2.addWidget(self.lbl_rate2, alignment=Qt.AlignLeft)
        layout_h3.addWidget(self.lbl_base1, alignment=Qt.AlignRight)
        layout_h3.addWidget(self.spin_base)
        layout_h3.addWidget(self.lbl_base2, alignment=Qt.AlignLeft)
        # формируем из этого верхнюю строку:
        # layout_top.addLayout(layout_h1) - нет, итог лучше смотрится внизу!
        # layout_top.addStretch(2)
        layout_top.addLayout(layout_h2)
        layout_top.addStretch(2)
        layout_top.addLayout(layout_h3)
        self.layout_main.addLayout(layout_top)  # добавили
        # и нижняя строка:
        layout_bottom.addWidget(self.button_ok)
        layout_bottom.addStretch(2)
        layout_bottom.addLayout(layout_h1)
        layout_bottom.addStretch(2)
        layout_bottom.addWidget(self.button_plus, alignment=Qt.AlignRight)
        self.layout_main.addLayout(layout_bottom)  # добавили

        # теперь первую строку таблицы, в ней будут названия столбцов:
        self.layout_famounts = QGridLayout()
        self.rows = 0  # запоминаем, сколько строк уже добавлено
        lbc1 = QLabel('лет')
        lbc1.setStyleSheet(QSS_Columns)
        self.layout_famounts.addWidget(lbc1, self.rows, 0, alignment=Qt.AlignHCenter)
        lbc2 = QLabel('месяцев')
        lbc2.setStyleSheet(QSS_Columns)
        self.layout_famounts.addWidget(lbc2, self.rows, 1, alignment=Qt.AlignHCenter)
        self.layout_famounts.addWidget(QLabel('  '), self.rows, 2)
        lbc3 = QLabel('сумма')
        lbc3.setStyleSheet(QSS_Columns)
        self.layout_famounts.addWidget(lbc3, self.rows, 3, alignment=Qt.AlignHCenter)
        self.layout_famounts.addWidget(QLabel('  '), self.rows, 4)
        lbc4 = QLabel('итог:')
        lbc4.setStyleSheet(QSS_Columns)
        self.layout_famounts.addWidget(lbc4, self.rows, 5, alignment=Qt.AlignRight)

        # в layout_famounts будут добавляться строки нажатием на '+'
        area = QScrollArea()
        widget_scroll = QWidget()
        widget_scroll.setLayout(self.layout_famounts)
        area.setWidget(widget_scroll)
        area.setWidgetResizable(True)
        self.layout_main.addWidget(area)  # добавили
        self.rows += 1

        self.setLayout(self.layout_main)


app = QApplication([])
main = CashFlow()
main.resize(750, 200)
main.setWindowTitle('Финансовый калькулятор')
app.exec()
