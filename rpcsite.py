from random import choice
import os

from flask import Flask, abort, jsonify, render_template, send_file

app = Flask(__name__)

CLIENT_VERSION = 2.0

RANDOM_IMAGE_POOL = os.listdir("static/img/showcases/")

version_dict = {"build": CLIENT_VERSION}

registry_dict = {
    "valid": [
        15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34,
        35, 38, 39, 50, 51, 53, 54, 62, 65, 73, 91, 139, 218, 326, 350, 866,
        873, 895, 921, 929, 988, 1015, 1041, 1043, 1045, 1052, 1062, 1149,
        1155, 1156, 1165, 1175, 1178, 1185, 1188, 1195, 1203, 1206, 1210, 1211,
        1226, 1228, 1248, 1263, 1264, 881, 878, 1270, 650, 371, 647, 375, 248,
        1271, 935, 895, 934, 1288, 918, 929, 922, 1301, 1303, 1306
    ],
    "special": {
        "Windswept Haven": "gh_haven",
        "Gilded Hollow": "gh_hollow",
        "Lost Precipice": "gh_precipice",
        "Special Forces Training Area": "1155",
        "Snowball Mayhem": "wintersday_snowball",
        "Winter Wonderland": "wintersday_snowball"
    },
    "fractals": [{
        "id": 872,
        "name": "Mistlock Observatory"
    }, {
        "id": 947,
        "name": "Uncategorized"
    }, {
        "id": 948,
        "name": "Snowblind"
    }, {
        "id": 949,
        "name": "Swampland"
    }, {
        "id": 950,
        "name": "Urban Battleground"
    }, {
        "id": 951,
        "name": "Aquatic Ruins"
    }, {
        "id": 952,
        "name": "Cliffside"
    }, {
        "id": 953,
        "name": "Underground Facility"
    }, {
        "id": 954,
        "name": "Volcanic"
    }, {
        "id": 955,
        "name": "Molten Furnace"
    }, {
        "id": 956,
        "name": "Aetherblade"
    }, {
        "id": 957,
        "name": "Thaumanova Reactor"
    }, {
        "id": 958,
        "name": "Solid Ocean"
    }, {
        "id": 959,
        "name": "Molten Boss"
    }, {
        "id": 960,
        "name": "Mai Trin"
    }, {
        "id": 1164,
        "name": "Chaos"
    }, {
        "id": 1177,
        "name": "Nightmare"
    }, {
        "id": 1205,
        "name": "Shattered Observatory"
    }, {
        "id": 1267,
        "name": "Twilight Oasis"
    }, {
        "id": 1290,
        "name": "Deepstone"
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
    },
    "raids": {
        "1062": [{
            "id": "vale_guardian",
            "type": "boss",
            "coord": [3896.16, 13533.7],
            "radius": 66
        }, {
            "id": "spirit_woods",
            "type": "event",
            "coord": [3777.57, 12873.72],
            "radius": 200,
            "height": 95
        }, {
            "id": "spirit_woods",
            "type": "event",
            "coord": [3913.19, 13121.69],
            "radius": 229
        }, {
            "id": "gorseval",
            "type": "boss",
            "coord": [4164.36, 12861.2],
            "radius": 135
        }, {
            "id": "sabetha",
            "type": "boss",
            "coord": [3883.09, 12540.5],
            "radius": 142
        }],
        "1149": [{
            "id": "slothasor",
            "type": "boss",
            "coord": [3529.07, 13061.6],
            "radius": 85
        }, {
            "id": "bandit_trio",
            "type": "boss",
            "coord": [3125.1, 13482.6],
            "radius": 242
        }, {
            "id": "matthias",
            "type": "boss",
            "coord": [2952.57, 12812.4],
            "radius": 60
        }],
        "1156": [{
            "id": "escort",
            "type": "event",
            "coord": [2487.41, 12396.86],
            "radius": 400
        }, {
            "id": "escort",
            "type": "event",
            "coord": [2274.07, 12620.67],
            "radius": 70
        }, {
            "id": "keep_construct",
            "type": "boss",
            "coord": [2272.88, 12921.2],
            "radius": 55
        }, {
            "id": "xera",
            "type": "boss",
            "coord": [2307.28, 13443.8],
            "radius": 120
        }, {
            "id": "twisted_castle",
            "type": "event",
            "coord": [2284.78, 13304.88],
            "radius": 315,
            "height": 400
        }],
        "1188": [{
            "id": "cairn",
            "type": "boss",
            "coord": [13524.2, 4907.92],
            "radius": 58
        }, {
            "id": "mursaat_overseer",
            "type": "boss",
            "coord": [13035.1, 4826.37],
            "radius": 75
        }, {
            "id": "samarog",
            "type": "boss",
            "coord": [12758.9, 4862.04],
            "radius": 91
        }, {
            "id": "deimos",
            "type": "boss",
            "coord": [12574.7, 4863.54],
            "radius": 92
        }],
        "1264": [{
            "id": "soulless_horror",
            "type": "boss",
            "coord": [19525.71, 15960.45],
            "radius": 71
        }, {
            "id": "river_of_souls",
            "type": "event",
            "coord": [20017.4, 16041.15],
            "radius": 160
        }, {
            "id": "river_of_souls",
            "type": "event",
            "coord": [20209.9, 15944.31],
            "radius": 75
        }, {
            "id": "river_of_souls",
            "type": "event",
            "coord": [19747.75, 15962.24],
            "radius": 150
        }, {
            "id": "broken_king",
            "type": "boss",
            "coord": [20166.29, 15649.43],
            "radius": 90
        }, {
            "id": "eater_of_souls",
            "type": "boss",
            "coord": [20093.32, 16318.5],
            "radius": 75
        }, {
            "id": "dhuum",
            "type": "boss",
            "coord": [20624.24, 15966.28],
            "radius": 105
        }, {
            "id": "statue_of_darkness",
            "type": "boss",
            "coord": [20565.93, 15955.36],
            "radius": 160,
            "height": 110
        }],
        "1303": [{
	    "id": "conjured_amalgamate",
	    "type": "boss",
	    "coord": [14199.68, 15899.78],
	    "radius": 90
	}, {
	    "id": "twin_largos",
	    "type": "boss",
	    "coord": [14937.7, 15332.13],
	    "radius": 275
	}, {
	    "id": "qadim",
	    "type": "boss",
	    "coord": [14030, 14857],
	    "radius": 225
	}],
	"1306": [{
	    "id": "freezie",
	    "type": "boss",
	    "coord": [19947.41, 8259.2],
	    "radius": 115
	}]
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
    image_path = "static/img/showcases/" + choice(RANDOM_IMAGE_POOL)
    return render_template('index.html', random_image=image_path)


@app.route('/download/latest')
def download_latest():
    path = "downloads/gw2rpc.7z"
    try:
        return send_file(path, as_attachment=True)
    except:
        return abort(400)


if __name__ == "__main__":
    app.run()
