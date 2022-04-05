from random import choice
import os
import hashlib
from functools import partial

from flask import Flask, abort, jsonify, render_template, send_file, request

app = Flask(__name__)

CLIENT_VERSION = 2.35

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
            "id": "gate",
            "type": "event",
            "coord": [67264, 51980],
            "radius": 206
        }, {
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
            "name": "Snowblind",
            "bosses": [
                {
                    "name": "Elemental Source",
                    "coord": [
                        -3447,
                        -4795
                    ],
                    "radius": 2490
                },
                {
                    "name": "Lornarr Dragonseeker",
                    "coord": [
                        7166,
                        -2435
                    ],
                    "radius": 1034
                }
            ]
        },
        {
            "id": 949,
            "name": "Swampland",
            "bosses": [
                {
                    "name": "Bloomhunger",
                    "coord": [
                        -4622,
                        -5250
                    ],
                    "radius": 2445
                }
            ]
        },
        {
            "id": 950,
            "name": "Urban Battleground",
            "bosses": [
                {
                    "name": "Captain Ashym",
                    "coord": [
                        7229,
                        31804
                    ],
                    "radius": 888
                }
            ]
        },
        {
            "id": 951,
            "name": "Aquatic Ruins",
            "bosses": [
                {
                    "name": "Jellyfish Beast",
                    "coord": [
                        -3041,
                        -788
                    ],
                    "radius": 1769
                }
            ]
        },
        {
            "id": 952,
            "name": "Cliffside",
            "bosses": [
                {
                    "name": "Archdiviner",
                    "coord": [
                        4960,
                        -400
                    ],
                    "radius": 938
                }
            ]
        },
        {
            "id": 953,
            "name": "Underground Facility",
            "bosses": [
                {
                    "name": "Rabsovich",
                    "coord": [
                        25545,
                        4908
                    ],
                    "radius": 1000
                },
                {
                    "name": "Rampaging Ice Elemental or Dredge Powersuit",
                    "coord": [
                        32588,
                        7262
                    ],
                    "radius": 12720
                }
            ]
        },
        {
            "id": 954,
            "name": "Volcanic",
            "bosses": [
                {
                    "name": "Grawl Shaman",
                    "coord": [
                        7756,
                        -27275
                    ],
                    "radius": 1475
                },
                {
                    "name": "Imbued Shaman",
                    "coord": [
                        9919,
                        -31756
                    ],
                    "radius": 1491
                }
            ]
        },
        {
            "id": 955,
            "name": "Molten Furnace",
            "bosses": [
                {
                    "name": "in Weapon Testing Facility",
                    "coord": [
                        -9176,
                        790
                    ],
                    "radius": 1453
                }
            ]
        },
        {
            "id": 956,
            "name": "Aetherblade",
            "bosses": [
                {
                    "name": "Frizz",
                    "coord": [
                        -3198,
                        6580
                    ],
                    "radius": 830
                }
            ]
        },
        {
            "id": 957,
            "name": "Thaumanova Reactor",
            "bosses": [
                {
                    "name": "Subject 6",
                    "coord": [
                        4569,
                        5542
                    ],
                    "radius": 1349
                },
                {
                    "name": "Thaumanova Anomaly",
                    "coord": [
                        21,
                        -18
                    ],
                    "radius": 737
                }
            ]
        },
        {
            "id": 958,
            "name": "Solid Ocean",
            "bosses": [
                {
                    "name": "Jade Maw",
                    "coord": [
                        30124,
                        31762
                    ],
                    "radius": 1969
                }
            ]
        },
        {
            "id": 959,
            "name": "Molten Boss",
            "bosses": [
                {
                    "name": "Berserker and Firestorm",
                    "coord": [
                        5493.12,
                        -4471.18
                    ],
                    "radius": 1266
                }
            ]
        },
        {
            "id": 960,
            "name": "Mai Trin fractal",
            "bosses": [
                {
                    "name": "Captain Mai Trin",
                    "coord": [
                        -1152,
                        -2649
                    ],
                    "radius": 1082
                }
            ]
        },
        {
            "id": 1164,
            "name": "Chaos",
            "bosses": [
                {
                    "name": "Anomaly",
                    "coord": [
                        221,
                        -5790
                    ],
                    "radius": 1547
                },
                {
                    "name": "Brazen Gladiator",
                    "coord": [
                        2429,
                        4504
                    ],
                    "radius": 1270
                }
            ]
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
            "name": "Twilight Oasis",
            "bosses": [
                {
                    "name": "Amala",
                    "coord": [
                        7639,
                        -1252
                    ],
                    "radius": 1400
                },
                {
                    "name": "a sandbinder",
                    "coord": [
                       815,
                       1322
                    ],
                    "radius": 655
                },
                {
                    "name": "a sandbinder",
                    "coord": [
                       5808,
                       3626
                    ],
                    "radius": 500
                },
                {
                    "name": "a sandbinder",
                    "coord": [
                       1009,
                       2501
                    ],
                    "radius": 500
                }
            ]
        },
        {
            "id": 1290,
            "name": "Deepstone",
            "bosses": [
                {
                    "name": "Brood Queen",
                    "coord": [
                        8534,
                        -4505
                    ],
                    "radius": 1031
                },
                {
                    "name": "Deepstone Sentinel",
                    "coord": [
                        -2634,
                        168
                    ],
                    "radius": 1014
                },
                {
                    "name": "The Voice",
                    "coord": [
                        700,
                        12184
                    ],
                    "radius": 2588
                }
            ]
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
            "name": "Siren's Reef",
            "bosses": [
                {
                    "name": "Blasting Black Peter",
                    "coord": [
                        4136.4,
                        12539.9
                    ],
                    "radius": 1726
                },
                {
                    "name": "Arabella Crowe",
                    "coord": [
                        -6757.73,
                        3787.74
                    ],
                    "radius": 4437
                }
            ]
        }
    ],
    "raids": {
        "1062": [
            {
            "coord": [
                36664.16,
                29917.7
            ],
            "id": "vale_guardian",
            "radius": 66,
            "type": "boss"
            },
            {
            "coord": [
                36545.57,
                29257.72
            ],
            "height": 95,
            "id": "spirit_woods",
            "radius": 200,
            "type": "event"
            },
            {
            "coord": [
                36681.19,
                29505.690000000002
            ],
            "id": "spirit_woods",
            "radius": 229,
            "type": "event"
            },
            {
            "coord": [
                36932.36,
                29245.2
            ],
            "id": "gorseval",
            "radius": 135,
            "type": "boss"
            },
            {
            "coord": [
                36651.09,
                28924.5
            ],
            "id": "sabetha",
            "radius": 142,
            "type": "boss"
            }
        ],
        "1149": [
            {
            "coord": [
                36297.07,
                29445.6
            ],
            "id": "slothasor",
            "radius": 85,
            "type": "boss"
            },
            {
            "coord": [
                35893.1,
                29866.6
            ],
            "id": "bandit_trio",
            "radius": 242,
            "type": "boss"
            },
            {
            "coord": [
                35720.57,
                29196.4
            ],
            "id": "matthias",
            "radius": 60,
            "type": "boss"
            }
        ],
        "1156": [
            {
            "coord": [
                35255.41,
                28780.86
            ],
            "id": "escort",
            "radius": 400,
            "type": "event"
            },
            {
            "coord": [
                35042.07,
                29004.67
            ],
            "id": "escort",
            "radius": 70,
            "type": "event"
            },
            {
            "coord": [
                35040.88,
                29305.2
            ],
            "id": "keep_construct",
            "radius": 55,
            "type": "boss"
            },
            {
            "coord": [
                35075.28,
                29827.8
            ],
            "id": "xera",
            "radius": 120,
            "type": "boss"
            },
            {
            "coord": [
                35052.78,
                29688.879999999997
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
                46292.2,
                21291.92
            ],
            "id": "cairn",
            "radius": 58,
            "type": "boss"
            },
            {
            "coord": [
                45803.1,
                21210.37
            ],
            "id": "mursaat_overseer",
            "radius": 75,
            "type": "boss"
            },
            {
            "coord": [
                45526.9,
                21246.04
            ],
            "id": "samarog",
            "radius": 91,
            "type": "boss"
            },
            {
            "coord": [
                45342.7,
                21247.54
            ],
            "id": "deimos",
            "radius": 92,
            "type": "boss"
            }
        ],
        "1264": [
            {
            "coord": [
                52293.71,
                32344.45
            ],
            "id": "soulless_horror",
            "radius": 71,
            "type": "boss"
            },
            {
            "coord": [
                52785.4,
                32425.15
            ],
            "id": "river_of_souls",
            "radius": 160,
            "type": "event"
            },
            {
            "coord": [
                52977.9,
                32328.309999999998
            ],
            "id": "river_of_souls",
            "radius": 75,
            "type": "event"
            },
            {
            "coord": [
                52515.75,
                32346.239999999998
            ],
            "id": "river_of_souls",
            "radius": 150,
            "type": "event"
            },
            {
            "coord": [
                52934.29,
                32033.43
            ],
            "id": "broken_king",
            "radius": 90,
            "type": "boss"
            },
            {
            "coord": [
                52861.32,
                32702.5
            ],
            "id": "eater_of_souls",
            "radius": 75,
            "type": "boss"
            },
            {
            "coord": [
                53392.240000000005,
                32350.28
            ],
            "id": "dhuum",
            "radius": 105,
            "type": "boss"
            },
            {
            "coord": [
                53333.93,
                32339.36
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
                46967.68,
                32283.78
            ],
            "id": "conjured_amalgamate",
            "radius": 90,
            "type": "boss"
            },
            {
            "coord": [
                47705.7,
                31716.129999999997
            ],
            "id": "twin_largos",
            "radius": 275,
            "type": "boss"
            },
            {
            "coord": [
                46798,
                31241
            ],
            "id": "qadim",
            "radius": 225,
            "type": "boss"
            }
        ],
        "1306": [
            {
            "coord": [
                52715.41,
                24643.2
            ],
            "id": "freezie",
            "radius": 115,
            "type": "boss"
            }
        ],
        "1323": [{
            "id": "gate",
            "type": "event",
            "coord": [67264, 51980],
            "radius": 206
            },
            {
            "coord": [
                66671.69,
                51324.87
            ],
            "id": "cardinal_sabir",
            "radius": 180,
            "type": "boss"
            },
            {
            "coord": [
                67815.23000000001,
                51519.78
            ],
            "id": "cardinal_adina",
            "radius": 60,
            "type": "boss"
            },
            {
            "coord": [
                67262.01999999999,
                51038.03
            ],
            "id": "qadim_the_peerless",
            "radius": 115,
            "type": "boss"
            }
        ],
        "1331": [
            {
            "coord": [
                59646.71,
                19188.46
            ],
            "id": "legendary_icebrood_construct",
            "radius": 85,
            "type": "boss"
            }
        ],
        "1332": [
            {
            "coord": [
                59646.71,
                19188.46
            ],
            "id": "legendary_icebrood_construct",
            "radius": 85,
            "type": "boss"
            }
        ],
        "1339": [
            {
            "coord": [
                57249.369999999995,
                18009.59
            ],
            "id": "boneskinner",
            "radius": 65,
            "type": "boss"
            }
        ],
        "1340": [
            {
            "coord": [
                57252.520000000004,
                18010.85
            ],
            "id": "voice_and_claw_of_the_fallen",
            "radius": 65,
            "type": "boss"
            }
        ],
        "1341": [
            {
            "coord": [
                57250.740000000005,
                18009.22
            ],
            "id": "fraenir_of_jormag",
            "radius": 65,
            "type": "boss"
            }
        ],
        "1344": [
            {
            "coord": [
                57250.740000000005,
                18009.22
            ],
            "id": "fraenir_of_jormag",
            "radius": 65,
            "type": "boss"
            }
        ],
        "1346": [
            {
            "coord": [
                57252.520000000004,
                18010.85
            ],
            "id": "voice_and_claw_of_the_fallen",
            "radius": 65,
            "type": "boss"
            }
        ],
        "1351": [
            {
            "coord": [
                57249.369999999995,
                18009.59
            ],
            "id": "boneskinner",
            "radius": 65,
            "type": "boss"
            }
        ],
        "1357": [
            {
            "coord": [
                55785,
                19170
            ],
            "id": "whisper_of_jormag",
            "radius": 50,
            "type": "boss"
            }
        ],
        "1359": [
            {
            "coord": [
                55785,
                19170
            ],
            "id": "whisper_of_jormag",
            "radius": 50,
            "type": "boss"
            }
        ],
        "1451": [
            {
                "coord":[
                    26025,
                    99989
                ],
                "id": "minister_li",
                "radius": 49,
                "type": "boss"
            },
            {
                "coord":[
                    25956,
                    100040
                ],
                "id": "minister_li",
                "radius": 30,
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
        "7": "38",
        "37": "region_cantha"
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
        "1250": "gh_haven",
        "1456": "gh_reflection",
        "1444": "gh_reflection",
        "1459": "gh_reflection",
        "1462": "gh_reflection",
        "1463": "gh_reflection",
        "1435": "gh_reflection",
        "1419": "gh_reflection",
        "1426": "gh_reflection",
        "1430": "gh_reflection",
        "1331": "strike_shiverpeaks_pass",
        "1332": "strike_shiverpeaks_pass",
        "1339": "strike_sanctum_arena",
        "1340": "strike_sanctum_arena",
        "1341": "strike_sanctum_arena",
        "1344": "strike_sanctum_arena",
        "1346": "strike_sanctum_arena",
        "1357": "strike_jormag",
        "1359": "strike_jormag",
        "1374": "strike_cold_war",
        "1376": "strike_cold_war",
        "1409": "dragonstorm",
        "1410": "dragonstorm",
        "1411": "dragonstorm",
        "1450": "strike_xunlai",
        "1451": "strike_kaineng",
        "1432": "strike_aetherblade",
        "1437": "strike_harvest"
    },
    "mounts": {
        1: "jackal",
        2: "griffon",
        3: "springer",
        4: "skimmer",
        5: "raptor",
        6: "roller beetle",
        7: "warclaw",
        8: "skyscale",
        9: "skiff",
        10: "siege turtle"
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
        1317,
        1323,
        1330,
        1331,
        1332,
        1339,
        1340,
        1341,
        1343,
        1344,
        1346,
        1351,
        1370,
        1371,
        1442,
        1452,
        1422,
        1428,
        1438,
        1465
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
    try:
        md5_sum = md5sum("downloads/gw2rpc.zip")
    except FileNotFoundError:
        md5_sum = ""
    return render_template('index.html', random_image=image_path, md5_sum=md5_sum)

@app.route('/copy-paste')
def copy_paste():
    chat_code = request.args.get('chat_code', type = str)
    name = request.args.get('name', type = str)
    character = request.args.get('character', type = str)
    return render_template('copy_paste.html', chat_code=chat_code, name=name, character=character)

@app.route('/download/latest')
def download_latest():
    path = "downloads/gw2rpc.zip"
    try:
        return send_file(path, as_attachment=True)
    except:
        return abort(400)

def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

if __name__ == "__main__":
    app.run()
    