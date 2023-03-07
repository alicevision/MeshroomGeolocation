{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2021.1.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "GetGPSData": "1.2",
            "CameraInit": "9.0",
            "WeatherHDRI": "1.2"
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
        "WeatherHDRI_1": {
            "nodeType": "WeatherHDRI",
            "position": [
                3228,
                -88
            ],
            "inputs": {
                "inputFile": "{GetGPSData_1.inputFile}",
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}