set URL=http://localhost:5000/
start "" "chrome.exe" "%URL%"
poetry run flask --debug run