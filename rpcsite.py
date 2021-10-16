from random import choice
import os

from flask import Flask, abort, jsonify, render_template, send_file

app = Flask(__name__)

CLIENT_VERSION = 2.11

RANDOM_IMAGE_POOL = os.listdir("static/img/showcases/")

version_dict = {"build": CLIENT_VERSION}

registry_dict = {
    "valid": [
        15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34,
        35, 38, 39, 50, 51, 53, 54, 62, 65, 73, 91, 139, 218, 326, 350, 866,
        873, 895, 921, 929, 988, 1015, 1041, 1043, 1045, 1052, 1062, 1149,
        1155, 1156, 1165, 1175, 1178, 1185, 1188, 1195, 1203, 1206, 1210, 1211,
        1226, 1228, 1248, 1263, 1264, 881, 878, 1270, 650, 371, 647, 375, 248,
        1271, 935, 895, 934, 1288, 918, 929, 922, 1301, 1303, 1306, 1323, 1331,
        1332, 1339, 1340, 1341, 1344, 1346, 1351
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
        "id": 1206,
        "name": "Mistlock Sanctuary"
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
        }],
        "1323": [{
            "id": "cardinal_sabir",
            "type": "boss",
            "coord": [33903.69, 34940.87],
            "radius": 180
        }, {
            "id": "cardinal_adina",
            "type": "boss",
            "coord": [35047.23, 35135.78],
            "radius": 60
        }, {
            "id": "qadim_the_peerless",
            "type": "boss",
            "coord": [34494.02, 34654.03],
            "radius": 115
        }],
        "1331": [{
            "id": "legendary_icebrood_construct",
            "type": "boss",
            "coord": [26878.71, 2804.46],
            "radius": 85
        }],
        "1332": [{
            "id": "legendary_icebrood_construct",
            "type": "boss",
            "coord": [26878.71, 2804.46],
            "radius": 85
        }],
        "1339": [{
            "id": "boneskinner",
            "type": "boss",
            "coord": [24481.37, 1625.59],
            "radius": 65
        }],
        "1340": [{
            "id": "voice_and_claw_of_the_fallen",
            "type": "boss",
            "coord": [24484.52, 1626.85],
            "radius": 65
        }],
        "1341": [{
            "id": "fraenir_of_jormag",
            "type": "boss",
            "coord": [24482.74, 1625.22],
            "radius": 65
        }],
        "1344": [{
            "id": "fraenir_of_jormag",
            "type": "boss",
            "coord": [24482.74, 1625.22],
            "radius": 65
        }],
        "1346": [{
            "id": "voice_and_claw_of_the_fallen",
            "type": "boss",
            "coord": [24484.52, 1626.85],
            "radius": 65
        }],
        "1351": [{
            "id": "boneskinner",
            "type": "boss",
            "coord": [24481.37, 1625.59],
            "radius": 65
        }]
    }
}

