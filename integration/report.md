# Integration Testing Report

## 2. System Overview

For Part 2, I implemented a command-line system called `StreetRace Manager` in Python under `integration/code/`. The system is organized as separate service modules with shared in-memory data models. This keeps the design simple while still making module interactions explicit and testable.

The final implementation includes all required modules:
- Registration
- Crew Management
- Inventory
- Race Management
- Results
- Mission Planning

It also includes two extra modules:
- Garage
- Ledger

The Garage module was added to manage vehicle damage, repairs, and availability. The Ledger module was added to record money movements such as race prize payouts. These two modules make the business rules easier to enforce and also improve the clarity of integration testing.

## 2.1 Modules Implemented

### Registration Module
- Registers crew members with a generated `member_id`, name, and initial role.
- Prevents downstream modules from using unknown members.

### Crew Management Module
- Assigns operational roles such as `driver`, `mechanic`, and `strategist`.
- Records skill levels.
- Checks whether a required role is currently available.

### Inventory Module
- Tracks vehicles and the global cash balance.
- Also contains simple spare-part and tool tracking hooks.

### Race Management Module
- Creates races.
- Validates driver and vehicle eligibility before entry.
- Completes races and produces result records.

### Results Module
- Records race outcomes.
- Updates rankings using points by finishing position.
- Updates the Inventory cash balance through prize payouts.

### Mission Planning Module
- Creates missions with required crew roles.
- Validates role availability before a mission can start.
- Checks vehicle availability when a mission depends on a vehicle.

### Extra Module 1: Garage
- Marks vehicles as damaged.
- Repairs vehicles.
- Ensures damaged vehicles are unavailable until repaired.
- Requires a mechanic for repairs.

### Extra Module 2: Ledger
- Records financial activity such as prize payouts.
- Makes cash-flow verification easier during testing.

## 2.2 Business Rules Enforced

The system enforces the following integration rules:
- A crew member must be registered before a role can be assigned.
- Only crew members with the `driver` role may be entered into a race.
- A race entry requires a valid and available vehicle.
- A vehicle already reserved for one race cannot be entered into another until the first race completes.
- Completed races are terminal and cannot be re-entered or completed again.
- If a car is damaged, it cannot be used again until it is repaired.
- Repairs require a crew member with the `mechanic` role.
- Healthy vehicles cannot be “repaired” as a no-op.
- Race results update rankings and the Inventory cash balance.
- Prize payouts are recorded in the Ledger.
- Missions cannot start if required roles are unavailable.
- Repeated required roles must be backed by enough matching crew members.
- Missions that depend on a vehicle cannot start if that vehicle is damaged.

These rules are implemented in code and verified using integration tests.

## 2.3 Call Graph Scope

The handwritten call graph for this section should cover the main calls within and between the modules. The most important functions to include are:
- `main()`
- `build_parser()`
- `run_demo()`
- `StreetRaceApp.register_member()`
- `StreetRaceApp.assign_role()`
- `StreetRaceApp.add_vehicle()`
- `StreetRaceApp.create_race()`
- `StreetRaceApp.enter_race()`
- `StreetRaceApp.complete_race()`
- `StreetRaceApp.create_mission()`
- `StreetRaceApp.start_mission()`
- `StreetRaceApp.repair_vehicle()`
- `StreetRaceApp.summary()`
- `RegistrationService.register_member()`
- `CrewService.assign_role()`
- `InventoryService.add_vehicle()`
- `GarageService.mark_damaged()`
- `GarageService.repair_vehicle()`
- `RaceService.create_race()`
- `RaceService.enter_driver()`
- `RaceService.complete_race()`
- `ResultsService.record_result()`
- `MissionPlanningService.create_mission()`
- `MissionPlanningService.start_mission()`
- `LedgerService.record_entry()`

The important inter-module flows to show are:
- registration to crew role assignment
- race entry using crew and inventory validation
- race completion to results to inventory and ledger
- damaged vehicle to garage repair to mission start

## 2.4 Integration Test Cases

### Test Case 1: Register a crew member and assign a role
- Scenario: register a new member and then assign the `driver` role with a skill level.
- Modules involved: Registration, Crew Management.
- Expected result: the role and skill level should update successfully.
- Actual result: worked as expected.
- Why needed: this verifies that role management depends on successful registration.

