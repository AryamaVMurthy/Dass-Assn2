# DASS Assignment 2 Submission

This repository contained the submission for Assignment 2 of Design and Analysis of Software Systems. It was organized exactly in the structure required in [Assignment.md](/home/aryamavmurthy/work/Dass_Assn/ASSN-2/Dass-Assn2/Assignment.md).

## Git Repository

- Repository link: `https://github.com/AryamaVMurthy/Dass-Assn2`
- OneDrive archive link: `https://iiithydstudents-my.sharepoint.com/:u:/g/personal/aryama_murthy_students_iiit_ac_in/IQA9BsJaEkSUQIWHSGcNSRKKAYQn-BS7RJ57KYVDXeT4Knw?e=V2iMXP`

## Submission Note

The complete assignment archive, including the `.git` directory, was provided through the OneDrive link above. If the Moodle upload size limit prevented uploading the full archive directly, the README-only ZIP was intended to be submitted there with these links.

## Repository Structure

```text
.
├── whitebox/
│   ├── code/
│   ├── diagrams/
│   ├── tests/
│   └── report.pdf
├── integration/
│   ├── code/
│   ├── diagrams/
│   ├── tests/
│   └── report.pdf
├── blackbox/
│   ├── tests/
│   └── report.pdf
└── README.md
```

## Prerequisites

The work was run with Python 3 and `pytest`. The commands below assumed execution from the repository root.

If the virtual environment was already present, the test commands could be run directly. Otherwise, install the required packages in the active environment before running the suites.

## Part 1: White Box Testing

### Contents

- Source code: `whitebox/code/moneypoly/`
- Hand-drawn CFG images: `whitebox/diagrams/`
- Test suite: `whitebox/tests/`
- Report: `whitebox/report.pdf`

### Run the MoneyPoly code

```bash
cd whitebox/code/moneypoly
python main.py
```

### Run the white-box tests

```bash
PYTHONPATH='whitebox/code/moneypoly' .venv/bin/pytest whitebox/tests -q
```

## Part 2: Integration Testing

### Contents

- StreetRace Manager code: `integration/code/`
- Hand-drawn call graph: `integration/diagrams/`
- Integration tests: `integration/tests/`
- Report: `integration/report.pdf`

### Run the StreetRace Manager CLI

```bash
cd integration/code
python main.py shell
```

### Run the integration tests

```bash
pytest integration/tests -q
```

## Part 3: Black Box API Testing

### Contents

- API test suite: `blackbox/tests/`
- Report: `blackbox/report.pdf`

### Prerequisite

The QuickCart API server had to be running locally before the black-box tests were executed. By default, the tests used:

```text
QUICKCART_BASE_URL=http://127.0.0.1:8080
QUICKCART_ROLL_NUMBER=2024101043
```

These could be overridden with environment variables if needed.

### Run the black-box tests

```bash
.venv/bin/pytest blackbox/tests -q
```

## Reports

The final PDF reports submitted for the assignment were:

- `whitebox/report.pdf`
- `integration/report.pdf`
- `blackbox/report.pdf`
