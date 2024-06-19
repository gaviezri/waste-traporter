from pathlib import Path

### GENERAL ###

PROJECT_ROOT = Path(__file__).cwd() 
CONFIG_PATH = PROJECT_ROOT / "config.json"

### SHAREPOINT ###

CREDENTIALS = "credentials"
SITE_URL = "https://ctcoeu.sharepoint.com/sites/ITDepartment"
FOLDER_URL = "Shared Documents/%E2%99%BB%EF%B8%8F%20Waste%20Management"
USER = "username"
PASS = "password"

### DATABASE ###

DB_NAME = 'waste-management.db'
DB_BACKUP_FILE = 'waste-management.backup'

### TEGRITY ###

TIMESTAMPS_PATH = PROJECT_ROOT / "timestamps.json"
DB = "db"
REPORT = "report"

### SCALE ###

SCALE = "scale"
BASE16 = 16

### UI ###

CANCEL = "-CANCEL-"
WEIGHT = '-WEIGHT-'
WHITE = 'white'
GREEN = "#543CC5"

