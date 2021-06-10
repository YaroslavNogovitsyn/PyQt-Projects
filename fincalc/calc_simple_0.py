""" Простая версия калькулятора NPV
сначала сделаем основу класса FutureAmount, который будет показывать один элемент денежного потока 

-   методы create_widgets и lay_widgets  создают и располагают в строку
    поля ввода (txt_years, txt_amount) и надпись lbl_pv
-   метод recalc обеспечивает, что текст lbl_pv будет показывать дисконтированную сумму
-   обновление вызывается по сигналам editingFinished от полей ввода 
    (т.е. как только поле ввода потеряло фокус, мы берем оттуда информацию),
    см. метод connects
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


# Проверка, что пока все работает:
app = QApplication([])

a = FutureAmount(10, 1)
b = FutureAmount(15, 2)

main_w = QWidget()
lt_main = QVBoxLayout()
lt_main.addWidget(a)
lt_main.addWidget(b)
main_w.setLayout(lt_main)
main_w.show()
app.exec()
