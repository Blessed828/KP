import random
import time
import statistics

# КОНСТАНТЫ (веса в граммах)
GOAL = 50000
NUM_RATS = 20
INITIAL_MIN_WT = 200
INITIAL_MAX_WT = 600
INITIAL_MODE_WT = 300
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 8
LITTERS_PER_YEAR = 10
GENERATION_LIMIT = 500
# обеспечить для племенных пар четное число крыс:
if NUM_RATS % 2 != 0:
    NUM_RATS += 1


def populate(num_rats, min_wt, max_wt, mode_wt):
    """Инициализировать популяцию треугольным расппределнием весов."""
    return [int(random.triangular(min_wt, max_wt, mode_wt)) \
            for i in range(num_rats)]


def fitness(population, goal):
    """Измерить пригодность популяции, основываясь на среднем значении атрибута относительно цели."""
    ave = statistics.mean(population)
    return ave / goal


def select(population, to_retain):
    """Отбраковать популяцию, оставив только заданное число ее членов."""
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain // 2
    members_per_sex = len(sorted_population) // 2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    return selected_males, selected_females


def breed(males, females):
    """Скрестить гены среди членов (весов) популяции."""
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        child = random.randint(female, male)
        children.append(child)
    return children


def mutate(children, mutate_odds, mutate_min, mutate_max):
    """Случайно изменить веса крыс, используя входные шансы и дробные изменения."""
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    return children


def main():
    """Инициализировать популяцию, отобрать, вывести и мутировать, показать результаты."""


generations = 0
parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)
print("первоночальные веса популяции = {}".format(parents))
popl_fitness = fitness(parents, GOAL)
print("первоначальная приспособленность популяции = {}".format(popl_fitness))
print("оставляемое число = {}".format(NUM_RATS))
ave_wt = []
while popl_fitness < 1 and generations < GENERATION_LIMIT:
    selected_males, selected_females = select(parents, NUM_RATS)
    children = breed(selected_males, selected_females)
    children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
    parents = selected_males + selected_females + children
    popl_fitness = fitness(parents, GOAL)
    print("Приспособленность поколения {} = {:.4f}".format(generations, popl_fitness))
    ave_wt.append(int(statistics.mean(parents)))
    generations += 1
    print("средний вес на поколоение = {}".format(ave_wt))
    print("\nчисло поколений = {}".format(generations))
    print("число лкт = {}".format(int(generations) / LITTERS_PER_YEAR))

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nВремя выполнения этой программы составило {} секунд.".format(duration))
