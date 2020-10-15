# University Of Cambridge COVID-19 Dashboard

A simple dashboard for tracking weekly case and testing data from the University of Cambridge asymptomatic and symptomatic testing programmes for students and staff.
- Data source: https://www.cam.ac.uk/coronavirus/stay-safe-cambridge-uni/data-from-covid-19-testing-service
- More information: https://www.cam.ac.uk/coronavirus/stay-safe-cambridge-uni/asymptomatic-covid-19-screening-programme

**Note:** this is not an official University dashboard. It is a student project.

## Development

Requires Python 3.7+.

```bash
git clone https://github.com/fpervaiz/UniversityOfCambridge-COVID-19-Dashboard.git
cd UniversityOfCambridge-COVID-19-Dashboard
py -3 -m venv .venv
pip install -r requirements.txt
set FLASK_ENV=development
python app.py
```