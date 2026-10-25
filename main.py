"""Run the UAV Genetic Algorithm simulation and save visualizations."""
from uav_ga import GeneticAlgorithm
from visualization import plot_fitness, plot_paths, plot_coverage
from config import CONFIG
import os

def main():
    os.makedirs("outputs", exist_ok=True)
    ga = GeneticAlgorithm(CONFIG)
    best, history = ga.run()
    print("\n=== UAV Genetic Algorithm Results ===")
    print(f"Best fitness: {best.fitness:.3f}")
    print(f"Coverage score: {best.metrics['coverage']:.3f}")
    print(f"Energy cost: {best.metrics['energy']:.3f}")
    print(f"Flight time: {best.metrics['time']:.3f}")
    print(f"Hazard exposure: {best.metrics['risk']:.3f}")
    print(f"Constraint penalty: {best.metrics['penalty']:.3f}")
    print("Best chromosome (waypoints x,y and sensor power):")
    for i, waypoint in enumerate(best.genes):
        print(f"  Point {i+1}: x={waypoint[0]:.2f}, y={waypoint[1]:.2f}, sensor={waypoint[2]:.2f}")
    plot_fitness(history, "outputs/fitness_convergence.png")
    plot_paths(best, CONFIG, "outputs/best_uav_path.png")
    plot_coverage(best, CONFIG, "outputs/coverage_heatmap.png")
    print("\nSaved plots in the outputs/ folder.")

if __name__ == "__main__":
    main()
