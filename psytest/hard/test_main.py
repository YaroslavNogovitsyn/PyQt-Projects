from functools import partial  # используем элементы функционального программирования, 
# чтобы сгенерировать несколько функций на базе одной - 
# это позволит сделать обработку нажатия на кнопки, 
# когда заранее не задано количество этих кнопок 

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QGroupBox, QRadioButton,
    QPushButton, QLabel, QListWidget)

from test_dataclasses import list_from_choices, list_from_types

txt_alt = 'Выбор '
txt_next = 'Вперёд'
txt_prev = 'Назад'
txt_finish = 'Завершить'
txt_title = 'Дифференциально-диагностический опросник Климова'
txt_result = 'Баллов'
txt_descr = 'Описание'
txt_more = 'Подробнее'

win_width, win_height = 800, 300
win_x, win_y = 200, 200


class AlternativeGroup:
    """ отображает два варианта"""

    def __init__(self, a1, a2, number, parent=None):
        """ передаётся две альтернативы и номер вопроса """
        self.a1 = QRadioButton(a1)
        self.a2 = QRadioButton(a2)
        self.number = number
        self.initUI()

    def initUI(self):
        """ создает графические элементы """
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.a1, alignment=Qt.AlignHCenter)
        layoutH.addWidget(self.a2, alignment=Qt.AlignHCenter)
        text = txt_alt + str(self.number + 1)
        self.group = QGroupBox(text)
        self.group.setLayout(layoutH)

    def show(self):
        self.group.show()

    def hide(self):
        self.group.hide()

    def is_checked(self):
        """отвечает, выбран ли какой-то ответ"""
        return self.a1.isChecked() or self.a2.isChecked()

    def value(self):
        """ значением группы будет считаться кортеж из номера группы, номера ответа (1 или 2), текста выбранного
        ответа """
        val = 0
        answer = ''
        if self.a1.isChecked():
            val, answer = 1, self.a1.text()
        elif self.a2.isChecked():
            val, answer = 2, self.a2.text()
        return (self.number, val, answer)


