"""Command-line entrypoint for StreetRace Manager."""

import argparse
import json
import shlex

from streetrace.app import StreetRaceApp


def build_parser():
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(prog="streetrace-manager")
    subparsers = parser.add_subparsers(dest="command", required=False)

    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("name")
    register_parser.add_argument("role")

    vehicle_parser = subparsers.add_parser("add-vehicle")
    vehicle_parser.add_argument("model")
    vehicle_parser.add_argument("brand")

    subparsers.add_parser("summary")
    subparsers.add_parser("demo")
    subparsers.add_parser("shell")
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


def run_cli_session(app, input_func=input, output_func=print):
    """Run an interactive CLI session that preserves in-memory app state."""
    commands = {
        "register": _session_register,
        "assign-role": _session_assign_role,
        "add-vehicle": _session_add_vehicle,
        "create-race": _session_create_race,
        "enter-race": _session_enter_race,
        "complete-race": _session_complete_race,
        "create-mission": _session_create_mission,
        "start-mission": _session_start_mission,
        "repair-vehicle": _session_repair_vehicle,
        "summary": _session_summary,
        "help": _session_help,
    }

    output_func("StreetRace Manager interactive session. Type help for commands.")
    while True:
        raw = input_func("streetrace> ").strip()
        if not raw:
            continue
        if raw in {"quit", "exit"}:
            output_func("Bye.")
            return
        parts = shlex.split(raw)
        handler = commands.get(parts[0])
        if handler is None:
            raise ValueError(f"Unknown command: {parts[0]}")
        handler(app, parts[1:], output_func)


def _session_register(app, args, output_func):
    """Handle a register command within the interactive CLI."""
    if len(args) != 2:
        raise ValueError("Usage: register <name> <role>")
    member = app.register_member(args[0], args[1])
    output_func(member.member_id)


def _session_assign_role(app, args, output_func):
    """Handle an assign-role command within the interactive CLI."""
    if len(args) != 3:
        raise ValueError("Usage: assign-role <member_id> <role> <skill_level>")
    member = app.assign_role(args[0], args[1], int(args[2]))
    output_func(member.member_id)


def _session_add_vehicle(app, args, output_func):
    """Handle an add-vehicle command within the interactive CLI."""
    if len(args) != 2:
        raise ValueError("Usage: add-vehicle <model> <brand>")
    vehicle = app.add_vehicle(args[0], args[1])
    output_func(vehicle.vehicle_id)


def _session_create_race(app, args, output_func):
    """Handle a create-race command within the interactive CLI."""
    if len(args) != 2:
        raise ValueError("Usage: create-race <name> <prize_money>")
    race = app.create_race(args[0], int(args[1]))
    output_func(race.race_id)


def _session_enter_race(app, args, output_func):
    """Handle an enter-race command within the interactive CLI."""
    if len(args) != 3:
        raise ValueError("Usage: enter-race <race_id> <member_id> <vehicle_id>")
    app.enter_race(args[0], args[1], args[2])
    output_func("ok")


def _session_complete_race(app, args, output_func):
    """Handle a complete-race command within the interactive CLI."""
    if len(args) != 3:
        raise ValueError("Usage: complete-race <race_id> <position> <damaged>")
    damaged = args[2].lower() == "true"
    result = app.complete_race(args[0], int(args[1]), damaged)
    output_func(json.dumps(result.__dict__, indent=2))


def _session_create_mission(app, args, output_func):
    """Handle a create-mission command within the interactive CLI."""
    if len(args) not in {2, 3}:
        raise ValueError(
            "Usage: create-mission <name> <role1,role2,...> [vehicle_id]"
        )
    vehicle_id = args[2] if len(args) == 3 else None
    mission = app.create_mission(args[0], args[1].split(","), vehicle_id=vehicle_id)
    output_func(mission.mission_id)


def _session_start_mission(app, args, output_func):
    """Handle a start-mission command within the interactive CLI."""
    if len(args) != 1:
        raise ValueError("Usage: start-mission <mission_id>")
    mission = app.start_mission(args[0])
    output_func(mission.status)


def _session_repair_vehicle(app, args, output_func):
    """Handle a repair-vehicle command within the interactive CLI."""
    if len(args) != 2:
        raise ValueError("Usage: repair-vehicle <vehicle_id> <mechanic_id>")
    app.repair_vehicle(args[0], args[1])
    output_func("ok")


def _session_summary(app, args, output_func):
    """Handle a summary command within the interactive CLI."""
    if args:
        raise ValueError("Usage: summary")
    output_func(json.dumps(app.summary(), indent=2))


def _session_help(_app, args, output_func):
    """Print supported interactive commands."""
    if args:
        raise ValueError("Usage: help")
    output_func(
        "\n".join(
            [
                "register <name> <role>",
                "assign-role <member_id> <role> <skill_level>",
                "add-vehicle <model> <brand>",
                "create-race <name> <prize_money>",
                "enter-race <race_id> <member_id> <vehicle_id>",
                "complete-race <race_id> <position> <damaged>",
                "create-mission <name> <role1,role2,...> [vehicle_id]",
                "start-mission <mission_id>",
                "repair-vehicle <vehicle_id> <mechanic_id>",
                "summary",
                "quit",
            ]
        )
    )


def main(argv=None):
    """Run the StreetRace CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    app = StreetRaceApp()

    if args.command in {None, "shell"}:
        run_cli_session(app)
        return

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
