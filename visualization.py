"""Matplotlib plots for convergence, evolved path, and coverage heatmap."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def plot_fitness(history, output_path):
    plt.figure(figsize=(8, 4.5))
    plt.plot(history["best"], label="Best fitness")
    plt.plot(history["average"], label="Average fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness (higher is better)")
    plt.title("Genetic Algorithm Fitness Convergence")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

def draw_zones(ax, config):
    for x1, y1, x2, y2 in config["no_fly_zones"]:
        ax.add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, fill=True, alpha=0.35,
                                   hatch="///", label="No-fly zone"))
    for hx, hy, radius in config["hazards"]:
        ax.add_patch(plt.Circle((hx, hy), radius, fill=False, linestyle="--",
                                linewidth=1.5, label="Hazard zone"))

def plot_paths(best, config, output_path):
    fig, ax = plt.subplots(figsize=(7, 7))
    draw_zones(ax, config)
    points = [config["start"]] + [(g[0], g[1]) for g in best.genes] + [config["goal"]]
    xs, ys = zip(*points)
    ax.plot(xs, ys, marker="o", linewidth=2, label="Evolved UAV route")
    ax.scatter(*config["start"], marker="s", s=90, label="Start")
    ax.scatter(*config["goal"], marker="*", s=180, label="Goal")
    ax.set_xlim(0, config["grid_size"]-1); ax.set_ylim(0, config["grid_size"]-1)
    ax.set_xlabel("X coordinate"); ax.set_ylabel("Y coordinate")
    ax.set_title("Best Evolved UAV Flight Path")
    ax.grid(True, alpha=0.25); ax.legend(loc="upper left", fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout(); fig.savefig(output_path, dpi=160); plt.close(fig)

def plot_coverage(best, config, output_path):
    size = config["grid_size"]
    xs = np.arange(size); ys = np.arange(size)
    xx, yy = np.meshgrid(xs, ys)
    coverage = np.zeros_like(xx, dtype=float)
    radius = config["coverage_radius"]
    for x, y, power in best.genes:
        dist = np.sqrt((xx-x)**2 + (yy-y)**2)
        coverage += np.where(dist <= radius, power, 0.0)
    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(coverage, origin="lower", extent=[0, size-1, 0, size-1], cmap="YlGnBu")
    fig.colorbar(image, ax=ax, label="Accumulated sensor coverage")
    draw_zones(ax, config)
    ax.set_xlabel("X coordinate"); ax.set_ylabel("Y coordinate")
    ax.set_title("UAV Sensor Coverage Heatmap")
    fig.tight_layout(); fig.savefig(output_path, dpi=160); plt.close(fig)
