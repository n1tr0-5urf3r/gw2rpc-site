from flask import Flask, render_template, jsonify

app = Flask(__name__)

fractal_list = {
    872: "Mistlock Observatory",
    947: "Uncategorized",
    948: "Snowblind",
    949: "Swampland",
    950: "Urban Battleground",
    951: "Aquatic Ruins",
    952: "Cliffside",
    953: "Underground Facility",
    954: "Volcanic",
    955: "Molten Furnace",
    956: "Aetherblade",
    957: "Thaumanova Reactor",
    958: "Solid Ocean",
    959: "Molten Boss",
    960: "Mai Trin",
    1164: "Chaos",
    1177: "Nightmare",
    1205: "Shattered Observatory"
}

valid_ids = {
    "valid": [
        15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34,
        35, 38, 39, 50, 51, 53, 54, 62, 65, 73, 91, 139, 218, 326, 350, 866,
        873, 895, 921, 929, 988, 1015, 1041, 1043, 1045, 1052, 1062, 1149,
        1155, 1156, 1165, 1175, 1178, 1185, 1188, 1195, 1203, 1206, 1210, 1211,
        1226, 1228, 1248, 1263
    ],
    "guild_halls": {
        "Windswept Haven": "gh_haven",
        "Gilded Hollow": "gh_hollow",
        "Lost Precipice": "gh_precipice"
    }
}


@app.route("/api/v1/fractals")
def fractals():
    return jsonify(fractal_list)


@app.route("/api/v1/registry")
def registry():
    return jsonify(valid_ids)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/usage')
def usage():
    return render_template('usage.html')


if __name__ == "__main__":
    app.run('0.0.0.0')
