""" Программа помогает провести тест Руфье для оценки работы сердца ребенка/подростка,
поэтапно проводя соответствующие замеры. Это вторая версия, с более сложным интерфейсом """
import ruffier  # в этом модуле реализовано вычисление индекса Руфье и оценка результата в зависимости от возраста
from PyQt5.QtCore import Qt  # Набор констант для разных флагов (в основном размещение виджетов)
from PyQt5.QtGui import QIntValidator  # Проверка, что в виджете находится целое число
from PyQt5.QtWidgets import *

# константы, управляющие размерами и положением окон:
win_width, win_height = 800, 500
win_test_width, win_test_height = 800, 500
win_x, win_y = 200, 200

# элементы таблиц стилей:
Style_green = "color: green; "
Style_red = "color: red; "
Style_large = "font-size: 36px; "
Style_middle = "font-size: 16px; "
Style_bold = 'font: bold "Times New Roman";'
Style_regular = 'font: "Times New Roman";'

# все текстовые сообщения:
txt_hello = 'Добро пожаловать в программу по определению состояния здоровья!'
txt_next = 'Начать'
txt_back = 'Вернуться'
txt_finish = 'Закончить тест'
txt_instruction = """
            Данное приложение позволит вам с помощью теста Руфье провести первичную диагностику вашего здоровья.
            Проба Руфье представляет собой нагрузочный комплекс, предназначенный для оценки работоспособности   
            сердца при физической нагрузке.
            У испытуемого, находящегося в положении лежа на спине в течение 5 мин,
            определяют частоту пульса за 15 секунд; затем в течение 45 секунд испытуемый выполняет 30 приседаний.
            После окончания нагрузки испытуемый ложится, и у него вновь подсчитывается число пульсаций за первые
            15 секунд, а потом — за последние 15 секунд первой минуты периода восстановления.
            Важно! Если в процессе проведения испытания вы почувствуете себя плохо (появится головокружение,
            шум в ушах, сильная одышка и др.), то тест необходимо прервать и обратиться к врачу!"""

txt_title = 'Здоровье'

txt_test1 = """Лягте на спину, отдохните пять минут. 
После отдыха замерьте пульс за 15 секунд. 
Нажмите кнопку "Начать", чтобы запустить таймер.
Результат запишите в соответствующее поле."""

txt_up_1 = 'Считайте пульс'
txt_bottom_1 = 'секунд'

txt_test2 = """Выполните 30 приседаний за 45 секунд. 
Нажмите кнопку "Начать", чтобы запустить счетчик приседаний.
Делайте приседания со скоростью счетчика.
Важно! 
Если в процессе проведения испытания вы почувствуете себя плохо 
(появится головокружение, шум в ушах, сильная одышка и др.), 
то тест необходимо прервать и обратиться к врачу.
"""
txt_up_2 = 'Вы сделали'
txt_bottom_2 = 'приседаний'

txt_test3 = """Лягте на спину.
В течение минуты замерьте пульс два раза: 
за первые 15 секунд минуты, затем за последние 15 секунд.
Нажмите кнопку "Начать", чтобы запустить таймер.
Число секунд будет писаться зелёным цветов в те периоды, 
когда нужно вести измерение, 
красным - во время перерыва между двумя замерами. 
Результаты запишите в соответствующие поля.
"""
txt_up_3 = 'Отдыхайте'
txt_res = 'Результат:'
txt_res2 = 'Результат после отдыха:'
txt_hinttest = '0'
txt_hintage = '7'


