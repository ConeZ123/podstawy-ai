import random
import time

weights = [2, 3, 5, 7, 1, 4, 6, 8, 9, 3]
values = [6, 5, 8, 9, 3, 7, 10, 11, 13, 6]

CAPACITY = 20

POPULATION_SIZE = 100
MAX_GENERATIONS = 10000
MUTATION_RATE = 0.03

N = len(weights)

def fitness(individual):
    total_weight = 0
    total_value = 0

    for i in range(N):
        if individual[i] == 1:
            total_weight += weights[i]
            total_value += values[i]

    if total_weight > CAPACITY:
        return -1000 - (total_weight - CAPACITY)

    return total_value

def create_individual():
    return [random.randint(0, 1) for _ in range(N)]

def crossover(parent1, parent2):
    point = random.randint(1, N - 1)

    child = parent1[:point] + parent2[point:]

    return child

def mutate(individual):
    for i in range(N):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]

    return individual

def solve():
    start_time = time.time()

    population = [
        create_individual()
        for _ in range(POPULATION_SIZE)
    ]

    best = None
    best_score = -float("inf")

    for generation in range(MAX_GENERATIONS):
        population.sort(key=fitness, reverse=True)

        current_best = population[0]
        current_score = fitness(current_best)

        if current_score > best_score:
            best = current_best.copy()
            best_score = current_score

        if best_score == 38:
            break

        new_population = population[:2]

        while len(new_population) < POPULATION_SIZE:

            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])

            child = crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    elapsed = time.time() - start_time

    return best, generation, elapsed


best, generation, elapsed = solve()

total_weight = sum(
    weights[i] for i in range(N) if best[i] == 1
)

total_value = sum(
    values[i] for i in range(N) if best[i] == 1
)

print("Najlepsze rozwiązanie:", best)
print("Wybrane przedmioty:")

for i in range(N):
    if best[i] == 1:
        print("Przedmiot", i + 1,
              "- waga:", weights[i],
              "- wartość:", values[i])

print("Łączna waga:", total_weight)
print("Łączna wartość:", total_value)
print("Pokolenie:", generation)
print("Czas działania:", round(elapsed, 4), "s")
