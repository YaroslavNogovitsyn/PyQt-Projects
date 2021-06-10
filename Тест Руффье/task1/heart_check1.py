""" Программа помогает провести тест Руфье для оценки работы сердца ребенка/подростка. Это первая версия кода. """
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIntValidator, QFont, QPalette, \
    QColor  # QIntValidator проверяет, что пользователем вводятся целые числа
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QLineEdit)

# размеры окон:
win_width1, win_height1 = 1000, 500
win_width2, win_height2 = 1000, 600
win_width3, win_height3 = 500, 200
win_x, win_y = 200, 200

# константы с текстами:
txt_hello = 'Добро пожаловать в программу по определению состояния здоровья!'
txt_next = 'Начать'
txt_instruction = (
    '\nДанное приложение позволит вам с помощью теста Руфье провести первичную диагностику вашего здоровья.\n\n'
    'Проба Руфье представляет собой нагрузочный комплекс, предназначенный для оценки работоспособности\n'
    'сердца при физической нагрузке. У испытуемого, находящегося в положении лежа на спине в течение 5 мин,\n'
    'определяют частоту пульса за 15 секунд; затем в течение 45 секунд испытуемый выполняет 30 приседаний.\n'
    'После окончания нагрузки испытуемый ложится, и у него вновь подсчитывается число пульсаций за первые\n'
    '15 секунд, а потом — за последние 15 секунд первой минуты периода восстановления.\n'
    'Важно! Если в процессе проведения испытания вы почувствуете себя плохо (появится головокружение, шум в\n'
    'ушах, сильная одышка и др.), то тест необходимо прервать и обратиться к врачу.')
txt_title = 'Здоровье'
txt_name = 'Введите Ф.И.О.:'
txt_hintname = "Ф.И.О."
txt_hintage = "0"
txt_test1 = 'Лягте на спину, отдохните, потом 15 секунд измеряйте пульс. \nНажмите кнопку "Начать первый тест", чтобы запустить таймер.\nРезультат запишите в соответствующее поле.'
txt_test2 = 'Выполните 30 приседаний за 45 секунд. \nНажмите кнопку "Начать делать приседания",\nчтобы запустить счетчик приседаний.'
txt_test3 = ('Лягте на спину и замерьте пульс сначала \nза первые 15 секунд минуты, затем за последние 15 секунд.\n'
             'Нажмите кнопку "Начать финальный тест", чтобы запустить таймер.\nЗеленым обозначены секунды, в течение которых необходимо'
             '\nпроводить измерения, красным - секунды без замера пульсаций. \nРезультаты запишите в соответствующие поля.')
txt_sendresults = 'Отправить результаты'
txt_hinttest1 = '0'
txt_hinttest2 = '0'
txt_hinttest3 = '0'
txt_starttest1 = 'Начать первый тест'
txt_starttest2 = 'Начать делать приседания'
txt_starttest3 = 'Начать финальный тест'
txt_timer = 'отдых'
txt_age = 'Полных лет:'
txt_finalwin = 'Результаты'
txt_index = 'Индекс Руфье: '
txt_workheart = 'Работоспособность сердца: '
txt_res1 = "низкая. Срочно обратитесь к врачу!"
txt_res2 = "удовлетворительная. Обратитесь к врачу!"
txt_res3 = "средняя. Возможно, стоит дополнительно обследоваться у врача."
txt_res4 = "выше среднего"
txt_res5 = "высокая"


class Person:
    """ информация о человеке: имя и возраст """

    def __init__(self, name, age):
        self.name = name
        self.age = age


class Experiment:
    """ запись об одном проведении всего теста: три измерения связываются с одним человеком """

    # можно использовать и набор переменных, но так проще передавать информацию:
    # экземпляр класса FinalWindow - окно с результатом - 
    # при создании получает один параметр класса Experiment, а не 5 переменных 
    def __init__(self, person, test1, test2, test3):
        self.person = person
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3


