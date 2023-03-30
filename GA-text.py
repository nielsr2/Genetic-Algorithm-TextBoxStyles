from flask import Flask, render_template, request, jsonify
import random
import json

from functions import *

app = Flask(__name__)


# Parameters

fonts = ["Roboto", "Lato", "Oswald", "Open Sans", "Raleway", "Montserrat"]
colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
highlight_colors = ["#FFD700", "#ADFF2F", "#F08080", "#ADD8E6", "#FFA07A"]
animations = [
    "bounce",
    "flash",
    "pulse",
    "rubberBand",
    # "shake",
    "headShake",
    "swing",
    "tada",
    "wobble",
    "jello",
    "heartBeat",
]



# generate a random individual - based on parameters^^
def generate_random_individual():
    font = random.choice(fonts)
    size = random.randint(10, 24)
    italics = random.choice([True, False])
    opacity = round(random.uniform(0.5, 1), 2)
    letterSpacing = random.randint(-2, 4)
    animation = random.choice(animations)

    # Generate a WCAG compliant color and highlight combination
    while True:
        color = random_color()
        highlight = random_color()
        print(is_wcag_compliant(color, highlight))
        if is_wcag_compliant(color, highlight):
            break

    return {
        "font": font,
        "size": size,
        "color": color,
        "highlight": highlight,
        "italics": italics,
        "opacity": opacity,
        "letterSpacing": letterSpacing,
        "animation": animation,
    }

#
def crossover(parent1, parent2):
    child = {}
    for key in parent1:
        child[key] = random.choice([parent1[key], parent2[key]])
    return child


# for each gene, there is a chance to mutate - all have the same mutation rate, but different genes chance to mutate
def mutate(individual, mutation_rate):
    old = individual.copy()
    if random.random() < mutation_rate:
        # print("Mutating gene: font", mutation_rate)
        individual["font"] = random.choice(fonts)

    if random.random() < mutation_rate:
        # print("Mutating gene: size", mutation_rate)
        individual["size"] = random.randint(10, 24)

    if random.random() < mutation_rate:
        # print("Mutating gene: color and highlight", mutation_rate)
        # Generate a WCAG compliant color and highlight combination
        while True:
            new_color = random_color()
            new_highlight = random_color()
            if is_wcag_compliant(new_color, new_highlight):
                individual["color"] = new_color
                individual["highlight"] = new_highlight
                break

    if random.random() < mutation_rate:
        # print("Mutating gene: opacity", mutation_rate)
        individual["opacity"] = round(random.uniform(0.5, 1), 2)

    if random.random() < mutation_rate:
        # print("Mutating gene: italics", mutation_rate)
        individual["italics"] = random.choice([True, False])

    if random.random() < mutation_rate:
        # print("Mutating gene: letterSpacing",   mutation_rate)
        individual["letterSpacing"] = random.randint(-2, 4)

    if random.random() < mutation_rate:
        # print("Mutating gene: animation", mutation_rate)
        individual["animation"] = random.choice(animations)
    # print("Old:", old, "New:", individual)
    jprint(dict_diff(old, individual))
    return individual


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["GET"])
def generate_population():
    population = [generate_random_individual() for _ in range(10)]
    return jsonify(population)

@app.route("/evolve", methods=["POST"])
def evolve():
    data = json.loads(request.data)
    selected_parents = data["population"]
    mutation_rate = data["minMutationRate"]
    new_population = []
    num_children = 10
    toggle_crossover = data['toggleCrossover']

    for _ in range(num_children):
        parent1 = selected_parents[0]
        parent2 = selected_parents[1]
        
        if toggle_crossover:
            child = crossover(parent1, parent2)
        else:
            child = random.choice([parent1, parent2]).copy()
        
        mutated_child = mutate(child, mutation_rate)
        new_population.append(mutated_child)

    return jsonify(new_population)


if __name__ == "__main__":
    app.run(debug=True)
