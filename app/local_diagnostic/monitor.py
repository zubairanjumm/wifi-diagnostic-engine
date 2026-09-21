from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Callable

from app.local_diagnostic.collector import collect_local_diagnostic


@dataclass
class MonitorRun:
    number: int
    result: object
    timestamp: float


class DiagnosticMonitor:
    def __init__(
        self,
        interval_seconds: int = 30,
        on_result: Callable[[MonitorRun], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ):
        self.interval_seconds = interval_seconds
        self.on_result = on_result
        self.on_error = on_error

        self._running = False
        self._thread: threading.Thread | None = None
        self._run_number = 0

    @property
    def running(self) -> bool:
        return self._running

    def start(self):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        self._running = False

    def _run_loop(self):
        while self._running:
            self._run_number += 1

            try:
                result = collect_local_diagnostic()

                monitor_run = MonitorRun(
                    number=self._run_number,
                    result=result,
                    timestamp=time.time(),
                )

                if self.on_result:
                    self.on_result(monitor_run)

            except Exception as error:
                if self.on_error:
                    self.on_error(error)

            for _ in range(self.interval_seconds):
                if not self._running:
                    break

                time.sleep(1)