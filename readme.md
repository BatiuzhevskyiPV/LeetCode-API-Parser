# LeetCode Leaderboard Parser

This is an asynchronous Python script that fetches the global leaderboard data with LeetCode API
and exports it to an Excel file.

# Project Structure

* **main.py** - main script to run  
* **config.py** - API headers(optional) and GraphQL query  
* **models.py** - Pydantic models for API response validation
* **requirements.txt** - basically requirements  
* **results.xlsx** - output Excel file

# Install dependencies

`pip install -r requirements.txt`

# Run the script

`python main.py`

# Tech

_♦ Python 3.12_  
_♦ Pydantic data validation_  
_♦ Client-friendly Rich CLI_