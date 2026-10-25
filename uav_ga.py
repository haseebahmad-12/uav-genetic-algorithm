"""Object-oriented Genetic Algorithm for multi-objective UAV route planning."""
from dataclasses import dataclass
import math
import random

@dataclass
class Individual:
    # Each gene is (x, y, sensor_power), with coordinates in [0, grid_size-1].
    genes: list
    fitness: float = float("-inf")
    metrics: dict = None

class GeneticAlgorithm:
    def __init__(self, config):
        self.cfg = config
        self.rng = random.Random(config["seed"])
        self.size = config["grid_size"]
        self.population = [self.random_individual() for _ in range(config["population_size"])]

    def random_individual(self):
        genes = []
        for _ in range(self.cfg["num_waypoints"]):
            genes.append([
                self.rng.uniform(0, self.size - 1),
                self.rng.uniform(0, self.size - 1),
                self.rng.uniform(self.cfg["sensor_min"], self.cfg["sensor_max"]),
            ])
        return Individual(genes)

    def point_in_zone(self, x, y, zone):
        x1, y1, x2, y2 = zone
        return x1 <= x <= x2 and y1 <= y <= y2

    def hazard_exposure(self, x, y):
        exposure = 0.0
        for hx, hy, radius in self.cfg["hazards"]:
            d = math.hypot(x - hx, y - hy)
            if d < radius:
                exposure += (radius - d) / radius
        return exposure

    def evaluate(self, individual):
        start, goal = self.cfg["start"], self.cfg["goal"]
        points = [start] + [(g[0], g[1]) for g in individual.genes] + [goal]
        total_distance, risk, penalty = 0.0, 0.0, 0.0
        blocked = 0
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            distance = math.hypot(x2 - x1, y2 - y1)
            total_distance += distance
            # Sample each segment so a line crossing a no-fly zone is penalized.
            samples = max(2, int(distance / 1.5))
            for k in range(samples + 1):
                t = k / samples
                x, y = x1 + (x2-x1)*t, y1 + (y2-y1)*t
                risk += self.hazard_exposure(x, y) / samples
                if any(self.point_in_zone(x, y, z) for z in self.cfg["no_fly_zones"]):
                    blocked += 1
        sensor_energy = sum(g[2] ** 2 for g in individual.genes) * 3.0
        energy = total_distance * 0.65 + sensor_energy
        flight_time = total_distance / 5.0
        if total_distance > self.cfg["max_range"]:
            penalty += total_distance - self.cfg["max_range"]
        penalty += blocked * 2.0
        # Coverage reward: waypoint sensor footprints cover high-priority targets.
        targets = [(8, 8), (8, 42), (25, 7), (27, 35), (43, 22), (43, 43), (18, 39), (35, 5)]
        covered = 0.0
        for tx, ty in targets:
            best = 0.0
            for x, y, power in individual.genes:
                d = math.hypot(tx-x, ty-y)
                contribution = power if d <= self.cfg["coverage_radius"] else 0.0
                best = max(best, contribution)
            covered += best
        coverage = covered / len(targets)
        w = self.cfg["weights"]
        fitness = (w["coverage"] * coverage
                   - w["energy"] * energy
                   - w["time"] * flight_time
                   - w["risk"] * risk
                   - w["constraint_penalty"] * penalty)
        individual.fitness = fitness
        individual.metrics = {
            "coverage": coverage, "energy": energy, "time": flight_time,
            "risk": risk, "penalty": penalty, "distance": total_distance,
        }
        return fitness

    def tournament_select(self, population):
        contestants = self.rng.sample(population, min(self.cfg["tournament_size"], len(population)))
        return max(contestants, key=lambda ind: ind.fitness)

    def crossover(self, parent1, parent2):
        # Segment-wise crossover: each waypoint triple is inherited from either parent.
        child1, child2 = [], []
        for a, b in zip(parent1.genes, parent2.genes):
            if self.rng.random() < 0.5:
                child1.append(a[:]); child2.append(b[:])
            else:
                child1.append(b[:]); child2.append(a[:])
        return Individual(child1), Individual(child2)

    def mutate(self, individual):
        for gene in individual.genes:
            if self.rng.random() < self.cfg["mutation_rate"]:
                gene[0] += self.rng.gauss(0, 5.0)
                gene[1] += self.rng.gauss(0, 5.0)
            if self.rng.random() < self.cfg["mutation_rate"]:
                gene[2] += self.rng.gauss(0, 0.12)
            gene[0] = min(max(gene[0], 0.0), self.size - 1.0)
            gene[1] = min(max(gene[1], 0.0), self.size - 1.0)
            gene[2] = min(max(gene[2], self.cfg["sensor_min"]), self.cfg["sensor_max"])

    def run(self):
        history = {"best": [], "average": []}
        for generation in range(self.cfg["generations"]):
            for ind in self.population:
                self.evaluate(ind)
            self.population.sort(key=lambda ind: ind.fitness, reverse=True)
            scores = [ind.fitness for ind in self.population]
            history["best"].append(scores[0])
            history["average"].append(sum(scores) / len(scores))
            # Elitism: retain the two strongest individuals.
            next_population = [self.clone(self.population[0]), self.clone(self.population[1])]
            while len(next_population) < self.cfg["population_size"]:
                p1 = self.tournament_select(self.population)
                p2 = self.tournament_select(self.population)
                if self.rng.random() < self.cfg["crossover_rate"]:
                    c1, c2 = self.crossover(p1, p2)
                else:
                    c1, c2 = self.clone(p1), self.clone(p2)
                self.mutate(c1); self.mutate(c2)
                next_population.append(c1)
                if len(next_population) < self.cfg["population_size"]:
                    next_population.append(c2)
            self.population = next_population
        for ind in self.population:
            self.evaluate(ind)
        return max(self.population, key=lambda ind: ind.fitness), history

    @staticmethod
    def clone(individual):
        return Individual([gene[:] for gene in individual.genes], individual.fitness,
                          dict(individual.metrics) if individual.metrics else None)
