"""Results service for StreetRace Manager."""

from streetrace.models import RankingEntry


class ResultsService:
    """Records race outcomes and updates downstream state."""

    def __init__(self, inventory_service, ledger_service):
        """Bind results to inventory and ledger state."""
        self._inventory = inventory_service
        self._ledger = ledger_service
        self._rankings = {}

    def record_result(self, race_result):
        """Apply a race result to rankings and prize accounting."""
        self._rankings[race_result.member_id] = (
            self._rankings.get(race_result.member_id, 0)
            + self._points_for_position(race_result.position)
        )
        if race_result.prize_money > 0:
            self._inventory.adjust_cash(
                race_result.prize_money, "Prize payout from race results"
            )
            self._ledger.record_entry(
                "prize",
                race_result.prize_money,
                f"Prize for {race_result.race_id}",
            )

    def get_rankings(self):
        """Return rankings sorted by descending points."""
        return [
            RankingEntry(member_id=member_id, points=points)
            for member_id, points in sorted(
                self._rankings.items(), key=lambda item: item[1], reverse=True
            )
        ]

    @staticmethod
    def _points_for_position(position):
        """Map a finishing position to ranking points."""
        if position == 1:
            return 10
        if position == 2:
            return 6
        if position == 3:
            return 4
        return 1
