"""Command-line entrypoint for StreetRace Manager."""

from streetrace.app import StreetRaceApp


def main():
    """Create the application and print a simple startup message."""
    StreetRaceApp()
    print("StreetRace Manager ready")


if __name__ == "__main__":
    main()
