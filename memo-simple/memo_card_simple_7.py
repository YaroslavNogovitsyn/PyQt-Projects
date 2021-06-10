""" Программа "карточка вопроса":
рабочая версия со случайным выбором вопроса из списка
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QGroupBox, QButtonGroup, QRadioButton,
    QPushButton, QLabel)
from random import randint, shuffle  # функция randint нужна для выбора случайного вопроса,


# а shuffle - для случайного перемешивания ответов

# ----------------------------------------------------------
# Подготовка данных для программы:
# ----------------------------------------------------------

class Question:
    """ содержит вопрос, правильный ответ и три неправильных"""

    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        # все строки надо задать при создании объекта, они запоминаются в свойства
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


questions_list = []  # с этим списком вопросов работает наша программа
# забьем в этот список несколько слов для русско-польского словарика:
questions_list.append(Question('холм', 'pagorek', 'bugor', 'kopcow', 'helm'))
questions_list.append(Question('деревня', 'wioska', 'woiska', 'woinstva', 'wilena'))
questions_list.append(Question('город', 'miasto', 'miejsce', 'grad', 'gurat'))
questions_list.append(Question('ель', 'swierk', 'sosna', 'cholka', 'picea'))

# ----------------------------------------------------------
# Создание интерфейса:
# ----------------------------------------------------------

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


def ask(q: Question):
    """ функция записывает значения вопроса и ответов в соответствующие виджеты, 
    при этом варианты ответов распределяются случайным образом"""
    shuffle(answers)  # перемешали список из кнопок, теперь на первом месте списка какая-то непредсказуемая кнопка
    answers[0].setText(q.right_answer)  # первый элемент списка заполним правильным ответом, остальные - неверными
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question)  # вопрос
    lb_Correct.setText(q.right_answer)  # ответ
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


def next_question():
    """ задает случайный вопрос из списка """
    cur_question = randint(0, len(questions_list) - 1)  # нам не нужно старое значение, 
    # поэтому можно использовать локальную переменную!
    # случайно взяли вопрос в пределах списка
    # если внести около сотни слов, то редко будет повторяться
    q = questions_list[cur_question]  # взяли вопрос
    ask(q)  # спросили


def click_OK():
    """ определяет, надо ли показывать другой вопрос либо проверить ответ на этот """
    if btn_OK.text() == 'Ответить':
        check_answer()  # проверка ответа
    else:
        next_question()  # следующий вопрос


# ----------------------------------------------------------
# Все готово, создаем окно и запускаем, задав первый вопрос. 
# Можно переходить к следующему:
# ----------------------------------------------------------

window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memo Card')

btn_OK.clicked.connect(click_OK)  # по нажатии на кнопку выбираем, что конкретно происходит

# все настроено, осталось задать вопрос и показать окно:
next_question()
window.resize(400, 300)
window.show()
app.exec()