class Counter(QWidget):
    """ Виджет для визуализации счетчика: умеет отсчитывать числа от A до B с данной задержкой """

    def __init__(self, start_value=15, parent=None, flags=Qt.WindowFlags()):
        """ При создании виджета достаточно указать одно значение счетчика: 
        оно будет показываться, пока счетчик не запущен """
        super().__init__(parent=parent, flags=flags)
        self.current_value = start_value
        # Нужно понимать, когда счетчик прекратил свою работу
        # Правильный способ для этого - создать в классе свой сигнал и посылать его в нужный момент
        # но если не хватает времени разобраться с созданием своих сигналов?
        # Добавим в класс невидимую кнопку:
        self.btn_finished = QPushButton()
        # кнопку можно нажимать программно, и можно коннектиться к сигналу counter.btn_finished.clicked
        # Она не участвует в интерфейсе. Всё, что рисуется, в этом методе:
        self.initUI()

    def initUI(self):
        """ метод создает визуальные компоненты счетчика и размещает их"""
        self.lb_value = QLabel(str(self.current_value))  # надпись, в которой отражено текущее значение счетчика
        self.dial = QDial()  # "крутилка": виджет, с помощью которого проще синхронизироваться с переключением значений
        # время, которое отводится на один шаг счетчика, всегда делится на 10 частей
        # крутилка за одну часть поворачивается на одно деление - от 0 к 1, от 1 к 2, ..., от 9 к 10
        self.dial.setMinimum(0)  # первое деление - ноль
        self.dial.setMaximum(10)  # последнее деление - десять
        self.dial.setValue(0)  # пока все стоит на минимуме
        # размещаем надпись и крутилку в строчку:
        lay = QHBoxLayout()
        lay.addWidget(self.lb_value)
        lay.addWidget(self.dial)
        self.setLayout(lay)

    def start(self, start_value=15, speed=1000, step=-1, finish=0):
        """ начинает работу счетчика, для чего надо получить начальное и конечное значение, 
        величину шага, и сколько миллисекунд отводится на один шаг.
        метод работает некорректно, если вызывать несколько раз, не дожидаясь конца работы счетчика. """
        # загружаем полученные значения в свойства счетчика:
        self.current_value = start_value
        self.lb_value.setText(str(self.current_value))
        self.step = step
        self.finish = finish
        self.speed = speed // 10  # нам нужно время для прохождения одного деления "крутилки"
        # запускаем таймер (по-хорошему стоит сначала убивать старый таймер и создавать новый, 
        # тогда метод станет корректным, но мы просто заблокируем кнопки в интерфейсе): 
        self.timer = self.startTimer(self.speed)

    def timerEvent(self, event):
        """ стандартный метод класса Виджет, который вызывается, когда срабатывает событие встроенного в виджет таймера
        переопределяем его так, чтобы счетчик продвигался на одно деление, а в конце убивал таймер и посылал сигнал об остановке"""
        val = self.dial.value()
        if val < self.dial.maximum():
            # крутилка не дошла до конца, крутим дальше:
            self.dial.setValue(val + 1)
        else:
            # круг сделан, это еще один шаг счетчика:
            self.current_value += self.step
            self.dial.setValue(self.dial.minimum())
            self.lb_value.setText(str(self.current_value))
            # проверка, не достигли ли финишного значения 
            # можно использовать условие self.current_value == self.finish
            # напишем более корректный вариант, на случай неточного попадания в целевое значение: 
            if abs(self.current_value - self.finish) < abs(self.step):
                self.killTimer(self.timer)  # пока, таймер!
                self.btn_finished.click()  # сигнал можно использовать извне счетчика


