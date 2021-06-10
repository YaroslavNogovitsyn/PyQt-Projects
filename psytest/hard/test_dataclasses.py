from klimov import *


class TestQuestion:
    """ один элемент теста: две альтернативы (строки), из которых нужно выбрать."""
    def __init__(self, a1, a2):
        self.a1 = a1  # альтернатива 1
        self.a2 = a2  # альтернатива 2


def list_from_choices():
    """ в подключенном модуле с перечисленными данными должен быть список test_choices
    переводим этот список в список объектов типа TestQuestion"""
    list_test = []
    for choice in test_choices:
        question = TestQuestion(choice[1], choice[2])
        list_test.append(question)
    return list_test


class ProfessionType:
    """ каждый "тип профессий" имеет текстовое описание, а также помнит, какие ответы соответствуют этому типу """
    def __init__(self, description):
        self.description = description
        self.data = []

    def add_answer(self, list_index, answer_num):
        """ относит конкретный ответ на определенный вопрос к данному типу профессий.
        Вопросы обозначаются своим номером в источнике! """
        self.data.append((list_index - 1, answer_num))  # добавляем кортеж. 
        # ВАЖНО: в файле с данными варианты ответов нумеровали от 1 - так проще их перенести из источников но в
        # структуре наших данных нумерация получается от 0. Это учитывается здесь, мы вычитаем из полученного индекса
        # 1.

    def check(self, list_answers):
        """ по текущему списку проверяет, какие ответы попали в этот тип профессий.
        list_questions - это список формата (id, answer_number, answer_text).
        check составляет список из этих ответов (можно будет показать на экране)
        Возвращает количество ответов, соответствующих этому типу профессии."""
        self.answers = []
        for answer in list_answers:
            id = answer[0]
            answer_number = answer[1]
            if (id, answer_number) in self.data:
                # на такой длине данных и этот поиск должен работать достаточно быстро
                self.answers.append(answer[2])
        return len(self.answers)

    def normal(self, list_answers):
        """ Нормализует результат: возвращает, сколько процентов от максимума набрано.
            Нормализация нужна, если варианты неравномерно распределены по типам (как в тесте Голланда).
            Этот метод сначала вызовет check! Поэтому в приложении использовать или check, или normal, не оба."""
        qty = self.check(list_answers)
        total = len(self.data)
        if total > 0:
            return 100 * qty / total
        else:
            return 0


def list_from_types():
    """ в подключенном модуле с перечисленными данными должны быть списки prf_types, prf_type_answers
    используя эту информацию, создается список с экземплярами класса ProfessionType"""
    list_proftypes = []

    for i, type_descr in enumerate(prf_types):
        currtype = ProfessionType(type_descr)  # экземпляр хранит описание типа профессии
        for answer in prf_type_answers[i]:
            # добавляем, какие ответы соответствуют этому типу
            currtype.add_answer(answer[0], answer[1])
        list_proftypes.append(currtype)  # все экземпляры - в одном списке
    return list_proftypes
