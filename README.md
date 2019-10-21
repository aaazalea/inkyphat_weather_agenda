# inkyphat_weather_agenda
Python3 code to display current and near-term weather conditions as well as an agenda for the day on an Pimoroni Inky pHAT eInk screen Using the [Dark Sky API](https://darksky.net/dev/) and Lukas Kubis's Python wrapper [darkskylib](https://github.com/lukaskubis/darkskylib/). My installation is on a Raspberry Pi Zero W running headless on my desk. 

## Acknowledgements
- This is based on https://github.com/ldritsas/inkyphat_weather

## Dependencies and requirements
- You will need to get an API key from Dark Sky and know your longitude and latitude (`secrets.py`)
- You will need API info from google calendar (`credentials.json`)
- `pip3 install -r requirements.txt`

## Tips
- Make sure your raspi is on the right timezone!!
- On your own system you may need to adjust the loction of the resource files (the fonts and icons, depending on where you put them). I found that I needed absolute links n the code to make it work properly.
- I suggest creating a cron job that refreshes the screen every 15 minutes with new data. This is a lot simpler than it sounds, check [here](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/) for guidance. I did not see any benefit to more frequent requests.

## Example
![Image](inky-pHAT.png)

## License

GNU General Public License v3.0
