
#! /usr/bin/env python

import sys, os
import argparse

#Format would be easier with pandas but not available in CMSSW7
#Define the point you want to generate with 4 parameters
#{'model': ['Scalar'], 'mChi': [1], 'mPhi': [75, 125, 150], 'gq': [1], 'gDM' : [1]}

MassScalar = [
    ['MassScalar'],
    [
        {'model': ['Scalar'],'mChi': [1], 'mPhi': [75, 125, 150], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [10], 'mPhi': [75, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [20], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [30], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]}
        ]
    ]


MassPseudo = [
    ['MassPseudo'],
    [
        {'model': ['Pseudo'],'mChi': [1], 'mPhi': [75, 125, 150, 250], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [10], 'mPhi': [75, 125, 150, 200, 250], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [20], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [30], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [50], 'mPhi': [175, 225, 250], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [30], 'mPhi': [175, 225, 250], 'gq': [1], 'gDM' : [1]},
        ]
    ]

Coupling = [
    ['Coupling'],
    [{'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [10], 'gq': [0.1, 0.2, 0.5, 0.6, 0.7, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [20], 'gq': [0.1, 0.2, 0.5, 0.6, 0.7, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [50], 'gq': [0.2, 0.5, 0.6, 0.7, 0.8, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [100], 'gq': [0.2, 0.5, 0.6, 0.7, 0.8, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [200], 'gq': [0.5, 0.7, 1, 1.3, 1.4, 1.5], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [300], 'gq': [0.5, 1, 1.3, 1.4, 1.6, 2], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [500], 'gq': [0.5, 1, 1.5,2, 2.5, 3, 3.5], 'gDM' : [1]}
     ]
    ]


Test = [
    ['Test'],
    [{'model': ['Scalar','Pseudo'],'mChi': [1,20], 'mPhi': [10,50], 'gq': [1], 'gDM' : [1]},
]]

AddMass = [
    ['AddMass'],
    [{'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [250,400, 450], 'gq': [1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [20, 50], 'mPhi': [250, 400, 450, 500], 'gq': [1], 'gDM' : [1]}
     ]]

Diagonal = [
    ['Diagonal'],
    [{'model': ['Scalar','Pseudo'],'mChi': [25, 17, 12.5], 'mPhi': [50], 'gq': [1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [50, 30, 20], 'mPhi': [100], 'gq': [1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [100, 70], 'mPhi': [200], 'gq': [1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [150, 100, 75], 'mPhi': [300], 'gq': [1], 'gDM' : [1]}
     ]]

AddMass2 = [
    ['AddMass2'],
    [
        {'model': ['Pseudo'],'mChi': [10], 'mPhi': [40], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [15], 'mPhi': [40, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [20], 'mPhi': [60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [30], 'mPhi': [65, 90], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [35], 'mPhi': [60, 90, 130], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [45], 'mPhi': [130], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [10], 'mPhi': [30, 40, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [15], 'mPhi': [35, 40, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [20], 'mPhi': [30, 45, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [35], 'mPhi': [125, 130], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [40], 'mPhi': [125, 130], 'gq': [1], 'gDM' : [1]}

        ]
    ]


AddMass3Scalar = [
    ['AddMass3Scalar'],
    [
        {'model': ['Scalar'],'mPhi': [20], 'mChi': [7, 9], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [30], 'mChi': [14], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [50], 'mChi': [15], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [60], 'mChi': [1,25,29], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [70], 'mChi': [1,25,30, 34], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [80], 'mChi': [1,25,30, 35, 39], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [90], 'mChi': [1,30,35, 40, 44], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [100], 'mChi': [1,35,40], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [110], 'mChi': [1,40,45], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [120], 'mChi': [1,40,45,50], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [130], 'mChi': [1,50], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [140], 'mChi': [1,50], 'gq': [1], 'gDM' : [1]},

        ]
    ]

AddMass3Pseudo = [
    ['AddMass3Pseudo'],
    [
        {'model': ['Pseudo'],'mPhi': [20], 'mChi': [7, 9], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [30], 'mChi': [14], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [50], 'mChi': [15], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [60], 'mChi': [1,25,29], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [70], 'mChi': [1,25,30, 34], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [80], 'mChi': [1,25,30, 35, 39], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [90], 'mChi': [1,30,35, 40, 44], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [100], 'mChi': [1,35,40], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [110], 'mChi': [1,40,45], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [120], 'mChi': [1,40,45,50], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [130], 'mChi': [1,50], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [140], 'mChi': [1,50], 'gq': [1], 'gDM' : [1]},

        ]
    ]

AddMass4Pseudo = [
    ['AddMass4Pseudo'],
    [
        {'model': ['Pseudo'],'mPhi': [10], 'mChi': [4, 6, 8], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [20], 'mChi': [11, 15], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [30], 'mChi': [16, 20], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [40], 'mChi': [19, 21, 25], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [50], 'mChi': [24, 26], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [60], 'mChi': [31], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [70], 'mChi': [36, 40], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [80], 'mChi': [41, 45], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [90], 'mChi': [46, 50], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [100], 'mChi': [45, 49, 51, 55], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [110], 'mChi': [50, 54, 56, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [120], 'mChi': [55, 59], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [130], 'mChi': [55, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [140], 'mChi': [55, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [175], 'mChi': [1, 70, 80], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [200], 'mChi': [1, 70, 80], 'gq': [1], 'gDM' : [1]},

        ]
    ]


AddMass4Scalar = [
    ['AddMass4Scalar'],
    [
        {'model': ['Scalar'],'mPhi': [10], 'mChi': [4, 6, 8], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [20], 'mChi': [11, 15], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [30], 'mChi': [16, 20], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [40], 'mChi': [19, 21, 25], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [50], 'mChi': [24, 26], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [60], 'mChi': [31], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [70], 'mChi': [36, 40], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [80], 'mChi': [41, 45], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [90], 'mChi': [46, 50], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [100], 'mChi': [45, 49, 51, 55], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [110], 'mChi': [50, 54, 56, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [120], 'mChi': [55, 59], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [130], 'mChi': [55, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [140], 'mChi': [55, 60], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [175], 'mChi': [1, 70, 80], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [200], 'mChi': [1, 70, 80], 'gq': [1], 'gDM' : [1]},

        ]
    ]


AddMass5Pseudo = [
    ['AddMass5Pseudo'],
    [
        {'model': ['Pseudo'],'mPhi': [120], 'mChi': [61], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [130], 'mChi': [64,66], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [140], 'mChi': [65,69,71], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [150], 'mChi': [60,65,70,74,76], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [175], 'mChi': [85,87,88], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [200], 'mChi': [85,90,95,99,101], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [210], 'mChi': [1, 75, 85, 95, 100, 104, 106], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [220], 'mChi': [1, 75, 85, 95, 100, 105, 109,111], 'gq': [1], 'gDM' : [1]},
        ]
    ]

AddMass6Pseudo = [
    ['AddMass6Pseudo'],
    [
        {'model': ['Pseudo'],'mPhi': [160], 'mChi': [1,55,65,75,79,81], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [170], 'mChi': [1,60,70,80,84,86], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [180], 'mChi': [1,70,80,85,89,91], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [190], 'mChi': [1,65,75,85,90,94,96], 'gq': [1], 'gDM' : [1]},
        ]
    ]

AddMass7Scalar = [
    ['AddMass7Scalar'],
    [
        {'model': ['Scalar'],'mPhi': [230], 'mChi': [1,90,110,114,116], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [240], 'mChi': [1,80,100,115,119,121], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [250], 'mChi': [85, 105, 120, 124, 126], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [260], 'mChi': [1, 90, 110, 125, 129, 131], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [270], 'mChi': [1, 90, 110, 130, 134, 136], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [280], 'mChi': [1, 95, 115, 135, 139, 141], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [290], 'mChi': [1, 100, 120, 140, 144, 146], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [300], 'mChi': [105, 125, 145, 149, 151], 'gq': [1], 'gDM' : [1]},
        ]
    ]

AddMass7Pseudo = [
    ['AddMass7Pseudo'],
    [
        {'model': ['Pseudo'],'mPhi': [210], 'mChi': [1,74,85], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [220], 'mChi': [1,75,85,90], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [230], 'mChi': [1,90,95], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [240], 'mChi': [1,80,100], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [250], 'mChi': [1,85,100], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [260], 'mChi': [1,90,105], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [270], 'mChi': [1,90,110], 'gq': [1], 'gDM' : [1]},
        ]
    ]

AddMass8Pseudo = [
    ['AddMass8Pseudo'],
    [
        {'model': ['Pseudo'],'mPhi': [230], 'mChi': [1,90,110,114,116], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [240], 'mChi': [1,80,100,115,119,121], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [250], 'mChi': [85, 105, 120, 124, 126], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [260], 'mChi': [1, 90, 110, 125, 129, 131], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [270], 'mChi': [1, 90, 110, 130, 134, 136], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [280], 'mChi': [1, 95, 115, 135, 139, 141], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [290], 'mChi': [1, 100, 120, 140, 144, 146], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mPhi': [300], 'mChi': [105, 125, 145, 149, 151], 'gq': [1], 'gDM' : [1]},
        ]
    ]
AddMass9Scalar = [
    ['AddMass9Scalar'],
    [
        {'model': ['Scalar'],'mPhi': [210], 'mChi': [1,74,85], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [220], 'mChi': [1,75,85,90], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [230], 'mChi': [1,90,95], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [240], 'mChi': [1,80,100], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [250], 'mChi': [1,85,100], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [260], 'mChi': [1,90,105], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [270], 'mChi': [1,90,110], 'gq': [1], 'gDM' : [1]},
        ]
    ]

AddMass10 = [
    ['AddMass10'],
    [
        {'model': ['Pseudo'],'mPhi': [30], 'mChi': [1,11], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [180], 'mChi': [1, 65, 75, 85, 89, 91], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [190], 'mChi': [1, 70, 80, 90, 94, 96], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [200], 'mChi': [90, 95, 99], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [210], 'mChi': [95, 100, 104], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [220], 'mChi': [100, 105, 109], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [230], 'mChi': [105, 110, 114], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [240], 'mChi': [110, 115, 119], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [250], 'mChi': [110, 120, 124], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [260], 'mChi': [115, 125, 129], 'gq': [1], 'gDM' : [1]},

        ]
    ]


AddMass11_width = [
    ['AddMass11_width'],
    [
        {'model': ['Scalar','Pseudo'],'mPhi': [30], 'mChi': [14.4,14.5,14.6,14.7,14.8,14.9,15.1,15.2,15.3,15.6,20], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar','Pseudo'],'mPhi': [150], 'mChi': [74.6,74.7,74.8,74.9,75.1,75.2,75.3,80], 'gq': [1], 'gDM' : [1]},

        ]
    ]

AddMass12_scalar = [
    ['AddMass12_scalar'],
    [
        {'model': ['Scalar'],'mPhi': [130], 'mChi': [64, 66], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [140], 'mChi': [65, 69, 71], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [150], 'mChi': [70, 74, 76], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mPhi': [175], 'mChi': [86, 88], 'gq': [1], 'gDM' : [1]},

        ]
    ]



mAll = [MassScalar, MassPseudo, Coupling, Test, AddMass, Diagonal, 
        AddMass2,AddMass3Scalar,AddMass3Pseudo, AddMass4Pseudo, AddMass4Scalar,AddMass5Pseudo,
        AddMass6Pseudo,AddMass7Scalar,AddMass7Pseudo,AddMass8Pseudo,AddMass9Scalar,AddMass10, AddMass11_width, AddMass12_scalar]
##################################

nEvents = 100000
import time,datetime,random

rseed = datetime.datetime.now()
seed = random.randint(1, 50000) 


def createJobs(mSample, filein, outlocation,scenario):
    jobs = []
    counter = 0
    for sample in mSample[1]:
        models = sample['model']
        mChis = sample['mChi']
        mPhis = sample['mPhi']
        gqs = sample['gq']
        gDMs = sample['gDM']
        for model in models:
            for mChi in mChis:
                for mPhi in mPhis:
                    for gq in gqs:
                        for gDM in gDMs:
                            print "model", model,"mChi",mChi,"mPhi",mPhi, "gq", gq,"gDM", gDM
                            fileout = filein.replace("X",str(mChi).replace('.','p')).replace("Y",str(mPhi).replace('.','p')+"_MG").replace('Model',model).replace('VarGDM',str(gDM).replace('.','p')).replace('VarGq',str(gq).replace('.','p'))
                            
                            f = open(filein,'r')
                            filedata = f.read()
                            f.close()
                            
                            newdata = filedata.replace("VarMphi",str(mPhi)).replace("VarMchi",str(mChi))
                            
                            newdata = newdata.replace("Varnevents",str(nEvents))
                            newdata = newdata.replace("VarIseed",str(seed))
                            newdata = newdata.replace("VarModel",str(model))
                            newdata = newdata.replace("VarScenario",str(scenario))
                            newdata = newdata.replace("VarLocation",str(outlocation))
                            newdata = newdata.replace("VarGDMstr",str(gDM).replace('.','p'))
                            newdata = newdata.replace("VarGqstr",str(gq).replace('.','p'))
                            newdata = newdata.replace("VarGDM",str(gDM))
                            newdata = newdata.replace("VarGq",str(gq))
                            counter = counter+1
                            f = open(fileout,'w')
                            f.write(newdata)
                            f.close()
                            jobs.append(fileout)
    
    return jobs
if __name__ == "__main__":
    
    filein = "ttDMModel_MchiXMphiY_CMS_5F_gDMVarGDM_gqVarGq.sh"
    scenario = 'Scalar'
    mModel = mAll[0]

    inputs = [x[0][0] for x in mAll]


    if len(sys.argv) > 1:
        scenario = sys.argv[1]
        if scenario in inputs:
            print "Running scenario: ", scenario
        else:
            print "No valid input provided"
            print "Possible input scenarios are (check in code for more detail): ", inputs
            exit(0)
    else:
        print "No input provided"
        print "Possible input scenarios are (check in code for more detail): ", inputs
        exit(0)

    for m in mAll:
        print m[0]
        if scenario in m[0]:
            mModel = m

    print "running the following setup"
    print mModel
    print '=============================='

    counter = 0
 #   outlocation = '/eos/cms/store/cmst3/group/susy/clseitz/DMsignal/' #doesn't seemm to work
    outlocation = os.getcwd() +"/"
    print outlocation
    jobs = createJobs(mModel, filein, outlocation, scenario)


    outFolder = outlocation+'output_' + str(scenario) + '_' + str(seed)
    try: os.stat(outFolder) 
    except: os.mkdir(outFolder)

    try: os.stat(outFolder + '/logs') 
    except: os.mkdir(outFolder + '/logs')

    try: os.stat(outFolder +'/cards') 
    except: os.mkdir(outFolder + '/cards')

    for job in jobs:    
        cmd = "mv "+ job + " " + outFolder+"/cards/."
#        print cmd
        os.system(cmd)

    submit = raw_input("Do you also want to submit "+str(len(jobs))+" jobs to the batch system? [y/n] ")
    if submit == 'y' or submit=='Y':
        print "Submitting jobs"
        for job in jobs:    
            cmd = "bsub -q 2nd -o " + outFolder+ "/logs/" + job.replace('.sh','_STDOUT.txt') + " -e "+outFolder+ "/logs/" + job.replace('.sh','_ERR.txt') + " batchRunner.sh "  + outFolder+"/cards/"+job
            print cmd
            os.system(cmd)

    else:
        print "Not submitting jobs"
            
