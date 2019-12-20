# whatsapp_to_slack
script to export whatsapp conversations into slack threads

updated the script from https://gist.github.com/onekiloparsec/a7df8dd1f2babd9740e8 to include recent format changes

How to use:

1) Go to any whatsapp chat => More => Export chat => Save to Drive (or other options)

2) Pass downloaded_file to the command...
python3 parse.py [-h] [-c chanel_name] [-o slack_data.txt] downloaded_file.txt

3) Go to https://<your_company>.slack.com/services/import/csv & upload slack_data.txt & follow on screen instructions.

Keywords:

whatsapp to slack
export from whatsapp
import to slack
whatsapp group to slack channel 

