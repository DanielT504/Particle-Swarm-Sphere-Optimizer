import random
import matplotlib.pyplot as plt
import numpy as np

# Constants
NUM_PARTICLES = 200
NUM_DIMENSIONS = 2
MAX_ITERATIONS = 50
C1 = 2.0  # Cognitive parameter
C2 = 2.0  # Social parameter
W = 0.7   # Inertia weight

# Function to optimize (example: sphere function)
def fitness_function(position):
    x = position[0]
    y = position[1]
    return x**2 + y**2

class Particle:
    def __init__(self):
        self.position = [random.uniform(-5, 5) for _ in range(NUM_DIMENSIONS)]
        self.velocity = [random.uniform(-1, 1) for _ in range(NUM_DIMENSIONS)]
        self.best_position = self.position.copy()

    def update_velocity(self, global_best_position):
        for i in range(NUM_DIMENSIONS):
            r1 = random.random()
            r2 = random.random()
            cognitive_velocity = C1 * r1 * (self.best_position[i] - self.position[i])
            social_velocity = C2 * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] = W * self.velocity[i] + cognitive_velocity + social_velocity

    def update_position(self):
        for i in range(NUM_DIMENSIONS):
            self.position[i] += self.velocity[i]

    def update_best_position(self):
        if fitness_function(self.position) < fitness_function(self.best_position):
            self.best_position = self.position.copy()

# Initialize particles
particles = [Particle() for _ in range(NUM_PARTICLES)]

# Find global best position
global_best_position = particles[0].position.copy()
for particle in particles:
    if fitness_function(particle.position) < fitness_function(global_best_position):
        global_best_position = particle.position.copy()

# Plot initialization
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Generate a grid of points to evaluate the fitness function
x_vals = np.linspace(-6, 6, 100)
y_vals = np.linspace(-6, 6, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = fitness_function([X, Y])

# Create a color map to represent the fitness values
cmap = plt.cm.get_cmap('jet')
norm = plt.Normalize(vmin=np.min(Z), vmax=np.max(Z))

# Plot the fitness landscape
ax.imshow(Z, extent=(-6, 6, -6, 6), origin='lower', cmap=cmap, norm=norm)

# Initialize the particles on the plot
particles_scatter = ax.scatter([particle.position[0] for particle in particles],
                              [particle.position[1] for particle in particles],
                              color='white', marker='o', s=10)

# PSO main loop
iteration = 0
while iteration < MAX_ITERATIONS:
    for particle in particles:
        particle.update_velocity(global_best_position)
        particle.update_position()
        particle.update_best_position()

        # Update global best position
        if fitness_function(particle.position) < fitness_function(global_best_position):
            global_best_position = particle.position.copy()

    # Update particle positions on the plot
    particles_scatter.set_offsets([[particle.position[0], particle.position[1]] for particle in particles])
    plt.pause(0.2)

    iteration += 1

# Print the global best position and fitness value
print("Global Best Position:", global_best_position)
print("Global Best Fitness:", fitness_function(global_best_position))

# Show the final plot
plt.show()