class TestWindow(QWidget):
    """ Общий класс для проведения этапа теста
    размещает в окне всю информацию:
    "этап номер ...", инструкцию, кнопку "начать", счетчик с подписями, поле ввода результата, кнопки "к инструкции" и "далее" """

    def __init__(self, stage=1, instruction='', up_text='', bottom_text='', counter_start=15, parent=None,
                 flags=Qt.WindowFlags()):
        """  нужно знать: номер этапа, инструкцию этапа, подписи к счетчику, значение счетчика для показа в остановленном состоянии"""
        super().__init__(parent=parent, flags=flags)
        # рисуем всё, что входит в этап, располагая в подходящих макетах:
        self.initUI(stage, instruction, up_text, bottom_text, counter_start)
        self.set_appear()  # размеры и положение окна
        self.connects()  # внутри этапа обрабатывается кнопка "начать".
        # В обычном случае это значит вызов метода start(),
        # который дезактивирует все кнопки и запускает start счетчика со значениями по умолчанию
        # метод ended() тоже описан в этом классе, - в общем случае
        # после конца работы счетчика надо "воскресить" кнопки.
        # Но мы не прописываем в connects() вызов метода ended по сигналу от счетчика,
        # потому что есть вариант, когда счетчик надо несколько раз запускать.

    def initUI(self, stage, instruction, up_text, bottom_text, counter_start):
        """ Создает все нужные виджеты, долго и муторно наводит красоту, расставляя их по макетам """
        self.setStyleSheet(Style_regular + Style_middle)  # применяем шрифт "обычный, среднего размера" ко всем виджетам

        v_layout = QVBoxLayout()  # главный макет: основное размещение - в столбик
        # вверху в центре - номер этапа, написанный жирным большим шрифтом
        lb_name = QLabel("Этап " + str(stage))
        lb_name.setStyleSheet(Style_bold + Style_large)
        v_layout.addWidget(lb_name, alignment=Qt.AlignHCenter)
        # дальше строка, в которой слева инструкция, под ней кнопка "начать", а справа - счетчик и подписи к нему (сверху и снизу)
        h_l1 = QHBoxLayout()
        v_l11 = QVBoxLayout()  # левый столбик
        lb_instruction = QLabel(instruction)
        self.btn_start = QPushButton("Начать")
        v_l11.addWidget(lb_instruction, alignment=Qt.AlignLeft)
        v_l11.addWidget(self.btn_start, alignment=Qt.AlignHCenter)
        v_l12 = QVBoxLayout()  # правый столбик
        self.lb_up = QLabel(up_text)
        self.lb_bottom = QLabel(bottom_text)
        self.counter = Counter(start_value=counter_start)
        self.counter.setStyleSheet(
            Style_bold + Style_large + Style_green)  # к счетчику применяется большой жирный зеленый шрифт
        v_l12.addWidget(self.lb_up, alignment=Qt.AlignHCenter)
        v_l12.addWidget(self.counter, alignment=Qt.AlignHCenter)
        v_l12.addWidget(self.lb_bottom, alignment=Qt.AlignHCenter)
        h_l1.addLayout(v_l11)
        h_l1.addLayout(v_l12)
        v_layout.addLayout(h_l1)  # готова строка
        v_layout.addStretch(1)  # отступ
        # количество результатов может быть разным. Мы будем переписывать его в классах-наследниках этого!
        # Для того, чтобы не менять этот метод, а в другом месте вписать сюда строку или убрать, 
        # заведем виджет типа "группа" и сделаем его свойством экземпляра:
        self.res_group = QGroupBox()
        # добавляем в эту группу одну строку
        self.line_result1 = QLineEdit()  # этот виджет должен быть доступен как свойство,
        # мы будем отсюда получать результаты тестирования!
        self.results_layout = QVBoxLayout()  # макет для группы
        self.add_result_line(txt_res,
                             self.line_result1)  # размещаем строку отдельным методом, чтобы повторять, когда потребуется
        self.res_group.setLayout(self.results_layout)
        v_layout.addWidget(self.res_group)
        # группа с результатами добавлена, дальше разрыв и кнопки:
        v_layout.addStretch(1)
        self.btn_back = QPushButton('К инструкции')
        self.btn_next = QPushButton('Далее')
        self.btn_next.setDisabled(True)
        h_l2 = QHBoxLayout()  # кнопки размещаются в строчку
        h_l2.addStretch(1)
        h_l2.addWidget(self.btn_back)
        h_l2.addStretch(1)
        h_l2.addWidget(self.btn_next)
        h_l2.addStretch(1)
        v_layout.addLayout(h_l2)  # добавили строку с кнопками в общий столбец
        # все готово, устанавливаем получившийся макет экземпляру класса: 
        self.setLayout(v_layout)

    def add_result_line(self, text, edit: QLineEdit):
        """ метод добавляет в макет results_layout строку из надписи и поля ввода результата"""
        edit.setText(txt_hinttest)  # ставим значение по умолчанию
        edit.setValidator(
            QIntValidator(0, 150))  # включаем проверку, что можно написать только целое число до 3-х знаков
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(QLabel(text))
        h_layout.addWidget(edit)
        h_layout.addStretch(1)
        self.results_layout.addLayout(h_layout)

    def set_appear(self):
        """ общие параметры окна """
        self.setWindowTitle(txt_title)
        self.resize(win_test_width, win_test_height)
        self.move(win_x, win_y)

    def connects(self):
        """ соединения сигнал-слот, которые работают одинаково для всех этапов """
        self.btn_start.clicked.connect(self.start)

    def start(self):
        """ после нажатия кнопки "начать" нельзя больше ничего нажимать
        запускается счетчик этапа """
        self.btn_start.setDisabled(True)
        self.btn_back.setDisabled(True)
        self.counter.start()

    def ended(self):
        """ когда все закончилось, мы возвращаем кнопки """
        self.btn_start.setDisabled(False)
        self.btn_next.setDisabled(False)  # теперь можно идти дальше! (раньше нельзя совсем)
        self.btn_back.setDisabled(False)
        self.line_result1.setFocus(Qt.TabFocusReason)  # фокус в поле ввода, параметр Qt.TabFocusReason
        # означает буквально
        # "поставь фокус таким же способом, как при нажатии Tab"
        # - это позволяет выделить текущее значение, экономим один delete


