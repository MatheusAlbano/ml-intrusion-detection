from src.live_monitor import LiveMonitor
from src.config import TEST_FILE


def main():
    monitor = LiveMonitor(TEST_FILE)
    monitor.start(interval=2)


if __name__ == "__main__":
    main()