### Test Case 2: Reject role assignment for an unknown member
- Scenario: try to assign a role to an ID that was never registered.
- Modules involved: Crew Management, Registration.
- Expected result: the system should fail with an explicit error.
- Actual result: worked as expected, raising `ValueError`.
- Why needed: this checks the dependency between crew management and registration data.

### Test Case 3: Add a vehicle and repair it through the garage
- Scenario: add a vehicle, mark it damaged, then repair it using a mechanic.
- Modules involved: Inventory, Garage, Registration, Crew Management.
- Expected result: the vehicle should become unavailable when damaged and available again after repair.
- Actual result: worked as expected.
- Why needed: this verifies vehicle-state flow across multiple modules.

### Test Case 4: Reject repairs by a non-mechanic
- Scenario: attempt to repair a vehicle using a crew member with the `driver` role.
- Modules involved: Garage, Crew Management, Registration.
- Expected result: repair should fail with an explicit error.
- Actual result: worked as expected, raising `ValueError`.
- Why needed: this verifies role-sensitive integration logic.

### Test Case 5: Register a driver and complete a race
- Scenario: register a driver, add a vehicle, create a race, enter the race, complete it, and record the result.
- Modules involved: Registration, Crew Management, Inventory, Race Management, Results, Ledger.
- Expected result: rankings should update, Inventory cash should increase, and Ledger should store a prize entry.
- Actual result: worked as expected.
- Why needed: this is the main end-to-end success flow required by the assignment.

### Test Case 6: Attempt race entry with an unregistered member
- Scenario: try to enter a race using an unknown crew-member ID.
- Modules involved: Race Management, Registration.
- Expected result: the system should fail with an explicit error.
- Actual result: worked as expected, raising `ValueError`.
- Why needed: this checks that race entry depends on valid registration.

### Test Case 7: Attempt race entry with a non-driver
- Scenario: register a crew member as `strategist` and attempt race entry.
- Modules involved: Registration, Crew Management, Race Management.
- Expected result: the system should reject the entry.
- Actual result: worked as expected, raising `ValueError`.
- Why needed: this checks role validation in race management.

### Test Case 8: Reject damaged vehicles during race entry
- Scenario: damage a vehicle first, then attempt to enter it into a race.
- Modules involved: Inventory, Garage, Race Management.
- Expected result: race entry should fail because the vehicle is unavailable.
- Actual result: worked as expected, raising `ValueError`.
- Why needed: this validates the interaction between garage state and race entry.

### Test Case 9: Rankings should sort correctly after multiple races
- Scenario: record race results for two different drivers with different finishing positions.
- Modules involved: Registration, Crew Management, Inventory, Race Management, Results.
- Expected result: the higher-scoring driver should appear first in rankings.
- Actual result: worked as expected.
- Why needed: this verifies repeated interaction between races and result aggregation.

### Test Case 10: Mission cannot start when a required role is missing
- Scenario: create a mission requiring `driver` and `mechanic` when neither role is available.
- Modules involved: Mission Planning, Crew Management.
- Expected result: mission start should fail immediately.
- Actual result: worked as expected, raising `ValueError`.
- Why needed: this verifies precondition checking for missions.

### Test Case 11: Damaged vehicle blocks a mission until repaired
- Scenario: damage a vehicle in a race, then try to start a mission that depends on that vehicle, repair it, and retry.
- Modules involved: Race Management, Results, Garage, Mission Planning, Crew Management.
- Expected result: the first mission start should fail, and the second should succeed after repair.
- Actual result: worked as expected.
- Why needed: this tests an important cross-module flow explicitly mentioned in the assignment.

### Test Case 12: App facade summary reports global system state
- Scenario: execute a complete high-level flow through the `StreetRaceApp` facade and request a summary.
- Modules involved: App facade, Registration, Crew Management, Inventory, Race Management, Results.
- Expected result: summary should show correct cash balance, member count, vehicle count, and rankings.
- Actual result: worked as expected.
- Why needed: this verifies that the CLI-facing orchestration layer is correctly connected to the underlying modules.

