{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2021.1.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "GetGPSData": "1.2",
            "MapBuildings": "1.0",
            "CameraInit": "9.0"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                2736,
                -88
            ],
            "inputs": {}
        },
        "GetGPSData_1": {
            "nodeType": "GetGPSData",
            "position": [
                2961,
                -91
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "MapBuildings_1": {
            "nodeType": "MapBuildings",
            "position": [
                3189,
                -94
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}