# UAV Genetic Algorithm Strategy Engine

A small, reproducible Python simulation for the Artificial Intelligence Assignment 2. It uses a Genetic Algorithm (GA) to evolve UAV waypoint positions and sensor power settings on a 50 × 50 grid.

## Features
- Object-oriented chromosome (`Individual`): each waypoint is `(x, y, sensor_power)`.
- Random population initialization.
- Tournament selection and segment-wise crossover.
- Coordinate and sensor-power mutation with boundary repair.
- Fitness function rewards target coverage and penalizes energy, time, hazard exposure, no-fly-zone intersections, and excessive route length.
- Elitism and fixed-generation termination.
- Three plots: fitness convergence, evolved route, and sensor coverage heatmap.

## Requirements
- Python 3.10 or newer recommended.
- Install packages with `python -m pip install -r requirements.txt`.

## Run
```bash
python -m pip install -r requirements.txt
python main.py
```
Generated PNGs are saved in `outputs/`.

## Project structure
```text
uav-genetic-algorithm/
├── config.py
├── main.py
├── uav_ga.py
├── visualization.py
├── requirements.txt
├── README.md
├── .gitignore
├── outputs/
└── tests/
```

## Chromosome and fitness
Each individual contains 8 waypoint genes. A gene has x coordinate, y coordinate, and sensor power. The fitness is:

`fitness = 12*coverage - 0.035*energy - 0.045*time - 1.4*risk - 30*constraint_penalty`

Higher fitness is preferred. Coverage is the fraction-weighted detection of eight simulated high-priority targets. Energy combines route distance and sensor use. Flight time is route distance divided by an assumed speed. Risk increases when the path approaches simulated hazard pockets. Penalty is added for crossing no-fly zones or exceeding the maximum route range.

## Simulation assumptions and limitations
This is an educational toy model, not a real flight-control system. Coordinates, targets, hazards, flight speed, and fitness weights are simulated. Straight segments are sampled to estimate no-fly-zone intersections. The model does not represent real aircraft dynamics, weather, communications, or regulatory requirements.

## Suggested experiments
Change `population_size`, `mutation_rate`, and `tournament_size` in `config.py`, run again, and compare `outputs/fitness_convergence.png` and the final fitness. Keep a note of each setting and result for the technical report.

## Team contribution idea
For a team of three: (1) GA and fitness logic, (2) visualizations and experiments, (3) README/report and testing. Adjust this to reflect actual work.
