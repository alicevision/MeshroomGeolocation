{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2021.1.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "GetGPSData": "1.2",
            "Map2D": "1.2",
            "CameraInit": "9.0"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                2744,
                -239
            ],
            "inputs": {}
        },
        "GetGPSData_1": {
            "nodeType": "GetGPSData",
            "position": [
                2969,
                -242
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "Map2D_1": {
            "nodeType": "Map2D",
            "position": [
                3175,
                -240
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}