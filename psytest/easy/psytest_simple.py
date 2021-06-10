""" Пример, как можно сделать опросник самыми простыми средствами
Такую программу легко написать, но сложно менять и трудно находить ошибки"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QGroupBox, QRadioButton, QPushButton, QLabel)

# для выбора альтернатив используем переключатели QRadioButton
# в пределах одной группы QGroupBox можно включить только один QRadioButton
# - так уже работают эти виджеты, ничего самостоятельно писать не надо.

app = QApplication([])

layoutV = QVBoxLayout()  # все вопросы будут расположены в столбец

gr_1 = QGroupBox(' Вопрос 1')  # группа
quest1_1 = QRadioButton('Ухаживать за животными')  # вопрос 1
quest1_2 = QRadioButton('Обслуживать машины')  # вопрос 2
layoutH_1 = QHBoxLayout()  # расположим вопросы в строку
layoutH_1.addWidget(quest1_1, alignment=Qt.AlignHCenter)
layoutH_1.addWidget(quest1_2, alignment=Qt.AlignHCenter)
gr_1.setLayout(layoutH_1)  # строка с переключателями - макет для группы
# теперь у переключателей один родитель, и пользователь сможет включить только один!
layoutV.addWidget(gr_1)  # а сама группа добавляется в вертикальный макет

# Дальше повторяем то же много раз.
# Программирование "методом копипаста" помогает быстрее писать, но
# каждый раз нужно вносить небольшие изменения. И если в этих изменениях опечататься, 
# найти проблему будет сложно... 
gr_2 = QGroupBox(' Вопрос 2')
quest2_1 = QRadioButton('Помогать больным людям, лечить их')
quest2_2 = QRadioButton('Составлять таблицы, схемы, программы для вычислительных машин')
layoutH_2 = QHBoxLayout()
layoutH_2.addWidget(quest2_1, alignment=Qt.AlignHCenter)
layoutH_2.addWidget(quest2_2, alignment=Qt.AlignHCenter)
gr_2.setLayout(layoutH_2)
layoutV.addWidget(gr_2)

gr_3 = QGroupBox(' Вопрос 3')
quest3_1 = QRadioButton('Участвовать в оформлении книг, плакатов,  журналов')
quest3_2 = QRadioButton('Следить за состоянием и развитием растений')
layoutH_3 = QHBoxLayout()
layoutH_3.addWidget(quest3_1, alignment=Qt.AlignHCenter)
layoutH_3.addWidget(quest3_2, alignment=Qt.AlignHCenter)
gr_3.setLayout(layoutH_3)
layoutV.addWidget(gr_3)

gr_4 = QGroupBox(' Вопрос 4')
quest4_1 = QRadioButton('Обрабатывать материалы (древесину, ткань, металл, пластмассу и др.)')
quest4_2 = QRadioButton('Доводить товары до потребителя (рекламировать)')
layoutH_4 = QHBoxLayout()
layoutH_4.addWidget(quest4_1, alignment=Qt.AlignHCenter)
layoutH_4.addWidget(quest4_2, alignment=Qt.AlignHCenter)
gr_4.setLayout(layoutH_4)
layoutV.addWidget(gr_4)

gr_5 = QGroupBox(' Вопрос 5')
quest5_1 = QRadioButton(' Обсуждать научно-популярные книги, статьи')
quest5_2 = QRadioButton('Обсуждать художественные книги (или пьесы, концерты)')
layoutH_5 = QHBoxLayout()
layoutH_5.addWidget(quest5_1, alignment=Qt.AlignHCenter)
layoutH_5.addWidget(quest5_2, alignment=Qt.AlignHCenter)
gr_5.setLayout(layoutH_5)
layoutV.addWidget(gr_5)

gr_6 = QGroupBox(' Вопрос 6')
quest6_1 = QRadioButton('Содержать животных')
quest6_2 = QRadioButton('Тренировать товарищей (или младших школьников) в выполнении каких-либо действий (трудовых, '
                        'учебных, спортивных)')
layoutH_6 = QHBoxLayout()
layoutH_6.addWidget(quest6_1, alignment=Qt.AlignHCenter)
layoutH_6.addWidget(quest6_2, alignment=Qt.AlignHCenter)
gr_6.setLayout(layoutH_6)
layoutV.addWidget(gr_6)

gr_7 = QGroupBox(' Вопрос 7')
quest7_1 = QRadioButton('Копировать рисунки, изображения (или настраивать музыкальные инструменты)')
quest7_2 = QRadioButton('Управлять подъемным краном, трактором, тепловозом и т. п.')
layoutH_7 = QHBoxLayout()
layoutH_7.addWidget(quest7_1, alignment=Qt.AlignHCenter)
layoutH_7.addWidget(quest7_2, alignment=Qt.AlignHCenter)
gr_7.setLayout(layoutH_7)
layoutV.addWidget(gr_7)

gr_8 = QGroupBox(' Вопрос 8')
quest8_1 = QRadioButton('Сообщать (разъяснять) людям какие-либо сведения (в справочном бюро, на экскурсии)')
quest8_2 = QRadioButton('Художественно оформлять выставки, витрины (или участвовать в подготовке пьес, концертов)')
layoutH_8 = QHBoxLayout()
layoutH_8.addWidget(quest8_1, alignment=Qt.AlignHCenter)
layoutH_8.addWidget(quest8_2, alignment=Qt.AlignHCenter)
gr_8.setLayout(layoutH_8)
layoutV.addWidget(gr_8)

gr_9 = QGroupBox(' Вопрос 9')
quest9_1 = QRadioButton('Ремонтировать вещи (одежду, технику), жилище')
quest9_2 = QRadioButton('Искать и исправлять ошибки в текстах, таблицах, рисунках')
layoutH_9 = QHBoxLayout()
layoutH_9.addWidget(quest9_1, alignment=Qt.AlignHCenter)
layoutH_9.addWidget(quest9_2, alignment=Qt.AlignHCenter)
gr_9.setLayout(layoutH_9)
layoutV.addWidget(gr_9)

gr_10 = QGroupBox(' Вопрос 10')
quest10_1 = QRadioButton('Лечить животных')
quest10_2 = QRadioButton('Выполнять вычисления, расчеты')
layoutH_10 = QHBoxLayout()
layoutH_10.addWidget(quest10_1, alignment=Qt.AlignHCenter)
layoutH_10.addWidget(quest10_2, alignment=Qt.AlignHCenter)
gr_10.setLayout(layoutH_10)
layoutV.addWidget(gr_10)


# Расположили 10 групп вопросов друг под другом.

def results():
    """ Функция возвращает число от 1 до 5 - это номер той группы, в которой больше всего ответов """
    r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0  # количества ответов в пяти группах
    # дальше прописываем правила, какой вариант ответа в какую группу попадает.
    # используем метод isChecked(), который отвечает, включен переключатель или нет: 
    if quest1_1.isChecked():
        r1 += 1  # этот ответ - в первой группе, увеличим соответствующий счетчик
    if quest1_2.isChecked():
        r2 += 1  # этот - во второй
    if quest2_1.isChecked():
        r3 += 1
    if quest2_2.isChecked():
        r4 += 1
    if quest3_1.isChecked():
        r5 += 1
    if quest3_2.isChecked():
        r1 += 1
    if quest4_1.isChecked():
        r2 += 1
    if quest4_2.isChecked():
        r3 += 1
    if quest5_1.isChecked():
        r4 += 1
    if quest5_2.isChecked():
        r5 += 1
    if quest6_1.isChecked():
        r1 += 1
    if quest6_2.isChecked():
        r3 += 1
    if quest7_1.isChecked():
        r5 += 1
    if quest7_2.isChecked():
        r2 += 1
    if quest8_1.isChecked():
        r3 += 1
    if quest8_2.isChecked():
        r5 += 1
    if quest9_1.isChecked():
        r2 += 1
    if quest9_2.isChecked():
        r4 += 1
    if quest10_1.isChecked():
        r1 += 1
    if quest10_2.isChecked():
        r4 += 1
    # Ура! И даже ничего не напутали?!
    # теперь разбираемся, где больше всего ответов:
    r_max = max(r1, r2, r3, r4, r5)
    if r_max == r1:
        return 1  # такой номер группы и возвращаем
    if r_max == r2:
        return 2
    if r_max == r3:
        return 3
    if r_max == r4:
        return 4
    if r_max == r5:
        return 5


def show_result():
    """ функция работает по нажатию на кнопку, показывает результат: какие профессии посоветуем тестируемому """
    r = results()  # получили номер группы профессий
    # берём текстовое описание группы по её номеру
    if 1 == r:
        text = ' «Человек—природа» — все профессии, связанные с растениеводством, животноводством и лесным хозяйством. '
    elif 2 == r:
        text = ' «Человек—техника» — все технические профессии. '
    elif 3 == r:
        text = ' «Человек—человек» — все профессии, связанные с обслуживанием людей, с общением. '
    elif 4 == r:
        text = '«Человек—знак» — все профессии, связанные с обсчетами, цифровыми буквенными знаками, в том числе и ' \
               'музыкальные специальности. '
    else:
        text = ' «Человек—художественный образ» — все творческие специальности. '
    # теперь окно с ответом
    global answer  # окно должно остаться после функции
    answer = QLabel(text)  # лень расставлять надписи в окне, сделаем просто надпись-окно.
    answer.resize(800, 300)
    answer.show()  # done.


# осталось создать основное окно:
main_w = QWidget()
main_w.setWindowTitle('Опросник')
btn_done = QPushButton('Готово!')
layoutV.addWidget(btn_done)  # добавили к куче вопросов кнопку
main_w.setLayout(layoutV)  # и этот макет теперь соответствует нашему окну
# связали нажатие на кнопку и функцию:
btn_done.clicked.connect(show_result)

# запускаем:
main_w.show()
app.exec()
