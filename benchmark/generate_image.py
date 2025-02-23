import csv

import matplotlib.pyplot as plt
import numpy as np


def plot_data(file_name, ax, offset):
    with open(file_name) as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        data = list(reader)

    # Extract the data
    names = [row[0] for row in data]
    time_5k = [float(row[11]) for row in data]  # time 5k at col index 11
    time_50k = [float(row[10]) for row in data]  # time 50k at col index 10
    time_200k = [float(row[9]) for row in data]  # time 200k at col index 9
    cpu_time_5k = [float(row[4]) for row in data]
    cpu_time_50k = [float(row[3]) for row in data]
    cpu_time_200k = [float(row[2]) for row in data]

    # Prepare the data for plotting
    x = np.arange(len(names)) + offset  # label locations
    width = 0.125  # width of bars

    # Plot Time for 5k requests
    rects = ax.bar(x, time_5k, width, label="Time 5k")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    # Plot Time for 50k requests
    rects = ax.bar(x + width, time_50k, width, label="Time 50k")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    # Plot Time for 200k requests
    rects = ax.bar(x + 2 * width, time_200k, width, label="Time 200k")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    # Plot CPU time for 5k requests
    rects = ax.bar(x + 3 * width, cpu_time_5k, width, label="CPU Time 5k")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    # Plot CPU time for 50k requests
    rects = ax.bar(x + 4 * width, cpu_time_50k, width, label="CPU Time 50k")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    # Plot CPU time for 200k requests
    rects = ax.bar(x + 5 * width, cpu_time_200k, width, label="CPU Time 200k")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    return x, width, names


def plot_json_data(file_name, ax, offset, gzip):
    with open(file_name) as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)

    names = [row[0] for row in data]
    # Based on the updated CSV the columns are as follows:
    # 12: time json/10?gzip=false, 13: time json/10?gzip=true,
    # 14: time json/1?gzip=false,   15: time json/1?gzip=true
    if not gzip:
        time_json_10 = [float(row[12]) for row in data]
        time_json_1 = [float(row[14]) for row in data]
        title_suffix = "gzip false"
    else:
        time_json_10 = [float(row[13]) for row in data]
        time_json_1 = [float(row[15]) for row in data]
        title_suffix = "gzip true"

    x = np.arange(len(names)) + offset
    width = 0.25  # slightly wider bars for only two groups

    rects = ax.bar(x, time_json_10, width, label="JSON vector [1,1024]")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    rects = ax.bar(x + width, time_json_1, width, label="JSON vector [10,1024]")
    ax.bar_label(rects, padding=3, fontsize=7, rotation=90)

    ax.set_xticks(x + width)
    ax.set_xticklabels(names)
    ax.legend(loc="upper left", ncols=2, prop={"size": 8})
    ax.tick_params(axis="x", labelsize=8)
    ax.set_ylabel("Time (s)")
    ax.set_title(
        f"Benchmark get(url).json() | Session=Async | {title_suffix} | Requests: 400 | Size: ~20kb, ~200kb, ~2mb"
    )

    return x, width, names


# Create a figure with five subplots:
# The first three plot .text and CPU times,
# And the last two plot JSON response times (one for gzip false and one for gzip true).
fig, axes = plt.subplots(5, 1, figsize=(10, 14), layout="constrained")
ax1, ax2, ax3, ax_json_false, ax_json_true = axes

x1, width, names = plot_data("session=False.csv", ax1, 0)
x2, _, _ = plot_data("session=True.csv", ax2, 0)
x3, _, x3names = plot_data("session='Async'.csv", ax3, 0)

# Adjust y-axis limits for first subplot
y_min, y_max = ax1.get_ylim()
ax1.set_ylim(y_min, y_max + 7)
ax1.set_ylabel("Time (s)")
ax1.set_title("Benchmark get(url).text | Session=False | Requests: 400 | Response: gzip, utf-8, size 5Kb,50Kb,200Kb")
ax1.set_xticks(x1 + 3 * width - width / 2)
ax1.set_xticklabels(names)
ax1.legend(loc="upper left", ncols=6, prop={"size": 8})
ax1.tick_params(axis="x", labelsize=8)

# Adjust second subplot
y_min, y_max = ax2.get_ylim()
ax2.set_ylim(y_min, y_max + 2)
ax2.set_ylabel("Time (s)")
ax2.set_title("Benchmark get(url).text | Session=True | Requests: 400 | Response: gzip, utf-8, size 5Kb,50Kb,200Kb")
ax2.set_xticks(x2 + 3 * width - width / 2)
ax2.set_xticklabels(names)
ax2.legend(loc="upper left", ncols=6, prop={"size": 8})
ax2.tick_params(axis="x", labelsize=8)

# Adjust third subplot (Async)
y_min, y_max = ax3.get_ylim()
ax3.set_ylim(y_min, y_max + 2)
ax3.set_ylabel("Time (s)")
ax3.set_title("Benchmark get(url).text | Session=Async | Requests: 400 | Response: gzip, utf-8, size 5Kb,50Kb,200Kb")
ax3.set_xticks(x3 + 3 * width - width / 2)
ax3.set_xticklabels(x3names)
ax3.legend(loc="upper left", ncols=6, prop={"size": 8})
ax3.tick_params(axis="x", labelsize=8)

# Plot JSON response times on the last two axes using session=False.csv
plot_json_data("session='Async'.csv", ax_json_false, 0, gzip=False)
plot_json_data("session='Async'.csv", ax_json_true, 0, gzip=True)

# Save the complete figure to a file
plt.savefig("benchmark.jpg", format="jpg", dpi=80, bbox_inches="tight")
