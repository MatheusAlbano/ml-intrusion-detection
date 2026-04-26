from src.analytics import AlertAnalytics


def main():
    print("Generating alert analytics report...\n")

    analytics = AlertAnalytics()

    report = analytics.generate_report()
    csv_path = analytics.export_csv()
    chart_path = analytics.generate_severity_chart()

    print("=== ALERT REPORT ===")
    print(f"Total alerts: {report['total_alerts']}")
    print(f"Critical alerts: {report['critical']}")
    print(f"High alerts: {report['high']}")
    print(f"Medium alerts: {report['medium']}")
    print(
        f"Average attack probability: "
        f"{report['average_probability']}"
    )

    print(f"\nCSV report saved at: {csv_path}")
    print(f"Chart saved at: {chart_path}")


if __name__ == "__main__":
    main()