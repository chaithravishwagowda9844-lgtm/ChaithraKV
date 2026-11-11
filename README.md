## Project Screenshots
# Website Security Header Checker

## Project Description
Website Security Header Checker is a web-based application developed using Python and Flask. It scans websites and checks whether important HTTP security headers are present or missing.

The application helps users understand basic website security configurations and generates a PDF report containing the scan results.

## Features
- Scan any website URL.
- Check important HTTP security headers.
- Identify present and missing security headers.
- Display security scan results.
- Generate and download PDF reports.
- Simple and user-friendly interface.

## Security Headers Checked
1. Strict-Transport-Security
2. Content-Security-Policy
3. X-Frame-Options
4. X-Content-Type-Options
5. Referrer-Policy
6. Permissions-Policy

## Technologies Used
- Python
- Flask
- HTML
- CSS
- JavaScript
- Requests
- ReportLab

## Project Structure
```text
WebsiteSecurityChecker/
│
├── static/
├── templates/
├── app.py
├── scanner.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run the Project

1. Clone the repository.
2. Open the project folder.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Open the local website in your browser using the address displayed by Flask.

## Project Objective
The main objective of this project is to identify missing HTTP security headers and help users understand how website security can be improved.

## Developed For
BCA Internship Project

## Author
Chaithra K V
