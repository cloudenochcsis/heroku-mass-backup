# heroku-mass-backup

A Python tool to automate mass backups of Heroku Postgres databases for multiple apps. For each app, the tool:
- Captures and downloads a Heroku Postgres backup (`.dump` file)
- Converts the backup to a plain SQL file (`.sql`)
- Stores both files locally in a `heroku_backups` directory

## Features
- Backs up all Heroku apps listed in `app_names.txt`
- Keeps both the original Heroku `.dump` and a `.sql` export for each app
- Timestamped filenames for easy tracking
- Summary of successful and failed backups

## Requirements
- Python 3.x
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (must be installed and logged in)
- [PostgreSQL tools](https://www.postgresql.org/download/) (for `pg_restore`)

## Setup
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd heroku-mass-backup
   ```
2. Ensure you have the Heroku CLI and PostgreSQL tools installed and available in your PATH.
3. Log in to Heroku CLI:
   ```bash
   heroku login
   ```
4. Create a file named `app_names.txt` in the project directory, listing one Heroku app name per line.

## Usage
Run the backup script:
```bash
python heroku_backup.py
```

- All backups will be saved in the `heroku_backups` directory.
- Each app will have two files: `appname_DD_MM_YYYY.dump` and `appname_DD_MM_YYYY.sql`.
- The script will print a summary of the backup process.

## Example
```
app_names.txt:
my-app-1
my-app-2
```

After running the script, you will find:
```
heroku_backups/
  my-app-1_12_05_2024.dump
  my-app-1_12_05_2024.sql
  my-app-2_12_05_2024.dump
  my-app-2_12_05_2024.sql
```

## Notes
- The script assumes each app has a Heroku Postgres database add-on.
- If an app does not have a database or the backup fails, the script will continue to the next app and report the failure at the end.

## License
MIT 