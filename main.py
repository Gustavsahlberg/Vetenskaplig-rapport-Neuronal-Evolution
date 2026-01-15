import random

POPULATION_SIZE = 100
GENES = [0, 1]

ITEMS = [
    ["A", 1, 1],
    ["B", 3, 4],
    ["C", 4, 5],
    ["D", 5, 7],
    ["E", 2, 3],#5
    ["F", 6, 9],
    ["G", 2, 2],
    ["H", 7, 11],
    ["I", 5, 8],
    ["J", 4, 6],#10
    ["K", 3, 5],
    ["L", 6, 10],
    ["M", 2, 4],
    ["N", 5, 9],
    ["O", 1, 2],#15
    ["P", 7, 12],
    ["Q", 4, 7],
    ["R", 3, 6],
    ["S", 2, 5],
    ["T", 6, 11],#20
    ["U", 5, 10],
    ["V", 4, 8],
    ["W", 7, 13],
    ["X", 1, 3],
    ["Y", 2, 6],#25


]

                                                                                         
              

BAG_CAP = 10


class Individual(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome  #[0,1,0,1]
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls):
        return random.choice(GENES)

    @classmethod
    def create_gnome(cls):
        gnome_len = len(ITEMS)
        return [cls.mutated_genes() for _ in range(gnome_len)]

    def mate(self, par2):
        child_chromosome = []
        for b1, b2 in zip(self.chromosome, par2.chromosome):
            prob = random.random()
            if prob < 0.45:
                child_chromosome.append(b1)
            elif prob < 0.90:
                child_chromosome.append(b2)
            else:
                child_chromosome.append(self.mutated_genes())
        return Individual(child_chromosome)

    def cal_fitness(self):
        total_weight = 0
        total_value = 0

        for bit, (name, w, v) in zip(self.chromosome, ITEMS):
            if bit == 1:
                total_weight += w
                total_value += v

        overweight = max(0, total_weight - BAG_CAP)
        penalty = 10_000 * overweight  

        return -total_value + penalty


def decode(chromosome):
    picked = []
    total_weight = 0
    total_value = 0
    for bit, (name, w, v) in zip(chromosome, ITEMS):
        if bit == 1:
            picked.append(name)
            total_weight += w
            total_value += v
    return picked, total_weight, total_value

def random_search(trials):
    best = None

    for _ in range(trials):
        chrom = Individual.create_gnome()
        ind = Individual(chrom)

        if best is None or ind.fitness < best.fitness:
            best = ind

    picked, w, v = decode(best.chromosome)
    print("\nRANDOM SEARCH BEST")
    print("picked:", picked, "weight:", w, "value:", v, "fitness:", best.fitness)
    return best



def main():
    generation = 1
    MAX_GENERATIONS = 500

    population = [Individual(Individual.create_gnome()) for _ in range(POPULATION_SIZE)]

    for _ in range(MAX_GENERATIONS):
        population = sorted(population, key=lambda x: x.fitness)
        best = population[0]

        chromoson = "".join(map(str, best.chromosome))
        picked, w, v = decode(best.chromosome)

        print(f"Gen {generation:3d} | chromoson {chromoson} | items {picked} | w={w} | v={v} | fitness={best.fitness}")

        # Ny generation
        new_generation = []
        elite = int(0.10 * POPULATION_SIZE)
        new_generation.extend(population[:elite])

        children = POPULATION_SIZE - elite
        for _ in range(children):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            new_generation.append(parent1.mate(parent2))

        population = new_generation
        generation += 1

    # Slutresultat
    population = sorted(population, key=lambda x: x.fitness)
    best = population[0]
    chromoson = "".join(map(str, best.chromosome))
    picked, w, v = decode(best.chromosome)

    print("\nFINAL BEST")
    print("chromoson:", chromoson)
    print("picked:", picked, "weight:", w, "value:", v, "fitness:", best.fitness)


if __name__ == "__main__":
    main()
    random_search(50000)
