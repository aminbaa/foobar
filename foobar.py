import json
import csv

"""
Docstring for the class
"""


class FoobarClass:

    def __init__(self, name="FoobarBaseClass",
                 code_map='{"A1": "a", "A2": "b", "A3": "c", "A4": "d", "A5": "e", "A6": "f", "A7": "g"}',
                 answer='abcde',
                 max_score=20, ):
        """
        Initialize the class
        :param name: The class name
        :param code_map: A dictionary that specifies how the card labels should be converted to letters
        :param answer: The correct ordering of cards (by their label) translated into a string according to the code map
        :param max_score: The highest possible score
        """
        self.name = name
        self.code_map = json.loads(code_map)
        self.answer = answer
        self.max_score = max_score
        self.result_students = []
        self.data = []

    def levenshtein_score(self, source_string):
        """
        Implementation of the Levenshtein Algorithm from Wikipedia article
        https://en.wikipedia.org/wiki/Levenshtein_distance

        Also known as the edit distance

        For example, the Levenshtein Distance between "the" and "there" is 2; the letters "r" and "e"
        must be added to change "the" into "there"

        :param source_string: the string to be compared to the answer
        :return the number of edits to match the source with the answer, i.e. the number of incorrect cards
        """
        if source_string == self.answer:
            return 0
        if len(source_string) == 0:
            return len(self.answer)
        if len(self.answer) == 0:
            return len(source_string)
        v0 = [i for i in range(len(self.answer) + 1)]
        v1 = [0] * (len(self.answer) + 1)

        for i in range(len(source_string)):
            v1[0] = i + 1
            for j in range(len(self.answer)):
                cost = 0 if source_string[i] == self.answer[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(self.answer)]

    def transform_card_order_to_string(self, card_order):
        """
        Turn a list of card labels into a string for measurement

        For example, [A1, A2, A3] would become 'abc' based on the code map

        :param card_order: the input list of card labels
        :return: output_string: the list converted to a string
        """
        output_string = str()
        for card in card_order:
            output_string += self.code_map[card]

        return output_string

    def read_data(self, file_name):
        """
        The data should be read from the csv file supplied
        """
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            email_set = {'test@test.com'}
            result = []
            for item in csv_reader:
                if item[-1] not in email_set:
                    result.append(item)
                    email_set.add(item[-1])

        self.data = result


    def compute_score(self):
        """
        Each correct card is worth 4 points.  Each incorrect card should subtract 1 point.
        Scores less than zero should be scored as zero
        """
        result_students = []
        for answer_student in self.data:
            student = answer_student[-1]
            answer = answer_student[:-1]
            transformed_answer = self.transform_card_order_to_string(answer)
            incorrect = self.levenshtein_score(transformed_answer)
            raw_score = (len(answer) - incorrect) * 4 - incorrect
            percentage_correct = round(incorrect / len(answer), 2)
            result_students.append([student, raw_score, percentage_correct])

        result_students.sort(key=lambda x: x[1], reverse=True)

        self.result_students = result_students


    def write_student_scores(self):
        """
        The output format of the csv file should be:
        <student id>, <raw score>, <percentage correct>
        """
        with open('aaa.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(self.result_students)


foobar_class=FoobarClass()

foobar_class.read_data('student_responses.csv')

foobar_class.compute_score()

foobar_class.write_student_scores()
