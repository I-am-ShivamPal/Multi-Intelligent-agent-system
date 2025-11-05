import os
import csv
import datetime
from core.sovereign_bus import bus
from core.logger import AgentLogger

class UptimeMonitor:
    """Maintains a synthetic uptime/downtime timeline."""
    def __init__(self, timeline_file):
        self.timeline_file = timeline_file
        self.logger = AgentLogger("UptimeMonitor")
        self.last_status = self._get_initial_status()
        if self.last_status is None:
            self.update_status("UP", "Initial status check")
        self.logger.info("Agent monitoring started", initial_status=self.last_status or "UP")

    def _get_initial_status(self):
        """Reads the last known status from the timeline file."""
        # Ensure the directory for the log file exists.
        os.makedirs(os.path.dirname(self.timeline_file), exist_ok=True)

        if not os.path.exists(self.timeline_file):
            with open(self.timeline_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'status', 'event'])
            return None
        else:
            try:
                with open(self.timeline_file, 'r', newline='') as f:
                    # Read all rows and get the last one's status
                    rows = list(csv.reader(f))
                    # Handle empty file or header-only file
                    if len(rows) > 1:
                        return rows[-1][1]
                    else:
                        return None
            except (IOError, IndexError):
                return None

    def update_status(self, new_status, event_description):
        """Logs a status change to the timeline if the status is different."""
        if new_status != self.last_status:
            timestamp = datetime.datetime.now().isoformat()
            with open(self.timeline_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, new_status, event_description])
            self.logger.log_action("status_change", new_status, 
                                 previous_status=self.last_status,
                                 reason=event_description)
            self.last_status = new_status
            bus.publish(f"system.{new_status.lower()}", {"reason": event_description})
        else:
            self.logger.debug("Status unchanged", status=self.last_status)

