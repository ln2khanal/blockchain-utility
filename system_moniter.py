import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import json
import subprocess
from collections import deque
from datetime import datetime
import sys
import threading

# File path for the log file
file_path = "system_monitor.jsontxt"

# Data storage with a fixed max length
max_points = 100  # Adjust as needed
timestamps = deque(maxlen=max_points)
data_variables = {
    "cpu_percent": deque(maxlen=max_points),
    "memory_percent": deque(maxlen=max_points),
    "rss_memory_mb": deque(maxlen=max_points),
    "virtual_memory_mb": deque(maxlen=max_points),
}

# Get user-specified variables from command-line arguments
selected_variables = sys.argv[
    1:
]  # Example usage: python script.py cpu_percent memory_percent
if not selected_variables:
    print("Usage: python script.py [variable1] [variable2] ...")
    print(f"Available variables: {', '.join(data_variables.keys())}")
    sys.exit(1)

# Validate user input
for var in selected_variables:
    if var not in data_variables:
        print(
            f"Invalid variable: {var}. Available options: {', '.join(data_variables.keys())}"
        )
        sys.exit(1)


# Function to read new data using `tail -F`
def read_new_data():
    try:
        process = subprocess.Popen(
            ["tail", "-F", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        for line in iter(process.stdout.readline, ""):
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            try:
                entry = json.loads(line)
                timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")

                timestamps.append(timestamp)
                for var in selected_variables:
                    data_variables[var].append(entry[var])

            except json.JSONDecodeError as err:
                print(f"Skipping malformed line: {line}, {err}")

    except Exception as e:
        print(f"Error reading file: {e}")


# Start reading new data in the background
threading.Thread(target=read_new_data, daemon=True).start()

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 6))
lines = {}

# Dynamically create plots for selected variables
for var in selected_variables:
    color = {
        "cpu_percent": "blue",
        "memory_percent": "green",
        "rss_memory_mb": "red",
        "virtual_memory_mb": "orange",
    }.get(
        var, "black"
    )  # Default to black if variable isn't recognized

    (lines[var],) = ax.plot(
        [], [], label=var.replace("_", " ").title(), color=color, marker="o"
    )

# Format the x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.xticks(rotation=45)
plt.xlabel("Timestamp")
plt.ylabel("Values")
plt.title("System Resource Usage Over Time")
plt.legend()


# Efficient update function
def update_plot(frame):
    if not timestamps:
        return list(lines.values())  # No data yet

    for var in selected_variables:
        lines[var].set_data(timestamps, data_variables[var])

    ax.relim()
    ax.autoscale_view()

    return list(lines.values())


# Continuous animation
ani = animation.FuncAnimation(fig, update_plot, interval=1000)

plt.tight_layout()
plt.show()
