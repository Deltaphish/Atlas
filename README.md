# Media indexer writen in python
Status: work in progress, will probably not delete all your files( external backups are encouraged)

# Usage:
run "python main.py" to start cli

## Commands:
### scan:
scan tag dir
scans a directory and adds all valid media files into the database with a tag

### scrape:
scrape tag
runs all scraper plugins bound to tag on all media files in the database with that tag

# Uninstall
delete /var/lib/atlas