class FinalWindow(QWidget):
    """ окно с результатами  """

    def __init__(self, exp, parent=None, flags=Qt.WindowFlags()):
        """ для создания окна необходимо передать конструктору запись с результатами теста """
        super().__init__(parent=parent, flags=flags)  # сначала создается пустой виджет
        # берем данные об "эксперименте"
        self.exp = exp
        # рассчитываем индекс:
        self.index = self.index_r()
        # интерпретируем индекс методом self.results() (для неправильного возраста индекс обнулится):
        self.text1 = txt_workheart + self.results()  # готов основной текст с результатом
        self.text2 = txt_index + str(self.index)  # текст для надписи с численным значением индекса
        # размещаем надписи:
        self.initUI()
        # устанавливает, как будет выглядеть окно (надпись, размер, место)
        self.set_appear()
        # старт:
        self.show()

    def index_r(self):
        """ возвращает индекс Руфье, используя данные из свойства self.exp - объекта класса Experiment"""
        return (4 * (int(self.exp.test1) + int(self.exp.test2) + int(self.exp.test3)) - 200) / 10

    def results(self):
        """ возвращает строку с интерпретацией индекса в зависимости от возраста """
        if self.exp.person.age < 7:
            self.index = 0
            return "нет данных для такого возраста"

        # дальше просто записана таблица для каждого возраста.
        # этот способ не очень изящен, но ученики скорее всего будут примерно так писать свой расчет:
        if self.exp.person.age == 7 or self.exp.person.age == 8:
            if self.index >= 21:
                return txt_res1
            elif self.index < 21 and self.index >= 17:
                return txt_res2
            elif self.index < 17 and self.index >= 12:
                return txt_res3
            elif self.index < 12 and self.index >= 6.5:
                return txt_res4
            else:
                return txt_res5
        if self.exp.person.age == 9 or self.exp.person.age == 10:
            if self.index >= 19.5:
                return txt_res1
            elif self.index < 19.5 and self.index >= 15.5:
                return txt_res2
            elif self.index < 15.5 and self.index >= 10.5:
                return txt_res3
            elif self.index < 10.5 and self.index >= 5:
                return txt_res4
            else:
                return txt_res5
        if self.exp.person.age == 11 or self.exp.person.age == 12:
            if self.index >= 18:
                return txt_res1
            elif self.index < 18 and self.index >= 14:
                return txt_res2
            elif self.index < 14 and self.index >= 9:
                return txt_res3
            elif self.index < 9 and self.index >= 3.5:
                return txt_res4
            else:
                return txt_res5
        if self.exp.person.age == 13 or self.exp.person.age == 14:
            if self.index >= 16.5:
                return txt_res1
            elif self.index < 16.5 and self.index >= 12.5:
                return txt_res2
            elif self.index < 12.5 and self.index >= 7.5:
                return txt_res3
            elif self.index < 7.5 and self.index >= 2:
                return txt_res4
            else:
                return txt_res5
        if self.exp.person.age >= 15:
            if self.index >= 15:
                return txt_res1
            elif self.index < 15 and self.index >= 11:
                return txt_res2
            elif self.index < 11 and self.index >= 6:
                return txt_res3
            elif self.index < 6 and self.index >= 0.5:
                return txt_res4
            else:
                return txt_res5

    def initUI(self):
        """ создает графические элементы """
        self.workh_text = QLabel(self.text1)  # основной текст с интерпретацией результата
        self.index_text = QLabel(self.text2)  # текст со значением индекса

        self.layout_line = QVBoxLayout()  # размещаем все в столбик
        self.layout_line.addWidget(self.index_text, alignment=Qt.AlignCenter)
        self.layout_line.addWidget(self.workh_text, alignment=Qt.AlignCenter)
        self.setLayout(self.layout_line)

    def set_appear(self):
        """ устанавливает, как будет выглядеть окно (надпись, размер, место) """
        self.setWindowTitle(txt_finalwin)
        self.resize(win_width3, win_height3)
        self.move(win_x, win_y)


