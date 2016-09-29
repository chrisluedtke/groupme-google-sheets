# GroupMe CSV Download
This script will export all the data that GroupMe stores about a single group. Once you have the group's CSV, you can use your favorite spreadsheet application or data manager to determine interesting statistics about your group and its users. This is also a convenient way to generate an archive of your group that is easier to search than GroupMe's app.

## How to Use This Script
1. Install Python 3 (this includes the pip installer used to install modules)
2. Use your command line to install necessary modules (json, requests, and pandas)
3. Open 'groupme_download.py' with IDLE
4. Find your group id by <a href="https://dev.groupme.com/bots/new" target="_blank">creating a bot</a> in the group you are interested in. The group id will now appear on the <a href="https://dev.groupme.com/bots" target="_blank">bots page</a>. You can delete the bot once you have the id. Paste your token between the apostrophes in 'groupme_download.py' after "group_id ="
5. Find your personal token on GroupMe's <a href="https://dev.groupme.com/session/new" target="_blank">developers website</a>. Click "Access Token" in the upper right. Paste your token between the apostrophes in 'groupme_download.py' after "token ="
6. At the bottom of 'groupme_download.py' update the directory you would like your CSV to export to.
7. Save the script.
8. Run the script in your command line or terminal. In windows, you would navigate to the directory of the scipt by typing "cd C:\Users\YOUR_USERNAME\Downloads". Run the script by typing "python groupme_download.py".
9. The CSV will now be located in the directory you defined in the last line of the script.