class Test1(TestWindow):
    """ экземпляр окна для первого этапа текста """

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        # создаем TestWindow с нужными параметрами (этап 1, инструкция 1 и т.д.)
        super().__init__(stage=1,
                         instruction=txt_test1,
                         up_text=txt_up_1,
                         bottom_text=txt_bottom_1,
                         counter_start=15,
                         parent=parent, flags=flags)
        # в базовом классе нет связи сигнала об окончании работы счетчика с методом ended()
        # потому что иногда надо другое делать, но тут не надо, связываем напрямую:
        self.counter.btn_finished.clicked.connect(self.ended)


class Test2(TestWindow):
    """ экземпляр окна для второго этапа текста """

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        # создаем TestWindow с нужными параметрами (этап 2, инструкция 2 и т.д.)
        super().__init__(stage=2,
                         instruction=txt_test2,
                         up_text=txt_up_2,
                         bottom_text=txt_bottom_2,
                         counter_start=0,
                         parent=parent, flags=flags)

        self.res_group.hide()  # на этом этапе никакие результаты не вводятся, убираем группу результатов с глаз долой!
        # связываем сигнал об окончании счетчика с ended()
        self.counter.btn_finished.clicked.connect(self.ended)

    def start(self):
        # обновляем метод start() - нам нужны нестандартные значения для запуска счетчика!
        self.btn_start.setDisabled(True)
        self.btn_back.setDisabled(True)
        # счетчик работает со скоростью 1,5 секунды на раз, считает от 0 до 30 (приседаний):
        self.counter.start(start_value=0, speed=1500, step=1, finish=30)


class Test3(TestWindow):
    """ экземпляр окна для третьего этапа текста """

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        # создаем TestWindow с нужными параметрами (этап 3, инструкция 3 и т.д.)
        super().__init__(stage=3,
                         instruction=txt_test3,
                         up_text=txt_up_1,
                         bottom_text=txt_bottom_1,
                         counter_start=15,
                         parent=parent, flags=flags)
        # добавляем в группу результатов еще одну строку, там будет второй результат:
        self.line_result2 = QLineEdit()
        self.add_result_line(txt_res2, self.line_result2)
        # счетчик на этом этапе запускается 3 раза. При нажатии на старт нужно обнулять количество запусков:
        self.btn_start.clicked.connect(self.start_counts)
        # сигнал об окончании счетчика связываем с новым методом check_counts:
        self.counter.btn_finished.clicked.connect(self.check_counts)

    def start_counts(self):
        # Обнуляет свойство для подсчета запусков:    
        self.counting = 0

    def check_counts(self):
        """ перезапускает или останавливает счетчик"""
        self.counting += 1
        if self.counting == 1:
            # второй запуск - это 30 секунд перерыва
            self.counter.setStyleSheet(Style_bold + Style_large + Style_red)  # пишем большим жирным и красным шрифтом
            self.counter.start(start_value=30)  # меняем стартовое значение
            self.lb_up.setText(txt_up_3)  # меняем подпись к счетчику
        elif self.counting == 2:
            # третий запуск - считаем пульс опять
            self.counter.setStyleSheet(Style_bold + Style_large + Style_green)  # снова зелено
            self.counter.start(start_value=15)
            self.lb_up.setText(txt_up_1)
        else:
            self.ended()  # достаточно


