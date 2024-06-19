import os
import json
from datetime import datetime

from constants import DB, REPORT, TIMESTAMPS_PATH

_8PM = 20
SATURDAY = 5
class Tegrity:
    @staticmethod
    def is_report_needed():
        now = datetime.now()
        hour = now.time().hour
        weekday = now.weekday()
        return Tegrity._is_action_needed(REPORT) and hour == _8PM and weekday == SATURDAY

    @staticmethod
    def is_backup_needed():
        return Tegrity._is_action_needed(DB) 

    @staticmethod
    def _is_action_needed(action):
        if not os.path.exists(TIMESTAMPS_PATH):
            open(TIMESTAMPS_PATH, 'w').close()
            return True
        
        with open(TIMESTAMPS_PATH, 'r') as f:
            timestamps = json.load(f)
        
        now = datetime.now()
        
        
        if action in timestamps:
            last_action_date = datetime.fromtimestamp(timestamps[action]).date()
            is_new_month = last_action_date.month != ((now.month - 1 ) % 12) + 1
            is_new_day = last_action_date.day != now.day
            # backup of db happens daily while report happens monthly
            return is_new_day if action == DB else is_new_month
        else:
            return True  # No timestamp found for action, action is needed
        
    @staticmethod
    def stamp(action):
        # update timestamp
        if os.path.exists(TIMESTAMPS_PATH):
            with open(TIMESTAMPS_PATH, 'r') as f:
                timestamps = json.load(f)
        else:
            timestamps = {}

        # Update the timestamp for the given action to current epoch time
        timestamps[action] = datetime.timestamp()

        # Write updated timestamps back to TIMESTAMPS_PATH
        with open(TIMESTAMPS_PATH, 'w') as f:
            json.dump(timestamps, f)