registry_dict_v2 = {
    "fractals": [
        {
            "id": 872,
            "name": "Mistlock Observatory"
        },
        {
            "id": 947,
            "name": "Uncategorized"
        },
        {
            "id": 948,
            "name": "Snowblind"
        },
        {
            "id": 949,
            "name": "Swampland"
        },
        {
            "id": 950,
            "name": "Urban Battleground"
        },
        {
            "id": 951,
            "name": "Aquatic Ruins"
        },
        {
            "id": 952,
            "name": "Cliffside"
        },
        {
            "id": 953,
            "name": "Underground Facility"
        },
        {
            "id": 954,
            "name": "Volcanic"
        },
        {
            "id": 955,
            "name": "Molten Furnace"
        },
        {
            "id": 956,
            "name": "Aetherblade"
        },
        {
            "id": 957,
            "name": "Thaumanova Reactor"
        },
        {
            "id": 958,
            "name": "Solid Ocean"
        },
        {
            "id": 959,
            "name": "Molten Boss"
        },
        {
            "id": 960,
            "name": "Mai Trin"
        },
        {
            "id": 1164,
            "name": "Chaos"
        },
        {
            "id": 1177,
            "name": "Nightmare",
            "bosses": [
                {
                    "name": "M.A.M.A.",
                    "coord": [
                        3921.28,
                        6105.77
                    ],
                    "radius": 2105
                },
                {
                    "name": "Siax",
                    "coord": [
                        1672.48,
                        -3042.64
                    ],
                    "radius": 1170
                },
                {
                    "name": "Ensolyss",
                    "coord": [
                        1619.11,
                        1461.35
                    ],
                    "radius": 1096
                }
            ]
        },
        {
            "id": 1205,
            "name": "Shattered Observatory",
            "bosses": [
                {
                    "name": "Skorvald",
                    "coord": [
                        -19562.9,
                        17709.66
                    ],
                    "radius": 2648
                },
                {
                    "name": "Artsariiv",
                    "coord": [
                        10393.96,
                        1461.08
                    ],
                    "radius": 1814
                },
                {
                    "name": "Arkk",
                    "coord": [
                        -17930.50,
                        -16916.88
                    ],
                    "radius": 1878
                }
            ]
        },
        {
        "id": 1206,
        "name": "Mistlock Sanctuary"
        },
        {
            "id": 1267,
            "name": "Twilight Oasis"
        },
        {
            "id": 1290,
            "name": "Deepstone"
        },
        {
            "id": 1384,
            "name": "Sunqua Peak",
            "bosses": [
                {
                    "name": "Ai",
                    "coord": [
                        6921.29,
                        1398.67
                    ],
                    "radius": 1434
                }
            ]
        },
        {
            "id": 1309,
            "name": "Siren's Reef"
        }
    ],
    "raids": {
        "1062": [
            {
                "coord": [
                    3896.16,
                    13533.7
                ],
                "id": "vale_guardian",
                "radius": 66,
                "type": "boss"
            },
            {
                "coord": [
                    3777.57,
                    12873.72
                ],
                "height": 95,
                "id": "spirit_woods",
                "radius": 200,
                "type": "event"
            },
            {
                "coord": [
                    3913.19,
                    13121.69
                ],
                "id": "spirit_woods",
                "radius": 229,
                "type": "event"
            },
            {
                "coord": [
                    4164.36,
                    12861.2
                ],
                "id": "gorseval",
                "radius": 135,
                "type": "boss"
            },
            {
                "coord": [
                    3883.09,
                    12540.5
                ],
                "id": "sabetha",
                "radius": 142,
                "type": "boss"
            }
        ],
        "1149": [
            {
                "coord": [
                    3529.07,
                    13061.6
                ],
                "id": "slothasor",
                "radius": 85,
                "type": "boss"
            },
            {
                "coord": [
                    3125.1,
                    13482.6
                ],
                "id": "bandit_trio",
                "radius": 242,
                "type": "boss"
            },
            {
                "coord": [
                    2952.57,
                    12812.4
                ],
                "id": "matthias",
                "radius": 60,
                "type": "boss"
            }
        ],
        "1156": [
            {
                "coord": [
                    2487.41,
                    12396.86
                ],
                "id": "escort",
                "radius": 400,
                "type": "event"
            },
            {
                "coord": [
                    2274.07,
                    12620.67
                ],
                "id": "escort",
                "radius": 70,
                "type": "event"
            },
            {
                "coord": [
                    2272.88,
                    12921.2
                ],
                "id": "keep_construct",
                "radius": 55,
                "type": "boss"
            },
            {
                "coord": [
                    2307.28,
                    13443.8
                ],
                "id": "xera",
                "radius": 120,
                "type": "boss"
            },
            {
                "coord": [
                    2284.78,
                    13304.88
                ],
                "height": 400,
                "id": "twisted_castle",
                "radius": 315,
                "type": "event"
            }
        ],
        "1188": [
            {
                "coord": [
                    13524.2,
                    4907.92
                ],
                "id": "cairn",
                "radius": 58,
                "type": "boss"
            },
            {
                "coord": [
                    13035.1,
                    4826.37
                ],
                "id": "mursaat_overseer",
                "radius": 75,
                "type": "boss"
            },
            {
                "coord": [
                    12758.9,
                    4862.04
                ],
                "id": "samarog",
                "radius": 91,
                "type": "boss"
            },
            {
                "coord": [
                    12574.7,
                    4863.54
                ],
                "id": "deimos",
                "radius": 92,
                "type": "boss"
            }
        ],
        "1264": [
            {
                "coord": [
                    19525.71,
                    15960.45
                ],
                "id": "soulless_horror",
                "radius": 71,
                "type": "boss"
            },
            {
                "coord": [
                    20017.4,
                    16041.15
                ],
                "id": "river_of_souls",
                "radius": 160,
                "type": "event"
            },
            {
                "coord": [
                    20209.9,
                    15944.31
                ],
                "id": "river_of_souls",
                "radius": 75,
                "type": "event"
            },
            {
                "coord": [
                    19747.75,
                    15962.24
                ],
                "id": "river_of_souls",
                "radius": 150,
                "type": "event"
            },
            {
                "coord": [
                    20166.29,
                    15649.43
                ],
                "id": "broken_king",
                "radius": 90,
                "type": "boss"
            },
            {
                "coord": [
                    20093.32,
                    16318.5
                ],
                "id": "eater_of_souls",
                "radius": 75,
                "type": "boss"
            },
            {
                "coord": [
                    20624.24,
                    15966.28
                ],
                "id": "dhuum",
                "radius": 105,
                "type": "boss"
            },
            {
                "coord": [
                    20565.93,
                    15955.36
                ],
                "height": 110,
                "id": "statue_of_darkness",
                "radius": 160,
                "type": "boss"
            }
        ],
        "1303": [
            {
                "coord": [
                    14199.68,
                    15899.78
                ],
                "id": "conjured_amalgamate",
                "radius": 90,
                "type": "boss"
            },
            {
                "coord": [
                    14937.7,
                    15332.13
                ],
                "id": "twin_largos",
                "radius": 275,
                "type": "boss"
            },
            {
                "coord": [
                    14030,
                    14857
                ],
                "id": "qadim",
                "radius": 225,
                "type": "boss"
            }
        ],
        "1306": [
            {
                "coord": [
                    19947.41,
                    8259.2
                ],
                "id": "freezie",
                "radius": 115,
                "type": "boss"
            }
        ],
        "1323": [
            {
                "coord": [
                    33903.69,
                    34940.87
                ],
                "id": "cardinal_sabir",
                "radius": 180,
                "type": "boss"
            },
            {
                "coord": [
                    35047.23,
                    35135.78
                ],
                "id": "cardinal_adina",
                "radius": 60,
                "type": "boss"
            },
            {
                "coord": [
                    34494.02,
                    34654.03
                ],
                "id": "qadim_the_peerless",
                "radius": 115,
                "type": "boss"
            }
        ],
        "1331": [
            {
                "coord": [
                    26878.71,
                    2804.46
                ],
                "id": "legendary_icebrood_construct",
                "radius": 85,
                "type": "boss"
            }
        ],
        "1332": [
            {
                "coord": [
                    26878.71,
                    2804.46
                ],
                "id": "legendary_icebrood_construct",
                "radius": 85,
                "type": "boss"
            }
        ],
        "1339": [
            {
                "coord": [
                    24481.37,
                    1625.59
                ],
                "id": "boneskinner",
                "radius": 65,
                "type": "boss"
            }
        ],
        "1340": [
            {
                "coord": [
                    24484.52,
                    1626.85
                ],
                "id": "voice_and_claw_of_the_fallen",
                "radius": 65,
                "type": "boss"
            }
        ],
        "1341": [
            {
                "coord": [
                    24482.74,
                    1625.22
                ],
                "id": "fraenir_of_jormag",
                "radius": 65,
                "type": "boss"
            }
        ],
        "1344": [
            {
                "coord": [
                    24482.74,
                    1625.22
                ],
                "id": "fraenir_of_jormag",
                "radius": 65,
                "type": "boss"
            }
        ],
        "1346": [
            {
                "coord": [
                    24484.52,
                    1626.85
                ],
                "id": "voice_and_claw_of_the_fallen",
                "radius": 65,
                "type": "boss"
            }
        ],
        "1351": [
            {
                "coord": [
                    24481.37,
                    1625.59
                ],
                "id": "boneskinner",
                "radius": 65,
                "type": "boss"
            }
        ]
    },
    "regions": {
        "2": "region_ascalon",
        "12": "region_desert",
        "10": "1045",
        "4": "24",
        "5": "54",
        "11 ": "1015",
        "20": "1175",
        "3": "region_orr",
        "1": "region_shiverpeaks",
        "27": "wintersday_dr",
        "7": "38"
    },
    "special": {
        "1068": "gh_hollow",
        "1101": "gh_hollow",
        "1107": "gh_hollow",
        "1108": "gh_hollow",
        "1121": "gh_hollow",
        "1069": "gh_precipice",
        "1076": "gh_precipice",
        "1071": "gh_precipice",
        "1104": "gh_precipice",
        "1124": "gh_precipice",
        "882": "wintersday_snowball",
        "877": "wintersday_snowball",
        "1155": "1155",
        "1214": "gh_haven",
        "1215": "gh_haven",
        "1232": "gh_haven",
        "1224": "gh_haven",
        "1243": "gh_haven",
        "1250": "gh_haven"
    },
    "valid": [
        15,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        34,
        35,
        38,
        39,
        50,
        51,
        53,
        54,
        62,
        65,
        73,
        91,
        139,
        218,
        326,
        350,
        866,
        873,
        895,
        921,
        929,
        988,
        1015,
        1041,
        1043,
        1045,
        1052,
        1062,
        1149,
        1155,
        1156,
        1165,
        1175,
        1178,
        1185,
        1188,
        1195,
        1203,
        1206,
        1210,
        1211,
        1226,
        1228,
        1248,
        1263,
        1264,
        881,
        878,
        1270,
        650,
        371,
        647,
        375,
        248,
        1271,
        935,
        895,
        934,
        1288,
        918,
        929,
        922,
        1301,
        1303,
        1306,
        1323,
        1331,
        1332,
        1339,
        1340,
        1341,
        1344,
        1346,
        1351
    ]
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

@app.route("/api/v2/registry")
def registry_v2():
    return jsonify(registry_dict_v2)

@app.route("/api/v2/build")
def build_v2():
    return jsonify(version_dict)


@app.route("/api/v2/support")
def support_v2():
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
