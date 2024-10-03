{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2024.1.0-develop",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "CameraInit": "11.0",
            "GetGPSData": "2.0",
            "Map2D": "2.0"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                0,
                0
            ],
            "inputs": {}
        },
        "GetGPSData_1": {
            "nodeType": "GetGPSData",
            "position": [
                200,
                0
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "Map2D_1": {
            "nodeType": "Map2D",
            "position": [
                400,
                0
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}