class AllQuestions(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        """ виджет, в котором много панелей, на каждой - два варианта ответов """
        super().__init__(parent=parent, flags=flags)
        self.list_choices = []  # список панелей-экземпляров класса AlternativeGroup
        self.layoutV = QVBoxLayout()
        self.current_choice = -1  # текущий вопрос

    def add_choice(self, a1, a2):
        number = len(self.list_choices)
        choice = AlternativeGroup(a1, a2, number, self)
        self.list_choices.append(choice)
        self.layoutV.addWidget(choice.group)
        choice.hide()

    def show_curr(self):
        self.list_choices[self.current_choice].show()

    def hide_curr(self):
        self.list_choices[self.current_choice].hide()

    def start(self):
        self.current_choice = 0
        self.show_curr()
        self.setLayout(self.layoutV)
        self.show()

    def is_checked(self):
        return self.list_choices[self.current_choice].is_checked()

    def is_last(self):
        return self.current_choice >= len(self.list_choices) - 1

    def is_first(self):
        return self.current_choice <= 0

    def next(self):
        if self.is_checked() and not self.is_last():
            self.hide_curr()
            self.current_choice += 1
            self.show_curr()

    def prev(self):
        if not self.is_first():
            self.hide_curr()
            self.current_choice -= 1
            self.show_curr()

    def calculate_values(self):
        """ составляет список всех выбранных значений """
        values = []
        for choice in self.list_choices:
            values.append(choice.value())
        return values


class MainWindow(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        """ окно, в котором проводится опрос """
        super().__init__(parent=parent, flags=flags)
        # загружаем данные: 
        self.list_choices = list_from_choices()
        self.list_types = list_from_types()
        # создаём и настраиваем графические эелементы:
        self.initUI()
        self.connects()
        self.set_appear()
        # переносим данные в виджеты:
        self.load_questions()
        self.questionnary.start()
        # старт:
        self.show()

    def initUI(self):
        """ создает графические элементы """
        self.questionnary = AllQuestions()
        self.btn_next = QPushButton(txt_next, self)
        self.btn_prev = QPushButton(txt_prev, self)

        layout_line = QHBoxLayout()
        layout_line.addStretch(1)
        layout_line.addWidget(self.btn_prev)
        layout_line.addStretch(1)
        layout_line.addWidget(self.btn_next)
        layout_line.addStretch(1)

        layout_column = QVBoxLayout()
        layout_column.addWidget(self.questionnary)
        layout_column.addLayout(layout_line)
        self.setLayout(layout_column)

    def addchoice(self, a1, a2):
        self.questionnary.add_choice(a1, a2)

    def load_questions(self):
        """ загружает вопросы из списка объектов в интерфейс """
        for question in self.list_choices:
            self.addchoice(question.a1, question.a2)

    def next_click(self):
        if self.questionnary.is_last():
            self.finish(self.questionnary.calculate_values())
        else:
            self.questionnary.next()
            if self.questionnary.is_last():
                self.btn_next.setText(txt_finish)  # меняем текст кнопки, если дальше нет вопросов, на "Завершить"

    def prev_click(self):
        # возможно, текст кнопки был "Завершить", в любом случае при шаге назад нужен текст "Продолжить"
        self.btn_next.setText(txt_next)
        self.questionnary.prev()

    def connects(self):
        self.btn_next.clicked.connect(self.next_click)
        self.btn_prev.clicked.connect(self.prev_click)

    def set_appear(self):
        """ устанавливает, как будет выглядеть окно (надпись, размер, место) """
        self.setWindowTitle(txt_title)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

    def finish(self, list_answers):
        """ завершение теста, переход к результатам"""
        list_result = []  # список из кортежей, в которых будут записаны: 
        # количество ответов для каждого типа профессии,
        # номер типа 
        # и соответствующий типу профессии текст 
        for i, profession_type in enumerate(self.list_types):
            result = profession_type.check(list_answers)
            list_result.append((result, i, profession_type.description))
        list_result.sort(reverse=True)  # сортируем по убыванию
        self.rt = ResultTable(list_result, self.list_types)  # создаем и показываем окно результатов, передавая ему
        # сгенерированные данные
        self.hide()
        self.rt.show()


class ResultTable(QWidget):
    def __init__(self, list_result, list_types, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.list_result = list_result
        self.list_types = list_types
        self.show_results()
        self.add_answerslist()
        self.connects()

    def show_results(self):
        self.setWindowTitle(" Результаты ")
        self.layoutG = QGridLayout()
        self.generate_buttons()  # список кнопок
        self.add_titlerow()
        self.add_rows()

    def add_answerslist(self):
        self.lw_answers = QListWidget(self)
        layoutV = QVBoxLayout()
        layoutV.addLayout(self.layoutG)
        layoutV.addWidget(self.lw_answers)
        self.lw_answers.hide()
        self.setLayout(layoutV)

    def generate_buttons(self):
        """ создает список кнопок - по одной для каждого типа профессий. Нажатие на кнопки позволит посмотреть
        детали. """
        self.buttons = []
        for i in self.list_result:
            self.buttons.append(QPushButton(txt_more))

    def add_titlerow(self):
        self.layoutG.addWidget(QLabel(txt_result), 0, 0)
        self.layoutG.addWidget(QLabel(txt_descr), 0, 1)

    def add_row(self, row, result, i, description):
        self.layoutG.addWidget(QLabel(str(result)), row, 0)
        self.layoutG.addWidget(QLabel(description), row, 1)
        self.layoutG.addWidget(self.buttons[i], row, 2)

    def add_rows(self):
        for row, res in enumerate(self.list_result):
            result, i, description = res[0], res[1], res[2]
            self.add_row(row + 1, result, i, description)

    def clicked(self, i):
        """ "Шаблон" для функций, которые обрабатывают клик на каждую кнопку"""
        self.current_index = i
        self.show_answers()

    def connects(self):
        for i, btn in enumerate(self.buttons):
            self.buttons[i].clicked.connect(partial(self.clicked, i))
            # partial(self.clicked, i) - это функция, которая получается из self.clicked, если передать в неё
            # параметр i
            # Можно просто создать отдельно нужные нам 5 функций обработки, и привязать каждую к кнопке на
            # соответствующей строке но тогда эта программа не сможет работать с другими тестами, где профилей - не
            # 5, а другое количество

    def show_answers(self):
        """ показывает в списке внизу ответы, которые соответствуют выбранному профилю 
        (нажатием нужной кнопки "подробнее") """
        l_a = self.list_types[self.current_index].answers
        self.lw_answers.hide()
        show_list(self.lw_answers, l_a)  # заполняем
        self.lw_answers.show()


def show_list(lw: QListWidget, list_data):
    """ заполняет список lw строками, которые содержатся в списке list_data"""
    lw.clear()
    for data_str in list_data:
        lw.addItem(data_str)


def main():
    app = QApplication([])
    mw = MainWindow()
    app.exec_()


main()
