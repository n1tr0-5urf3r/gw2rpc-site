from flask import Flask, jsonify, render_template, send_file, abort

app = Flask(__name__)

CLIENT_VERSION = 0.3

version_dict = {"build": CLIENT_VERSION}

registry_dict = {
    "valid": [
        15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34,
        35, 38, 39, 50, 51, 53, 54, 62, 65, 73, 91, 139, 218, 326, 350, 866,
        873, 895, 921, 929, 988, 1015, 1041, 1043, 1045, 1052, 1062, 1149,
        1155, 1156, 1165, 1175, 1178, 1185, 1188, 1195, 1203, 1206, 1210, 1211,
        1226, 1228, 1248, 1263, 1264, 881, 878, 1270, 650, 371, 647, 375, 248
    ],
    "special": {
        "Windswept Haven": "gh_haven",
        "Gilded Hollow": "gh_hollow",
        "Lost Precipice": "gh_precipice",
        "Special Forces Training Area": "1155",
        "Divinity's Reach": "wintersday_dr",
        "Snowball Mayhem": "wintersday_snowball",
        "Winter Wonderland": "wintersday_snowball"
    },
    "fractals": [{
        'id': 872,
        'name': 'Mistlock Observatory'
    }, {
        'id': 947,
        'name': 'Uncategorized'
    }, {
        'id': 948,
        'name': 'Snowblind'
    }, {
        'id': 949,
        'name': 'Swampland'
    }, {
        'id': 950,
        'name': 'Urban Battleground'
    }, {
        'id': 951,
        'name': 'Aquatic Ruins'
    }, {
        'id': 952,
        'name': 'Cliffside'
    }, {
        'id': 953,
        'name': 'Underground Facility'
    }, {
        'id': 954,
        'name': 'Volcanic'
    }, {
        'id': 955,
        'name': 'Molten Furnace'
    }, {
        'id': 956,
        'name': 'Aetherblade'
    }, {
        'id': 957,
        'name': 'Thaumanova Reactor'
    }, {
        'id': 958,
        'name': 'Solid Ocean'
    }, {
        'id': 959,
        'name': 'Molten Boss'
    }, {
        'id': 960,
        'name': 'Mai Trin'
    }, {
        'id': 1164,
        'name': 'Chaos'
    }, {
        'id': 1177,
        'name': 'Nightmare'
    }, {
        'id': 1205,
        'name': 'Shattered Observatory'
    }, {
        "id": 1267,
        "name": "Twilight Oasis"
    }],
    "regions": {
        "Shiverpeak Mountains": "region_shiverpeaks",
        "Ascalon": "region_ascalon",
        "Crystal Desert": "region_desert",
        "Heart of Maguuma": "1045",
        "Ruins of Orr": "region_orr",
        "Maguuma Wastes": "1015",
        "Maguuma Jungle": "54",
        "Wintersday Celebration": "wintersday_dr",
        "World vs. World": "38",
        "Kryta": "24",
        "Ring of Fire": "1175"
    }
}

support_dict = {"support": "https://discord.gg/BFfwjZS"}


@app.route("/api/v1/registry")
def registry():
    return jsonify(registry_dict)


@app.route("/api/v1/build")
def build():
    return jsonify(version_dict)


@app.route("/api/v1/support")
def support():
    return jsonify(support_dict)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/download/latest')
def download_latest():
    path = "downloads/gw2rpc.7z"
    try:
        return send_file(path, as_attachment=True)
    except:
        return abort(400)


if __name__ == "__main__":
    app.run()
