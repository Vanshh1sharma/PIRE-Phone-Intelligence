import os
from datetime import datetime


def generate_text_report(risk_report):
  
    lines = []

    lines.append(f"Risk Score: {risk_report['risk_score']}/100")
    lines.append(f"Risk Level: {risk_report['risk_level']}")
    lines.append("")

    lines.append("Detailed Checks:")
    for item in risk_report["risk_details"]:
        lines.append(
            f"- {item['check']}: "
            f"score={item['score']}, "
            f"weight={item['weight']} | "
            f"{item['message']}"
        )

    lines.append("")
    lines.append("Flags:")
    if risk_report["flags"]:
        for flag in risk_report["flags"]:
            lines.append(f"- {flag}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append(risk_report["summary"])

    return "\n".join(lines)


def save_text_report(risk_report, filename=None):
  
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "Reports", "text_outputs")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"risk_report_{timestamp}.txt"

    file_path = os.path.join(OUTPUT_DIR, filename)

    text = generate_text_report(risk_report)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

    return file_path
