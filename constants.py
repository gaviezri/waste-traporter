from pathlib import Path

### GENERAL ###

PROJECT_ROOT = Path(__file__).cwd() 


### SHAREPOINT ###

CREDENTIALS_PATH = PROJECT_ROOT / "credentials.json"
SITE_URL = "https://ctcoeu.sharepoint.com/sites/ITDepartment"
FOLDER_URL = "Shared Documents/%E2%99%BB%EF%B8%8F%20Waste%20Management"
USER = "username"
PASS = "password"

### DATABASE ###

DB_NAME = 'waste-management.db'
DB_BACKUP_FILE = 'waste-management.backup'

### SCALE ###

VENDOR_ID = 0x1A86
PRODUCT_ID = 0x7523