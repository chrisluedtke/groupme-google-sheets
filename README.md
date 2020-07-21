# GroupMe Export to Google Sheets

This script retrieves all GroupMe message data from a group chat and writes it to a Google sheet.

### Local Setup
1. Copy `.env.sample` to `.env` and fill in the variables.

    ```
    cp .env.sample .env
    ```

    `GROUPME_TOKEN` is found on [GroupMe's developers website](https://dev.groupme.com/session/new). Click "Access Token" (upper right).

2. Save Google Sheets API credentials to `credendials.json`. You will also need to grant edit permissions to this identity. [This article](https://towardsdatascience.com/python-pandas-dataframe-to-google-sheets-for-tableau-desktop-live-cc1f86982bca) provides a good walkthrough.
3. Create and activate a virtual environment
    ```
    python -m venv env
    source env/bin/activate
    ```
4. Install dependencies
    ```
    pip install -r requirements.txt
    ```
5. Run script
    ```
    python groupme.py
    ```
