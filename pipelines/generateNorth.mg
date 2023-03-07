{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2021.1.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "North": "1.2",
            "GetGPSData": "1.2",
            "CameraInit": "9.0"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                1692,
                -202
            ],
            "inputs": {}
        },
        "GetGPSData_1": {
            "nodeType": "GetGPSData",
            "position": [
                1917,
                -205
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "North_1": {
            "nodeType": "North",
            "position": [
                2170,
                -200
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}