class MainWindow(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        """ первое окно - приветствие, инструкция, ввод общих параметров """
        super().__init__(parent=parent, flags=flags)
        # создаём и настраиваем графические эелементы:
        self.initUI()
        # устанавливает, как будет выглядеть окно (надпись, размер, место)
        self.set_appear()
        # старт - это окно видно по факту запуска программы:
        self.show()

    def initUI(self):
        """ создает графические элементы """
        self.setStyleSheet(Style_regular + Style_middle)  # шрифт - средний обычный
        # создаем все элементы:
        self.btn_test = QPushButton(txt_next)
        self.lbl_hello = QLabel(txt_hello)
        self.lbl_instruction = QLabel(txt_instruction)
        self.line_age = QLineEdit(txt_hintage)
        self.line_age.setValidator(QIntValidator(7, 120))
        self.line_name = QLineEdit()
        self.group = QGroupBox()  # форму ввода информации разместим в этой группе
        # размещаем их (главный макет - столбик)
        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        v_layout.addWidget(self.lbl_hello, alignment=Qt.AlignHCenter)
        v_layout.addWidget(self.lbl_instruction, alignment=Qt.AlignHCenter)

        layout_form = QFormLayout()
        layout_form.addRow('Введите ФИО:', self.line_name)
        layout_form.addRow('Возраст:', self.line_age)

        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addLayout(layout_form)
        h_layout.addStretch(2)

        self.group.setLayout(h_layout)

        v_layout.addStretch(1)
        v_layout.addWidget(self.group)
        v_layout.addWidget(self.btn_test, alignment=Qt.AlignCenter)

        self.setLayout(v_layout)

    def set_appear(self):
        """ устанавливает, как будет выглядеть окно (надпись, размер, место) """
        self.setWindowTitle(txt_title)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

    def showresults(self, text1, text2):
        """ я открываюсь под конец...
        метод, после которого в окне остаются только переданные строки"""
        text1 = self.line_name.text() + ', ' + text1  # Обратимся к человеку по введённому имени
        # больше ничего нельзя сделать:
        self.btn_test.hide()
        self.group.hide()
        self.setStyleSheet(Style_regular + Style_large)  # у нас теперь много места, меняем шрифт соответственно
        # вписываем переданные результаты
        self.lbl_hello.setText(text1)
        self.lbl_instruction.setText(text2)


class RuffierApp():
    """ класс для создания нужных окон в программе "тест Руфье": 
    первое окно и три теста, они все связаны соответствующими кнопками"""

    def __init__(self):
        """ создаем, связываем"""
        self.first_win = MainWindow()
        self.test1 = Test1()
        self.test2 = Test2()
        self.test3 = Test3()
        self.cur_test = self.test1  # ссылка на текущий этап
        self.connects()  # связи

    def goto_test(self):
        """ переход из первого окна в текущий тест """
        self.first_win.btn_test.setText(txt_back)  # кнопка уже не должна называться "начать", мы начали
        self.first_win.hide()
        self.cur_test.show()

    def back(self):
        """ возврат из текущего теста в первое окно """
        self.cur_test.hide()
        self.first_win.show()

    def next_to2(self):
        """ переход ко второму этапу теста """
        self.cur_test.hide()
        self.test2.show()
        self.cur_test = self.test2

    def next_to3(self):
        """ переход к третьему этапу теста """
        self.cur_test.hide()
        self.test3.btn_next.setText(txt_finish)
        self.test3.show()
        self.cur_test = self.test3

    def finish(self):
        """ окончание работы программы: считаем результаты и вывешиваем их в главном окне """
        # получаем информацию из нужных полей ввода 
        P1 = int(self.test1.line_result1.text())
        P2 = int(self.test3.line_result1.text())
        P3 = int(self.test3.line_result2.text())
        age = int(self.first_win.line_age.text())
        # используем функцию ruffier.test для обсчета
        # она возвращат кортеж из двух готовых строк, их остается только передать окну 
        results = ruffier.test(P1, P2, P3, age)
        self.first_win.showresults(results[0], results[1])
        # показываем первое окно с результатами
        self.back()

    def connects(self):
        """ установка соединений для переходам между окнами по соответствующим кнопкам """
        self.first_win.btn_test.clicked.connect(self.goto_test)
        self.test1.btn_back.clicked.connect(self.back)
        self.test2.btn_back.clicked.connect(self.back)
        self.test3.btn_back.clicked.connect(self.back)
        self.test1.btn_next.clicked.connect(self.next_to2)
        self.test2.btn_next.clicked.connect(self.next_to3)
        self.test3.btn_next.clicked.connect(self.finish)


def main():
    app = QApplication([])
    ra = RuffierApp()  # если не присвоить результат переменной, то сборщик мусора python выкинет все созданные окна )))
    app.exec()


main()
