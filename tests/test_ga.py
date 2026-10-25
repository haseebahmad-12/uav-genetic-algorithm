import unittest
from config import CONFIG
from uav_ga import GeneticAlgorithm

class TestGeneticAlgorithm(unittest.TestCase):
    def test_chromosome_size_and_bounds(self):
        ga = GeneticAlgorithm(CONFIG)
        individual = ga.random_individual()
        self.assertEqual(len(individual.genes), CONFIG["num_waypoints"])
        for x, y, power in individual.genes:
            self.assertTrue(0 <= x < CONFIG["grid_size"])
            self.assertTrue(0 <= y < CONFIG["grid_size"])
            self.assertTrue(CONFIG["sensor_min"] <= power <= CONFIG["sensor_max"])

    def test_evaluation_returns_number(self):
        ga = GeneticAlgorithm(CONFIG)
        individual = ga.random_individual()
        score = ga.evaluate(individual)
        self.assertTrue(isinstance(score, float))
        self.assertIsNotNone(individual.metrics)

if __name__ == "__main__":
    unittest.main()