class TestWindow(QWidget):
    """ 
    Окно, в котором проводится тестирование.
    Счетчики секунд/приседаний помогают провести измерения.
    В соотетствующих полях записываются результаты измерения. 
    """

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        """ Конструктор окна для теста, можно создавать без параметров """
        super().__init__(parent=parent, flags=flags)

        self.timer = QTimer()  # создаем один таймер, сигнал от которого будет менять часы
        # в каждом нужном случае

        self.time = 15  # свойство "счетчик" - сколько осталось времени или приседаний

        # создаём и настраиваем графические эелементы:
        self.initUI()
        # устанавливает связи между элементами
        self.connects()
        # устанавливает, как будет выглядеть окно (надпись, размер, место)
        self.set_appear()
        # старт:
        self.show()

    def initUI(self):
        """ создает графические элементы """
        # кнопки:
        self.btn_next = QPushButton(txt_sendresults, self)
        self.btn_test1 = QPushButton(txt_starttest1, self)
        self.btn_test2 = QPushButton(txt_starttest2, self)
        self.btn_test3 = QPushButton(txt_starttest3, self)
        # подсказки:
        self.text_name = QLabel(txt_name)
        self.text_age = QLabel(txt_age)
        self.text_test1 = QLabel(txt_test1)
        self.text_test2 = QLabel(txt_test2)
        self.text_test3 = QLabel(txt_test3)
        # счетчик на экране (текст, который мы будем менять):
        self.text_timer = QLabel(txt_timer)
        self.text_timer.setFont(QFont("Times", 36, QFont.Bold))  # большой такой текст!
        # поля ввода данных о человеке :
        self.line_name = QLineEdit(txt_hintname)  #
        self.line_age = QLineEdit(txt_hintage)  # возраст
        self.line_age.setValidator(QIntValidator(7, 150))  # возраст должен быть числом!
        # валидатор проверяет, что вводится целое число с нужным количеством цифр
        # хочется, чтобы пользователь не мог ввести возраст меньше 7,
        # но в действительности тут написано "минимум одна цифра, максимум три"
        # поля ввода результатов
        self.line_test1 = QLineEdit(txt_hinttest1)
        self.line_test1.setValidator(QIntValidator(0, 150))

        self.line_test2 = QLineEdit(txt_hinttest2)
        self.line_test2.setValidator(QIntValidator(0, 150))

        self.line_test3 = QLineEdit(txt_hinttest3)
        self.line_test3.setValidator(QIntValidator(0, 150))

        # теперь расставляем все в макетах 
        self.layout_hline = QHBoxLayout()  # основной макет: строка из двух столбцов
        self.layout_lineleft = QVBoxLayout()  # слева тут будет друг под другом много чего
        self.layout_lineright = QVBoxLayout()  # а справа гордый счетчик
        self.layout_lineright.addWidget(self.text_timer, alignment=Qt.AlignCenter)
        # правый есть, теперь все виджеты в левый столбец:
        self.layout_lineleft.addWidget(self.text_name, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.line_name, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.text_age, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.line_age, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.text_test1, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.btn_test1, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.line_test1, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.text_test2, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.btn_test2, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.text_test3, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.btn_test3, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.line_test2, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.line_test3, alignment=Qt.AlignLeft)
        self.layout_lineleft.addWidget(self.btn_next, alignment=Qt.AlignRight)
        # собираем два столбца в строку:
        self.layout_hline.addLayout(self.layout_lineleft)
        self.layout_hline.addLayout(self.layout_lineright)
        # макет layout_hline применяется к окну:
        self.setLayout(self.layout_hline)

    def set_appear(self):
        """ устанавливает, как будет выглядеть окно (надпись, размер, место) """
        self.setWindowTitle(txt_title)
        self.resize(win_width2, win_height2)
        self.move(win_x, win_y)

    def connects(self):
        self.btn_next.clicked.connect(self.show_result)
        self.btn_test1.clicked.connect(self.start_test1)
        self.btn_test2.clicked.connect(self.start_sits_stands)
        self.btn_test3.clicked.connect(self.start_finaltest)

    def show_result(self):
        """ заканчивает тест, показывает окно с рассчитанным результатом"""
        # запомнили данные о человеке, взяли text у всех нужных полей ввода :
        prs = Person(self.line_name.text(), int(self.line_age.text()))
        # запомнили данные о проведенном тесте:
        exp = Experiment(prs, self.line_test1.text(), self.line_test2.text(), self.line_test2.text())
        self.hide()  # ушли в закат
        self.fw = FinalWindow(exp)  # можно и так добиться, чтобы fw не было локальной переменной, 
        # которая уничтожается после конца работы метода

    def reset_timer(self):
        """ обнуляет таймер, убирая все имеющиеся связи с ним """
        self.timer.stop()  # стоп
        try:
            self.timer.timeout.disconnect()  # выдаст ошибку, если никаких коннектов нет
        except:
            pass  # а нам и не надо, чтоб коннекты были

    def start_test1(self):
        """ отмеряет 15 секунд для первого измерения пульса """
        self.reset_timer()
        self.time = 15
        self.text_timer.setText("00:00:15")
        self.timer.timeout.connect(self.next_test1)
        self.text_timer.setStyleSheet("color: black")  # для цветов, которые трудно записать строкой, можно
        # использовать RGB-код, например,
        # self.text_timer.setStyleSheet("color: rgb(0,255,0)")
        # устанавливает зелёный цвет
        # rgb(255,0,255) - фиолетовый и т.д.
        self.timer.start(1000)

    def start_sits_stands(self):
        """ отмеряет 30 приседаний и отводит 1,5 секунды на каждое """
        self.reset_timer()
        self.time = 30
        self.text_timer.setText(str(self.time))
        self.text_timer.setStyleSheet("color: rgb(255,0,255)")
        self.timer.timeout.connect(self.next_sit)
        # одно приседание в 1.5 секунды
        self.timer.start(1500)

    def start_finaltest(self):
        """ отмеряет минуту для второго и третьего измерения пульса """
        self.reset_timer()
        self.time = 60
        self.text_timer.setText("00:01:00")
        self.text_timer.setStyleSheet("color: green")
        self.timer.timeout.connect(self.next_finaltest)
        self.timer.start(1000)

    def next_test1(self):
        """ сработал таймер в первом тесте, меняем надпись (в виде часов) """
        self.time = self.time - 1
        seconds = str(self.time)
        if self.time < 10:
            seconds = "0" + seconds
        self.text_timer.setText("00:00:" + seconds)
        if self.time == 0:
            self.timer.stop()

    def next_sit(self):
        """ сработал таймер для приседания, меняем надпись (в виде числа) """
        self.time -= 1
        self.text_timer.setText(str(self.time))
        if self.time == 0:
            self.timer.stop()

    def next_finaltest(self):
        """ сработал таймер в последнем тесте, меняем надпись (в виде часов), 
        и меняем цвет, чтобы показывать, когда измерять пульс """
        self.time -= 1
        seconds = str(self.time)
        if self.time < 10:
            seconds = "0" + seconds
        self.text_timer.setText("00:00:" + seconds)
        if self.time >= 45 or self.time <= 15:
            self.text_timer.setStyleSheet("color: green")
        else:
            self.text_timer.setStyleSheet("color: red")
        if self.time == 0:
            self.timer.stop()


