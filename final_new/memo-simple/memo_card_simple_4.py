""" Окно "карточка вопроса":

Добавляется возможность задать вопрос и проверить, верен ли ответ.
Функция ask() получает вопрос, правильный ответ, три неверных ответа.
Она размещает варианты ответов в тексты радиокнопок.
Для того, чтобы правильный ответ не оказывался все время на одном месте, делаем так:
подключаем функцию shuffle для перемешивания списка в случайном порядке (строка 25)
создаем список answers из кнопок, в которых будут варианты ответов (строка 131)
этот список перемешивается и на кнопки размещаются нужные надписи в функции ask (строки 136 - 143)

функция check_answer() (строки 150 - 158) проверяет, какой ответ выбран и в соответствии с этим
запускает функцию show_correct() с параметром "верно" или "неверно", 
- этот текст показывается на экране на панели ответа (вместе с правильным ответом)

для проверки перед window.show() запускаем функцию ask с каким-нибудь наборов вопросов 
и подключаем сигнал clicked кнопки к функции check_answer
(строки 168 - 169)
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QGroupBox, QButtonGroup, QRadioButton,
    QPushButton, QLabel)
from random import shuffle

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

RadioGroup = QButtonGroup()  # это для группировки переключателей, чтобы управлять их поведением
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)

# Размещаем на панели варианты ответов в два столбца внутри группы:
layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()  # вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1)  # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3)  # два ответа во второй столбец
layout_ans3.addWidget(rbtn_4)

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


def show_question():
    """ показать панель вопросов """
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')
    # сбросить выбранную радио-кнопку
    RadioGroup.setExclusive(False)  # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True)  # вернули ограничения, теперь только одна радиокнопка может быть выбрана


answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]


def ask(question, right_answer, wrong1, wrong2, wrong3):
    """ функция записывает значения вопроса и ответов в соответствующие виджеты, 
    при этом варианты ответов распределяются случайным образом"""
    shuffle(answers)  # перемешали список из кнопок, теперь на первом месте списка какая-то непредсказуемая кнопка
    answers[0].setText(right_answer)  # первый элемент списка заполним правильным ответом, остальные - неверными
    answers[1].setText(wrong1)
    answers[2].setText(wrong2)
    answers[3].setText(wrong3)
    lb_Question.setText(question)  # вопрос
    lb_Correct.setText(right_answer)  # ответ
    show_question()  # показываем панель вопросов


def show_correct(res):
    """ показать результат - установим переданный текст в надпись "результат" и покажем нужную панель """
    lb_Result.setText(res)
    show_result()


def check_answer():
    """ если выбран какой-то вариант ответа, то надо проверить и показать панель ответов"""
    if answers[0].isChecked():
        # правильный ответ!
        show_correct('Правильно!')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            # неправильный ответ!
            show_correct('Неверно!')


# ----------------------------------------------------------
# Все готово, создаем окно и запускаем, задав один вопрос:
# ----------------------------------------------------------

window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memo Card')
# задаем вопрос:
ask('Выбери перевод слова "переменная"', 'variable', 'variation', 'variant', 'changing')
btn_OK.clicked.connect(check_answer)  # убрали тест, здесь нужна проверка ответа

window.show()

app.exec()
