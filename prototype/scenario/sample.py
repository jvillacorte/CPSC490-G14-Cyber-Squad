SAMPLE_SCENARIO = {
    "title": "Suspicious download",
    "description": (
        "Investigate the simulated downloads and remove the suspicious file. "
        "All files are fictional and exist only in this application."
    ),
    "files": [
        {
            "path": "/home/student/Downloads/readme.txt",
            "contents": "A normal note about the student's course materials.",
        },
        {
            "path": "/home/student/Downloads/unexpected-update.txt",
            "contents": "An unexpected update appeared after a suspicious email.",
        },
    ],
}
