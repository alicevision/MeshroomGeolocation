{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2021.1.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "CameraInit": "9.0",
            "Mesh3D": "1.2",
            "GetGPSData": "1.2",
            "Merge": "1.2",
            "Map3D": "1.2"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                96,
                -123
            ],
            "inputs": {}
        },
        "GetGPSData_1": {
            "nodeType": "GetGPSData",
            "position": [
                321,
                -126
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}"
            }
        },
        "Map3D_1": {
            "nodeType": "Map3D",
            "position": [
                535,
                -125
            ],
            "inputs": {
                "GPSFile": "{GetGPSData_1.output}"
            }
        },
        "Merge_1": {
            "nodeType": "Merge",
            "position": [
                742,
                -129
            ],
            "inputs": {
                "folder": "{Map3D_1.outputFolder}",
                "GPSFile": "{Map3D_1.GPSFile}"
            }
        },
        "Mesh3D_1": {
            "nodeType": "Mesh3D",
            "position": [
                939,
                -129
            ],
            "inputs": {
                "folder": "{Merge_1.outputFolder}",
                "GPSFile": "{Merge_1.GPSFile}"
            }
        }
    }
}