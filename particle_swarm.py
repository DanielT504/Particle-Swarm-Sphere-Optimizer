import random
import matplotlib.pyplot as plt

# Constants
NUM_PARTICLES = 200
NUM_DIMENSIONS = 4
MAX_ITERATIONS = 200
C1 = 2.0  # Cognitive parameter
C2 = 2.0  # Social parameter
W = 0.7   # Inertia weight

# Function to optimize (example: sphere function)
def fitness_function(position):
    return sum([x**2 for x in position])

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
particles_scatter = ax.scatter([particle.position[0] for particle in particles],
                              [particle.position[1] for particle in particles],
                              color='b', marker='o')

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
    plt.pause(0.05)

    iteration += 1

# Print the global best position and fitness value
print("Global Best Position:", global_best_position)
print("Global Best Fitness:", fitness_function(global_best_position))

# Show the final plot
plt.show()
