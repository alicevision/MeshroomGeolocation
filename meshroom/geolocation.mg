{
    "header": {
        "releaseVersion": "2025.1.0-develop",
        "fileVersion": "2.0",
        "nodesVersions": {
            "CameraInit": "12.0",
            "Download2dMap": "2.0",
            "DownloadLidar3dMap": "2.0",
            "DownloadTopography3dMap": "2.0",
            "GeolocationLidarLasToMesh": "2.0",
            "GetGPSData": "2.0",
            "North": "2.0",
            "Publish": "1.3",
            "Sun": "2.0",
            "WeatherHDRI": "2.0"
        },
        "template": true
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                189,
                212
            ],
            "inputs": {}
        },
        "Download2dMap_1": {
            "nodeType": "Download2dMap",
            "position": [
                647,
                387
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        },
        "DownloadLidar3dMap_1": {
            "nodeType": "DownloadLidar3dMap",
            "position": [
                648,
                286
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        },
        "DownloadTopography3dMap_1": {
            "nodeType": "DownloadTopography3dMap",
            "position": [
                651,
                169
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        },
        "GeolocationLidarLasToMesh_1": {
            "nodeType": "GeolocationLidarLasToMesh",
            "position": [
                848,
                286
            ],
            "inputs": {
                "folder": "{DownloadLidar3dMap_1.outputFolder}",
                "GPSFile": "{DownloadLidar3dMap_1.GPSFile}"
            }
        },
        "GetGPSData_1": {
            "nodeType": "GetGPSData",
            "position": [
                385,
                214
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "North_1": {
            "nodeType": "North",
            "position": [
                647,
                569
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        },
        "Publish_1": {
            "nodeType": "Publish",
            "position": [
                1176,
                318
            ],
            "inputs": {
                "inputFiles": [
                    "{DownloadTopography3dMap_1.output}",
                    "{Download2dMap_1.outputPath}",
                    "{North_1.outputPath}",
                    "{Sun_1.outputPath}",
                    "{WeatherHDRI_1.output}",
                    "{GeolocationLidarLasToMesh_1.outputobj}"
                ]
            }
        },
        "Sun_1": {
            "nodeType": "Sun",
            "position": [
                647,
                671
            ],
            "inputs": {
                "inputFile": "{GetGPSData_1.inputFile}",
                "GPSFile": "{GetGPSData_1.output}"
            }
        },
        "WeatherHDRI_1": {
            "nodeType": "WeatherHDRI",
            "position": [
                646,
                789
            ],
            "inputs": {
                "inputFile": "{GetGPSData_1.inputFile}",
                "GPSFile": "{GetGPSData_1.output}"
            }
        }
    }
}