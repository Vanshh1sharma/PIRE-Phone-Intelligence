from Core.parse import parse_pipeline
from Core.Scorer import calculate_risk
from reports.json_report import save_json_report 
from reports.text_report import save_text_report


def main():
    phone_input = input("Enter phone number: ").strip()

    parse_result = parse_pipeline(phone_input, region="IN")

    if not parse_result["success"]:
        print("Parsing failed:", parse_result["error"])
        return

    print("\nParsed Number:")
    print(parse_result["parsed"])

    print("\nNormalized Formats:")
    for name, number in parse_result["normalized"].items():
        print(f"{name}: {number}")

    risk_report = calculate_risk(parse_result["parsed"])

    report_filename = save_json_report(risk_report)
    
    text_path = save_text_report(risk_report)

    print("\nRisk Score:", risk_report["risk_score"])
    print("Risk Level:", risk_report["risk_level"])

    print("\nDetailed Checks:")
    for item in risk_report["risk_details"]:
        print(
            f"{item['check']} | "
            f"Score: {item['score']}/10 | "
            f"Weight: {item['weight']} | "
            f"{item['message']}"
        )

    print("\nFlags:")
    if risk_report["flags"]:
        for flag in risk_report["flags"]:
            print(flag)
    else:
        print("None")

    print("\nSummary:")
    print(risk_report["summary"])

    print("JSON report saved at:", report_filename)
    print("Text report saved at:", text_path)


if __name__ == "__main__":
    main()
