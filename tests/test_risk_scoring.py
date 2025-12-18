from Core.parse import parse_pipeline
from Core.Scorer import calculate_risk


def test_risk_report_structure():
    result = parse_pipeline("9058578790", region="IN")
    report = calculate_risk(result["parsed"])

    assert "risk_score" in report
    assert "risk_level" in report
    assert "flags" in report
    assert "risk_details" in report


def test_risk_score_range():
    result = parse_pipeline("9058578790", region="IN")
    report = calculate_risk(result["parsed"])

    assert 0 <= report["risk_score"] <= 100


if __name__ == "__main__":
    test_risk_report_structure()
    test_risk_score_range()
    print("Risk scoring tests passed")
