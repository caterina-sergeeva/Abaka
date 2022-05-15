TASK_IS_NOT_VALIBLE = 1
ALREADY_PASSED = 2
WRONG_ANSWER = 3
ACCEPT = 4


class Crew:
    def __init__(self, name):
        self.name = name
        self.tasks = [0, 0, 0, 0, 0]
        self.score = 0

    def submit_a_task(self, task_category, task_number):
        if self.tasks[task_category] < task_number - 1:
            return TASK_IS_NOT_VALIBLE
        elif self.tasks[task_category] >= task_number:
            return ALREADY_PASSED
        else:
            return 34

    def accept(self, task_category, achievements):
        self.tasks[task_category] += 1
        q = self.tasks[task_category]
        self.score += q * 10
        w = set()
        if q == 5:
            if (task_category + 5) in achievements:
                w.add(task_category + 5)
                self.score += 100
            else:
                self.score += 50
        if self.tasks[0] >= q and self.tasks[1] >= q and self.tasks[2] >= q and self.tasks[3] >= q and self.tasks[
            4] >= q:
            if q in achievements:
                w.add(q)
                self.score += 20 * q
            else:
                self.score += 10 * q
        if self.tasks == [5, 5, 5, 5, 5]:
            if 10 in achievements:
                w.add(10)
                self.score += 200
            else:
                self.score += 100
        return w

    def get_score(self):
        return ' : '.join([str(self.name), str(self.score)])


class Game:
    def __init__(self, name_file):
        self.crews = {}
        self.answers = self.get_answers(name_file)
        # self.all_1 = 0  # сданы все первые задачи # 0
        # self.all_2 = 0  # сданы все вторые задачи # 1
        # self.all_3 = 0  # сданы все третьи задачи # 2
        # self.all_4 = 0  # сданы все четвёртые задачи # 3
        # self.all_5 = 0  # сданы все пятые задачи # 4
        # self.all_tasks_1 = 0  # сданы все задачи из первой категории # 5
        # self.all_tasks_2 = 0  # сданы все первые из второй категории # 6
        # self.all_tasks_3 = 0  # сданы все первые из третьей категории # 7
        # self.all_tasks_4 = 0  # сданы все первые из четвертой категории # 8
        # self.all_tasks_5 = 0  # сданы все первые из пятой категории # 9
        # self.all = 0  # сданы все задачи # 10
        # пояснения что означает каждая цифра в ачивках
        self.achievements = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def add_crew(self, name):
        self.crews[name] = Crew(name)

    def get_answers(self, name_file):
        f = open(name_file, mode='r')
        q = f.readlines()
        w = []
        for i in range(5):
            w.append([])
            for j in range(5):
                w[i].append(q[i * 5 + j][:-1])
        del w[4][-1]
        w[4].append(q[24])
        return w

    def answer(self, name, task_category, task_number,
               answer):  # категория - номер задачи // 5, номер - % 5, номерация с нуля для категории, с 1 для номера
        q = self.crews[name].submit_a_task(task_category, task_number)
        if q != 34:
            return q
        elif self.answers[task_category][task_number - 1] == answer:
            w = self.crews[name].accept(task_category, self.achievements)
            self.achievements = self.achievements - w
            return ACCEPT, w
        else:
            return WRONG_ANSWER

    def get_score(self):
        w = []
        for i in self.crews:
            w.append(self.crews[i].get_score())
        return '\n'.join(w)
