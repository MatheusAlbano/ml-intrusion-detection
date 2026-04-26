from src.analytics import AlertAnalytics


def main():
    print("Generating alert analytics report...\n")

    analytics = AlertAnalytics()
    report = analytics.generate_report()

    print("=== ALERT REPORT ===")
    print(f"Total alerts: {report['total_alerts']}")
    print(f"Critical alerts: {report['critical']}")
    print(f"High alerts: {report['high']}")
    print(f"Medium alerts: {report['medium']}")
    print(
        f"Average attack probability: "
        f"{report['average_probability']}"
    )


if __name__ == "__main__":
    main()