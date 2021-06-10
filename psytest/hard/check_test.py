""" Проверка данных в файле, который импортируется первой строкой """
from klimov import *


def check_type_answers(questions, type_answers, types):
    """ проверяет, что в данных нет противоречий: каждый ответ встречается ровно 1 раз"""
    l_types = len(types)
    # количество описаний профессий равно количеству столбцов проверочной таблицы
    isCorrect = 0 < l_types == len(type_answers)
    if isCorrect:
        # проверка, что каждый тип содержит равное число ответов, нужна для теста Климова, не нужна для Голланда...
        total = len(questions) * 2  # всего ответов - в два раза больше, чем вопросов
        ta_quantity = total / l_types
        for column in type_answers:
            # в каждом столбце проверочной таблицы - нужное число элементов
            isCorrect = isCorrect and ta_quantity == len(column)
    else:
        print('Не проходит проверку: l_types > 0 and len(type_answers) == l_types ')
    if isCorrect:
        for i in range(1, len(questions) + 1):
            for j in range(1, 2):
                check_qty = 0
                for k in range(l_types):
                    if (i, j) in type_answers[k]:
                        check_qty += 1
                isCorrect = 1 == check_qty  # данная пара нашлась 1 раз
                if not isCorrect:
                    print('(', i, ',', j, ') встречается ', check_qty, 'раз')
                    break
            if not isCorrect:
                break
    else:
        print('Не проходит проверку: неравномерно распределены ответы по столбцам')
    print(isCorrect)


check_type_answers(test_choices, prf_type_answers, prf_types)