class MainWindow(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        """ окно, в котором располагается приветствие """
        super().__init__(parent=parent, flags=flags)
        # создаём и настраиваем графические эелементы:
        self.initUI()
        # устанавливает связи между элементами
        self.connects()
        # устанавливает, как будет выглядеть окно (надпись, размер, место)
        self.set_appear()
        # старт:
        self.show()

    def initUI(self):
        """ создает графические элементы """
        self.btn_next = QPushButton(txt_next, self)
        self.hello_text = QLabel(txt_hello)
        self.instruction = QLabel(txt_instruction)
        # размещение приветствия, инструкции и кнопки "далее" в один столбец:
        layout_line = QVBoxLayout()
        layout_line.addWidget(self.hello_text, alignment=Qt.AlignHCenter)
        layout_line.addWidget(self.instruction, alignment=Qt.AlignHCenter)
        layout_line.addWidget(self.btn_next, alignment=Qt.AlignCenter)
        self.setLayout(layout_line)

    def set_appear(self):
        """ устанавливает, как будет выглядеть окно (надпись, размер, место) """
        self.setWindowTitle(txt_title)
        self.resize(win_width1, win_height1)
        self.move(win_x, win_y)

    def connects(self):
        self.btn_next.clicked.connect(self.next_click)

    def next_click(self):
        global tw
        tw = TestWindow()
        self.hide()


def main():
    app = QApplication([])  # это первым делом, до создания виджетов
    app.setFont(QFont("Times New Roman", 12),
                className='MainWindow')  # setFont и setPalette можно применять ко всему application,
    # при этом можно выбрать классы, экземпляры которых будут показаны так
    app.setFont(QFont("Times New Roman", 10), className='TestWindow')
    pal = QPalette()  # создать палитру
    pal.setColor(QPalette.Window, QColor("white"))  # флаг QPalette.Window означает цвет фона
    app.setPalette(pal)
    # первое окно:
    mw = MainWindow()
    app.exec_()


main()
