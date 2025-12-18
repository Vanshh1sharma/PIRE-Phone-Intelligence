# PIRE – Phone Intelligence & Risk Engine

PIRE (Phone Intelligence & Risk Engine) is a rule-based system built in Python to analyze phone numbers and assess potential risk using multiple technical signals.

The project focuses on clean architecture, explainable scoring, and practical engineering practices rather than black-box models.

---

## 📌 Features

- Phone number parsing and normalization
- Validation using international numbering rules
- Risk analysis based on:
  - Number type (mobile, VOIP, toll-free, etc.)
  - Carrier availability
  - Geographic region
  - Timezone consistency
  - Formatting and validity checks
- Weighted risk scoring (0–100)
- Risk levels: LOW / MEDIUM / HIGH / CRITICAL
- Explainable flags for suspicious signals
- JSON and text report generation
- Basic test cases for core functionality

---

## 🏗 Project Structure

```text
PIRE-Phone-Intelligence/
├── Core/
│   ├── parse.py
│   └── Scorer.py
├── Reports/
│   ├── json_report.py
│   ├── text_report.py
│   └── outputs/
├── tests/
│   ├── test_parsing.py
│   ├── test_risk_scoring.py
│   └── test_reports.py
├── main.py
├── requirements.txt
└── README.md




⚙️ Installation & Setup

1. Clone the repository

git clone https://github.com/<your-username>/PIRE-Phone-Intelligence.git

cd PIRE-Phone-Intelligence

2. Create and activate virtual environment

python -m venv OSINT

Windows (PowerShell):

.\OSINT\Scripts\Activate
source OSINT/bin/activate

3. Install dependencies

pip install -r requirements.txt

Run the main program:

python main.py

You will be prompted to enter a phone number.

The system will:

Parse and validate the number

Analyze risk signals

Display results in the terminal

Save JSON and text reports in Reports/outputs/

🧪 Running Tests

Run tests as modules from the project root:

python -m tests.test_parsing
python -m tests.test_risk_scoring
python -m tests.test_reports

⚠️ Limitations

Rule-based system (no machine learning)

Risk scores are heuristic, not definitive judgments

Carrier and region metadata may be incomplete or outdated

Not intended for real-time fraud prevention in production systems

🚀 Future Improvements

API interface

Machine learning–assisted scoring

OSINT data integration

Batch analysis support

Web-based dashboard

going to add Opencage library

📄 License

This project is for educational and research purposes.