"""Command-line entrypoint for StreetRace Manager."""

import argparse
import json

from streetrace.app import StreetRaceApp


def build_parser():
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(prog="streetrace-manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("name")
    register_parser.add_argument("role")

    vehicle_parser = subparsers.add_parser("add-vehicle")
    vehicle_parser.add_argument("model")
    vehicle_parser.add_argument("brand")

    subparsers.add_parser("summary")
    subparsers.add_parser("demo")
    return parser


def run_demo(app):
    """Populate a simple scenario and return the resulting summary."""
    driver = app.register_member("Demo Driver", "rookie")
    app.assign_role(driver.member_id, "driver", 8)
    vehicle = app.add_vehicle("Demo Car", "Demo Brand")
    race = app.create_race("Demo Race", 2000)
    app.enter_race(race.race_id, driver.member_id, vehicle.vehicle_id)
    app.complete_race(race.race_id, position=1, damaged=False)
    return app.summary()


def main(argv=None):
    """Run the StreetRace CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    app = StreetRaceApp()

    if args.command == "register":
        member = app.register_member(args.name, args.role)
        print(member.member_id)
        return
    if args.command == "add-vehicle":
        vehicle = app.add_vehicle(args.model, args.brand)
        print(vehicle.vehicle_id)
        return
    if args.command == "summary":
        print(json.dumps(app.summary(), indent=2))
        return
    if args.command == "demo":
        print(json.dumps(run_demo(app), indent=2))
        return
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
