{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2021.1.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "TopographyMap3D": "1.2",
            "CameraInit": "9.0",
            "GetGPSData": "1.2"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                3689,
                -88
            ],
            "inputs": {}
        },
        "GetGPSData_1": {
            "nodeType": "GetGPSData",
            "position": [
                3914,
                -91
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "TopographyMap3D_1": {
            "nodeType": "TopographyMap3D",
            "position": [
                4131,
                -89
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}