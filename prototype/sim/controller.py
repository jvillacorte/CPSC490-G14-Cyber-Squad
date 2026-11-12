from scenario.models import Scenario, SimulatedFile
from sim.engine import SimulationEngine


class SimulationController:
    def __init__(self):
        self.scenario: Scenario | None = None
        self.engine: SimulationEngine | None = None

    def start_scenario(self, data: object) -> Scenario:
        scenario = Scenario.model_validate(data)
        engine = SimulationEngine(scenario)
        self.scenario = scenario
        self.engine = engine
        return scenario

    def file_paths(self) -> tuple[str, ...]:
        return self._active_engine().paths

    def inspect_file(self, path: str) -> SimulatedFile:
        return self._active_engine().inspect_file(path)

    def delete_file(self, path: str) -> None:
        self._active_engine().delete_file(path)

    def _active_engine(self) -> SimulationEngine:
        if self.engine is None:
            raise RuntimeError("Start a scenario before using simulated files")
        return self.engine
