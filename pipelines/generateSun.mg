

{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2021.1.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "Sun": "1.2",
            "CameraInit": "9.0",
            "GetGPSData": "1.2"
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
                225,
                -3
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "Sun_1": {
            "nodeType": "Sun",
            "position": [
                513,
                -5
            ],
            "inputs": {
                "inputFile": "{GetGPSData_1.inputFile}",
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}