# a programme to display today's weather and tomorrow
# on the inky_display using Lukas Kubis's Python wrapper
# for the Dark Sky API https://github.com/lukaskubis/darkskylib 

import glob
print("Initializing inky...")
from inky import InkyPHAT
print("Initializing PIL...")
from PIL import Image, ImageFont, ImageDraw
import datetime
from datetime import date, timedelta
from darksky import forecast
import textwrap
print("Initializing matplotlib...")
from matplotlib import pyplot as plt
print("Other init...")
from math import ceil, floor
import secrets
import calendar_reader
# set the colour of the phat: black, red or yellow
inky_display = InkyPHAT('yellow')
BLACK = inky_display.BLACK
YELLOW = inky_display.YELLOW
WIDTH = inky_display.WIDTH

# set lat/long for location
LOCATION = (40.650002, -73.949997) #put your longitude and latittude here in decimal degrees
UNITS = 'us' #specify the units you want your results in here, see the Dark Sky API docs page for details 

# set Darksky API Key
APIKEY= secrets.darksky_apikey # put your Dark Sky API key here. Get one at https://darksky.net/dev
calendar_agenda = calendar_reader.get_events()
# Get data from DarkSky
print("Weather forecast...")
with forecast(APIKEY, *LOCATION, units=UNITS) as location:
    # print(location)
    # today
    currentTemp = location['currently']['temperature']
    upcoming_conditions = location['minutely']['summary']
    relativeHumidity = location['currently']['humidity']
    highTemp = location['daily']['data'][0]['temperatureHigh']
    lowTemp = location['daily']['data'][0]['temperatureLow']
    iconDesc = location['currently']['icon']
  
    # tomorrow 
    summary2 = location['daily']['data'][1]['summary']
    iconDesc2 = location['daily']['data'][1]['icon']
    highTemp2 = location['daily']['data'][1]['temperatureHigh']
    lowTemp2 = location['daily']['data'][1]['temperatureLow']

    hourly_times = [datetime.datetime.fromtimestamp(fc.time) for fc in location.hourly.data[:16]]
    hourly_temps = [fc.temperature for fc in location.hourly.data[:16]]
    hourly_precip = [fc.precipProbability for fc in location.hourly.data[:16]]
print("Drawing...")
# print(hourly_first_time, hourly_temps, hourly_precip)
min_temp = 5 * floor(min(hourly_temps) / 5.)
max_temp = 5 * ceil(max(hourly_temps) / 5.)
adjusted_temps = [(t - min_temp) / (max_temp - min_temp) for t in hourly_temps]
plt.plot(range(16),adjusted_temps, 'r', linewidth=11)
plt.plot(range(16),hourly_precip, 'k', linewidth=11)
plt.axis('off')
plt.ylim((-0.02,1.02))
plt.savefig('weather.png', bbox_inches="tight")
weather_image = Image.open('weather.png')
# print(min_temp, max_temp)


temp = '{0:.0f}'.format(currentTemp) + '°'

# Create a new blank image, img, of type P 
# that is the width and height of the Inky pHAT display,
# then create a drawing canvas, draw, to which we can draw text and graphics
img = Image.new('P', (212, 104))
draw = ImageDraw.Draw(img)

# import the fonts and set sizes
tempFont = ImageFont.truetype('fonts/Aller_Bd.ttf', 22)
dayFont = ImageFont.truetype('fonts/Roboto-Black.ttf', 18)
dateFont = ImageFont.truetype('fonts/Roboto-Bold.ttf', 14)
font = ImageFont.truetype('fonts/ElecSign.ttf', 10)
smallFont = ImageFont.truetype('fonts/ElecSign.ttf', 8)
smallestFont = ImageFont.truetype('fonts/ElecSign.ttf', 7)

# define weekday text
weekday = date.today()
day_Name = date.strftime(weekday, '%a %-d')
# day_month_year = date.strftime(weekday, '%-d %B %y')

weekday2 = datetime.date.today() + datetime.timedelta(days=1)
day2 = date.strftime(weekday2, '%A')

draw.line((117,0,117,200),BLACK,1)

draw.text((3, 3), day_Name, BLACK, dateFont)


# draw the current summary and conditions on the left side of the screen
# draw.text((3, 60), currentCondFormatted, BLACK, smallFont)
weather_image.thumbnail((100,120))

img.paste(weather_image, (8,20))
for pct in (0,25,50,75,100):
    st = f'{pct}%'
    hpos = 111 - 3 * len(st)
    vpos = int(round(90 - .69 * pct))
    draw.text((hpos,vpos), st, BLACK, smallestFont)
for tmp in range(min_temp, max_temp+1,5):
    pct = (tmp - min_temp) / (max_temp - min_temp)
    st = str(tmp)
    hpos = 10 - 3 * len(st)
    vpos = int(round(90 - 69 * pct))
    draw.text((hpos,vpos), st, YELLOW, smallestFont)
# draw.text((97,96),'21',BLACK,smallestFont)
for idx in range(0,16,3):
    timestamp = hourly_times[idx].hour
    st = str(timestamp)
    pct = idx / 15.
    hpos = 12 + 84 * pct + 3*(len(st) == 1)
    vpos = 96
    draw.text((hpos,vpos), st, BLACK, smallFont)


draw.text((80, -2), temp, BLACK, tempFont)

# # draw tomorrow's forecast in lower right box
# draw.text((125, 55), day2, BLACK, font)
# draw.text((125, 66), tempsDay2, BLACK, smallFont)
# draw.text((125, 77), summary2Formatted, BLACK, smallestFont)
draw.text((123,0),"Agenda",BLACK,dateFont)
curr_height = 20
for time,event in calendar_agenda:
    newX = 123
    width = 17
    if time:
        draw.text((118 + 5 * (5-len(time)),curr_height),time,YELLOW,smallFont)
        newX = 146
        width = 13
    formattedEvent = textwrap.fill(event, width, break_long_words=True,max_lines=2)
    lines = formattedEvent.count('\n') + 1
    draw.text((newX,curr_height),formattedEvent,BLACK,smallFont)
    curr_height += 11 * lines
# prepare to draw the icon on the upper right side of the screen
# Dictionary to store the icons
icons = {}

# build the dictionary 'icons'
for icon in glob.glob('weather-icons/icon-*.png'):
    # format the file name down to the text we need
    # example: 'icon-fog.png' becomes 'fog'
    # and gets put in the libary 
    icon_name = icon.split('icon-')[1].replace('.png', '')
    icon_image = Image.open(icon)
    icon_image.thumbnail((30,30))
    icons[icon_name] = icon_image

# Draw the current weather icon top in top right
# print(f'Icon is {iconDesc}, icons are {icons}')
if iconDesc is not None:
    img.paste(icons[iconDesc], (49, 1))        
else:
    draw.text((49, 1), '?', YELLOW, dayFont)
print("Displaying...")
img.save("preview.png","PNG")
# set up the image to push it
inky_display.set_image(img)

# push it all to the screen
inky_display.show()
