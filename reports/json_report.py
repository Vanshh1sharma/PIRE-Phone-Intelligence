import json
import os
from datetime import datetime


def save_json_report(risk_report, filename=None):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "Reports", "json_outputs")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"risk_report_{timestamp}.json"

    file_path = os.path.join(OUTPUT_DIR, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(risk_report, file, indent=4)

    return file_path
