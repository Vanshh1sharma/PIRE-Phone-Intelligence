from reports.text_report import generate_text_report


def test_text_report_generation():
    dummy_report = {
        "risk_score": 10,
        "risk_level": "LOW",
        "flags": [],
        "risk_details": [
            {
                "check": "Region",
                "score": 2,
                "weight": 15,
                "message": "Region: IN"
            }
        ],
        "summary": "Risk Score: 10/100 - Level: LOW"
    }

    text = generate_text_report(dummy_report)

    assert "Risk Score" in text
    assert "Region" in text


if __name__ == "__main__":
    test_text_report_generation()
    print("Report tests passed")
