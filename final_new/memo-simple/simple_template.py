""" Создаем окно с кнопкой """
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

app = QApplication([])

# виджеты, которые надо будет разместить:
btn_OK = QPushButton('Ответить')  # кнопка ответа
lb_Question = QLabel('Самый сложный вопрос в мире!')  # текст вопроса

# размещаем в окне друг под другом:
layout_card = QVBoxLayout()

layout_card.addWidget(lb_Question)
layout_card.addWidget(btn_OK)

window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memo Card')
window.show()

app.exec()
