""" Окно "карточка вопроса":
добавим функцию, которая показывает панель проверки ответа
эта панель при добавлении в макет должна быть скрыта
(строка 77 - меняем, какая панель скрывается в начале)
функция show_result() её показывает и скрывает панель вопросов, 
а также меняет надпись на кнопке:
строки 97 - 10
нажатие кнопки btn_OK вызывает функцию show_result()
(строка 107)
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QGroupBox, QRadioButton,
    QPushButton, QLabel)

app = QApplication([])

# виджеты, которые надо будет разместить:
btn_OK = QPushButton('Ответить')  # кнопка ответа
lb_Question = QLabel('Самый сложный вопрос в мире!')  # текст вопроса

# ----------------------------------------------------------
# Создаем панель с вариантами ответов:
# ----------------------------------------------------------

# Создаем виджеты и объединяем их в группы
RadioGroupBox = QGroupBox("Варианты ответов")  # группа на экране для переключателей с ответами

rbtn_1 = QRadioButton('Вариант 1')
rbtn_2 = QRadioButton('Вариант 2')
rbtn_3 = QRadioButton('Вариант 3')
rbtn_4 = QRadioButton('Вариант 4')

# Размещаем на панели варианты ответов в два столбца внутри группы:
layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()  # вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1, alignment=Qt.AlignCenter)  # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2, alignment=Qt.AlignCenter)
layout_ans3.addWidget(rbtn_3, alignment=Qt.AlignCenter)  # два ответа во второй столбец
layout_ans3.addWidget(rbtn_4, alignment=Qt.AlignCenter)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)  # разместили столбцы в одной строке

RadioGroupBox.setLayout(layout_ans1)  # готова "панель" с вариантами ответов

# ----------------------------------------------------------
# Создаем панель с результатом теста (проверка ответа):
# ----------------------------------------------------------

# Создаем виджеты и объединяем их в группы
AnsGroupBox = QGroupBox("Результат теста")
lb_Result = QLabel('прав ты или нет?')  # здесь размещается надпись "правильно" или "неправильно"
lb_Correct = QLabel('ответ будет тут!')  # здесь будет написан текст правильного ответа

# Размещаем результат теста:
layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)

# ----------------------------------------------------------
# Размещаем все виджеты в окне:
# ----------------------------------------------------------

layout_line1 = QHBoxLayout()  # вопрос
layout_line2 = QHBoxLayout()  # варианты ответов или результат теста
layout_line3 = QHBoxLayout()  # кнопка "Ответить"

layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
# Размещаем в одной строке обе панели, одна из них будет скрываться, другая показываться:
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide()  # скроем панель с ответом, сначала должна быть видна панель вопросов

layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2)  # кнопка должна быть большой
layout_line3.addStretch(1)

# Теперь созданные строки разместим друг под другой:
layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5)  # пробелы между содержимым


# ----------------------------------------------------------
# Виджеты и макеты созданы, далее - функции:
# ----------------------------------------------------------

def show_result():
    """ показать панель ответов """
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Следующий вопрос')


window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memo Card')

btn_OK.clicked.connect(show_result)  # проверяем, что панель ответов показывается при нажатии на кнопку

window.show()

app.exec()
