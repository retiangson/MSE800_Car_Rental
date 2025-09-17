from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path

file_path = Path("docs") / "test_results.txt"
destination_path = Path("docs") / "test_results.pdf"

# Read pytest results
print("Reading:", file_path)
with open(file_path, "r", encoding="utf-8") as f:
    results = f.read()

# Create PDF
doc = SimpleDocTemplate(str(destination_path), pagesize=A4)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Car Rental System - Pytest Results", styles["Heading1"]))
story.append(Spacer(1, 12))
story.append(Paragraph(results.replace("\n", "<br/>"), styles["Normal"]))

doc.build(story)

print("PDF exported to:", destination_path)