### Test Case 13: Interactive CLI session supports a full end-to-end workflow
- Scenario: use one CLI session to register a member, assign a role, add a vehicle, create and complete a race, and then request a summary.
- Modules involved: CLI, App facade, Registration, Crew Management, Inventory, Race Management, Results.
- Expected result: the command-line session should preserve in-memory state and complete the workflow in one process.
- Actual result: worked as expected after adding the interactive session loop.
- Why needed: this fixes the earlier one-shot CLI limitation and proves the submitted terminal interface can actually drive the system.

### Test Case 14: Prevent double-booking the same vehicle into multiple races
- Scenario: enter one vehicle into a race and then attempt to enter the same vehicle into a second race before the first completes.
- Modules involved: Inventory, Garage, Race Management.
- Expected result: the second entry should fail until the first race completes and releases the vehicle.
- Actual result: worked as expected after adding explicit reservation state.
- Why needed: this checks the assignment rule that only available vehicles may be used.

### Test Case 15: Completed races are terminal
- Scenario: complete a race and then try to enter it again or complete it a second time.
- Modules involved: Race Management, Results.
- Expected result: both operations should fail with explicit errors.
- Actual result: worked as expected after adding race-state guards.
- Why needed: this prevents duplicate payouts and duplicate ranking updates.

### Test Case 16: Reject repairs for healthy vehicles
- Scenario: try to repair a vehicle that was never damaged.
- Modules involved: Garage, Inventory.
- Expected result: the repair should fail with an explicit error.
- Actual result: worked as expected after adding the damage-state guard.
- Why needed: this prevents silent no-op repair workflows.

### Test Case 17: Mission role validation counts duplicate requirements
- Scenario: create a mission that requires two drivers but register only one.
- Modules involved: Mission Planning, Crew Management, Registration.
- Expected result: mission start should fail because the crew roster does not satisfy both driver slots.
- Actual result: worked as expected after changing validation from role presence to counted role slots.
- Why needed: this verifies that repeated role requirements are enforced correctly.

## 2.5 Errors Or Issues Found

The integration section was built incrementally using test-first slices, and the following concrete issues were found and fixed:

1. `Error 1: Add interactive CLI session for end-to-end workflows`
   - Problem found: the CLI used one-shot subcommands only, so state was lost between invocations and the terminal interface could not drive the full workflow in one process.
   - Fix: added an interactive session loop with command handlers for registration, role assignment, races, missions, repairs, and summaries.

2. `Error 2: Prevent vehicles from being double-booked`
   - Problem found: the same vehicle could be entered into multiple races simultaneously because availability only checked damage, not reservation state.
   - Fix: added reservation state to vehicles and reserve/release behavior in inventory and race handling.

3. `Error 3: Make completed races terminal`
   - Problem found: completed races could be re-entered and completed again, causing repeated prize payouts and ranking updates.
   - Fix: enforced the race lifecycle so only `planned` races accept entries and only `ready` races can be completed.

4. `Error 4: Reject repairs for healthy vehicles`
   - Problem found: garage repairs silently succeeded even when the vehicle was not damaged.
   - Fix: added an explicit guard that rejects no-op repairs.

5. `Error 5: Count duplicate role requirements in missions`
   - Problem found: mission validation only checked role presence, so one driver incorrectly satisfied `['driver', 'driver']`.
   - Fix: switched mission validation to counted role slots using role-frequency checks.

The only repository-level issue encountered during development was accidental generation of Python cache files under `integration/`. Those generated files were removed and not left as part of the intended submission content.

## 2.6 Verification

The implementation was verified using:

```bash
PYTHONPATH='integration/code' .venv/bin/pytest integration/tests -q
```

Final result:

```text
17 passed in 0.02s
```

Manual CLI verification was also performed with:

```bash
PYTHONPATH='integration/code' .venv/bin/python integration/code/main.py demo
```

This produced a valid JSON summary showing:
- 1 registered member
- 1 vehicle
- updated cash balance
- updated rankings

## 2.7 Summary

The final StreetRace Manager system satisfies the required module list, includes two extra modules, and enforces the main business rules through module interaction rather than isolated logic. The integration tests now cover both success flows and failure flows, including the interactive CLI workflow, race entry validation, vehicle reservation and release, vehicle damage and repair, prize-money updates, rankings, and mission role validation.
