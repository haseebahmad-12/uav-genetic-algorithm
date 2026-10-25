"""Central configuration for the toy UAV mission simulation."""
CONFIG = {
    "grid_size": 50,
    "num_waypoints": 8,
    "population_size": 60,
    "generations": 100,
    "mutation_rate": 0.18,
    "crossover_rate": 0.85,
    "tournament_size": 4,
    "max_range": 220.0,
    "coverage_radius": 5.5,
    "sensor_min": 0.2,
    "sensor_max": 1.0,
    "seed": 42,
    "start": (2.0, 2.0),
    "goal": (47.0, 47.0),
    # Rectangular no-fly areas: (x_min, y_min, x_max, y_max)
    "no_fly_zones": [(16, 10, 23, 30), (30, 28, 38, 39)],
    # Simulated hazard centers and radii: (x, y, radius)
    "hazards": [(11, 34, 7), (36, 14, 8), (27, 43, 5)],
    "weights": {
        "coverage": 12.0,
        "energy": 0.035,
        "time": 0.045,
        "risk": 1.4,
        "constraint_penalty": 30.0,
    },
}
