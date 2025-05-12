import subprocess
import os
from datetime import datetime
import sys

def run_command(command):
    """Execute a shell command and return its output"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e.stderr}")
        return None

def create_backup_folder():
    """Create a backup folder if it doesn't exist"""
    backup_dir = "heroku_backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

def convert_dump_to_sql(dump_path, sql_path):
    """Convert a .dump file to .sql format using pg_restore"""
    print(f"Converting {os.path.basename(dump_path)} to SQL format...")
    
    # Command to convert dump to SQL
    convert_command = f"pg_restore -f {sql_path} {dump_path}"
    
    if run_command(convert_command) is None:
        return False
    
    print(f"Successfully converted to: {os.path.basename(sql_path)}")
    return True

def backup_heroku_app(app_name, backup_dir):
    """Create a backup of a Heroku app and convert it to SQL"""
    # Get current timestamp
    timestamp = datetime.now().strftime("%d_%m_%Y")
    
    # Create backup filenames
    dump_filename = f"{app_name}_{timestamp}.dump"
    sql_filename = f"{app_name}_{timestamp}.sql"
    dump_path = os.path.join(backup_dir, dump_filename)
    sql_path = os.path.join(backup_dir, sql_filename)
    
    print(f"Creating backup for {app_name}...")
    
    # Create and download the backup using Heroku CLI
    backup_command = f"heroku pg:backups:capture --app {app_name} && heroku pg:backups:download --app {app_name} --output {dump_path}"
    if run_command(backup_command) is None:
        return False
    
    print(f"Backup created successfully: {dump_filename}")
    
    # Convert dump to SQL
    if not convert_dump_to_sql(dump_path, sql_path):
        return False
    
    print(f"Both dump and SQL files are saved for {app_name}")
    return True

def main():
    # Check if Heroku CLI is installed
    if run_command("heroku --version") is None:
        print("Error: Heroku CLI is not installed or not in PATH")
        sys.exit(1)
    
    # Check if pg_restore is installed
    if run_command("pg_restore --version") is None:
        print("Error: pg_restore is not installed or not in PATH")
        sys.exit(1)
    
    # Create backup directory
    backup_dir = create_backup_folder()
    
    # Read app names from file
    try:
        with open("app_names.txt", "r") as file:
            app_names = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: app_names.txt file not found")
        sys.exit(1)
    
    # Process each app
    successful_backups = 0
    failed_backups = 0
    
    for app_name in app_names:
        if backup_heroku_app(app_name, backup_dir):
            successful_backups += 1
        else:
            failed_backups += 1
    
    print("\nBackup Summary:")
    print(f"Total apps processed: {len(app_names)}")
    print(f"Successful backups: {successful_backups}")
    print(f"Failed backups: {failed_backups}")
    print(f"\nBoth dump and SQL backups are stored in: {os.path.abspath(backup_dir)}")

if __name__ == "__main__":
    main() 