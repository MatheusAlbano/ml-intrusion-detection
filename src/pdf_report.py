from pathlib import Path
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from src.analytics import AlertAnalytics


class PDFReportGenerator:

    def __init__(self, output_folder="reports"):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(
            exist_ok=True
        )

    def generate(self):
        analytics = AlertAnalytics()
        report = analytics.generate_report()

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_file = (
            self.output_folder /
            f"executive_report_{timestamp}.pdf"
        )

        document = SimpleDocTemplate(
            str(output_file)
        )

        styles = getSampleStyleSheet()

        content = []

        title = Paragraph(
            "Intrusion Detection Executive Report",
            styles["Title"]
        )

        content.append(title)
        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                f"Generated at: {datetime.now()}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                f"Total alerts: {report['total_alerts']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Critical alerts: {report['critical']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"High alerts: {report['high']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Medium alerts: {report['medium']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Average attack probability: {report['average_probability']}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 30))

        content.append(
            Paragraph(
                "Executive Summary:",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                "The intrusion detection system identified suspicious "
                "network activities with high confidence. Most alerts "
                "were classified as critical, indicating strong evidence "
                "of malicious behavior.",
                styles["Normal"]
            )
        )

        document.build(content)

        return output_file