
from flask import Flask, render_template, request, make_response
from scanner import scan_website
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():

    url = request.form.get("url", "").strip()

    try:
        result = scan_website(url)

        return render_template(
            "result.html",
            result=result
        )

    except ValueError as error:
        return render_template(
            "index.html",
            error=str(error)
        )

    except Exception:
        return render_template(
            "index.html",
            error="Unable to scan this website. Please check the URL and try again."
        )


@app.route("/download-report", methods=["POST"])
def download_report():

    url = request.form.get("url", "").strip()

    try:
        result = scan_website(url)

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=A4)

        width, height = A4

        y = height - 60

        pdf.setTitle("Website Security Report")

        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(50, y, "Website Security Report")

        y -= 40

        pdf.setFont("Helvetica", 11)

        pdf.drawString(50, y, f"Website: {result['url']}")
        y -= 25

        pdf.drawString(50, y, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
        y -= 25

        pdf.drawString(50, y, f"Security Score: {result['score']} / 100")
        y -= 25

        pdf.drawString(50, y, f"Present Headers: {result['present']}")
        y -= 25

        pdf.drawString(50, y, f"Missing Headers: {result['missing']}")
        y -= 40

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(50, y, "Security Header Details")
        y -= 30

        pdf.setFont("Helvetica", 10)

        for item in result["headers"]:

            if y < 100:
                pdf.showPage()
                y = height - 60
                pdf.setFont("Helvetica", 10)

            pdf.drawString(
                50, y,
                f"{item['name']}: {item['status']}"
            )

            y -= 22

        if y < 100:
            pdf.showPage()
            y = height - 60

        y -= 10
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(50, y, "Recommendations")

        y -= 25
        pdf.setFont("Helvetica", 10)

        for item in result["recommendations"]:

            if y < 80:
                pdf.showPage()
                y = height - 60
                pdf.setFont("Helvetica", 10)

            pdf.drawString(
                50, y,
                f"- Add {item['name']} header."
            )

            y -= 20

        pdf.save()

        buffer.seek(0)

        response = make_response(buffer.getvalue())

        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = (
            "attachment; filename=security_report.pdf"
        )

        return response

    except Exception:
        return "Unable to generate the security report. Please scan a valid public website first.", 400


if __name__ == "__main__":
    app.run(debug=True)
