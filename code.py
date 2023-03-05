import time
import terminalio
import board
from adafruit_matrixportal.matrixportal import MatrixPortal
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.scrolling_label import ScrollingLabel

from adafruit_bitmap_font import bitmap_font
import gc
import re


display = board.DISPLAY

# Set up the weather location and API key
weather_location = "Malmö, SE"
weather_api_key = "YOUR_OPENWEATHERMAP_API_KEY_HERE"

# Set up the texttv URL
texttv_url = "https://texttv.nu/api/get/100?includePlainTextContent=1"

# Set up the display group for the weather forecast
weather_group = displayio.Group()
weather_label = label.Label(terminalio.FONT, color=0xFFFFFF,
                            text="Loading...", x=85, y=30, scale=2, background_tight=True)
weather_group.append(weather_label)
#display.show(weather_label)
""" 
weather_group.append(
    Rect(0, 0, pyportal.graphics.display.width, 30, fill=0x000000))
weather_group.append(weather_label)
 """
font = bitmap_font.load_font("ib16x16u.bdf")
#font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzåäöABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')
# Set up the display group for the scrolling text
text_group = displayio.Group()
text_label = ScrollingLabel(font, color=0xFFFFFF,
                            text="TEXTTVqwertyuiopasdfghjklözxcvbnm,qwertyuiopåasdfghjklcxvbn", scale=4, x=11, y=80, max_characters=40, animate_time=0.2)
text_group.append(text_label)

# Set up the display group for both groups
group = displayio.Group()
group.append(weather_group)
group.append(text_group)
#print(group)
display.show(group)

# Set up the PyPortal Titano
matrixportal = MatrixPortal(status_neopixel = board.NEOPIXEL,
)
# Set up the display
#pyportal.splash.append(group)
#pyportal.show(group)
##pyportal.network.connect()

# Get the weather data from OpenWeatherMap API
"""    try:
    weather_data = pyportal.network.fetch_data("http://api.openweathermap.org/data/2.5/forecast?q=Malmo, SE&appid=4acdd2457856e1ef6c064f1e928ea71e&cnt=8", json_path=[])  # 3 hour forecasts this is cnt*3=24 h
    #print(weather_data[0])
    #weather_label.text = f"{weather_data['name']}: {weather_data['main']['temp']}°C"
    
except (ValueError, RuntimeError) as e:
    weather_label.text = "Error getting weather"

hi = max([item['main']['temp'] for item in weather_data[0]['list']])-273.15
lo = min([item['main']['temp'] for item in weather_data[0]['list']])-273.15
print("hi: %.1f, lo: %.1f" % (hi, lo))

weather_label.text = "%.1f\u00b0C" % (
    float(weather_data[0]['list'][0]['main']['temp'])-273.15)
#WEATHER_LABELS[3].text = "24h H: %.1f\u00b0 L: %.1f\u00b0" % (hi, lo)

desc = weather_data[0]['list'][0]['weather'][0]['description']
desc = desc[0].upper() + desc[1:]
print(desc)
del weather_data
gc.collect()
print(gc.mem_free())
"""
# Get the texttv data
try:

    texttv_response = matrixportal.network.fetch(texttv_url)
    #texttv_response = pyportal.network.requests.get(texttv_url)
    texttv_data = texttv_response.json()
    #print(texttv_data[0]["content_plain"])
    # Concatenate the strings and replace newlines
    content_plain = ''.join(texttv_data[0]["content_plain"]).replace('\n', '')
    del texttv_data
    gc.collect()
    
    # Replace sequences of whitespace with a single space
    content_plain = re.sub(r'\s+', ' ', content_plain)
    #print(content_plain)
    content_plain = content_plain.replace("Inrikes", "").replace(
        "Utrikes", "").replace("Innehåll", "").strip(" *")
    # Remove three-digit numbers and spaces
    content_plain = re.sub(r'((^|\s)\d\d\d)(\s|$)', ' ** ', content_plain)
    # Remove three-digit numbers and following f
    content_plain = re.sub(r'((^|\s)\d\d\df?)(\s|$)', '', content_plain)
    #print(content_plain)
    """ 
    content_plain = content_plain.replace("å", "\u00E5")
    content_plain = content_plain.replace("ä", "\u00E4")
    content_plain = content_plain.replace("ö", "\u00F6") 
    """
    print("ersatt", content_plain)
    text_label.full_text = content_plain
    print("text_label.text", text_label.text)

except Exception as e:
    text_label.text = "Error getting TextTV data"
    print("error", e)
#text_label.scroll_speed = 0.05
#text_label.scroll_delay = 0.05
#text_label.scroll_style = label.ScrollStyle.SINGLE
# Wait a bit before refreshing the display

while True:
    text_label.update()

""" content_plain = "SVT Täxt tårsdög 02 mar 2023                                                                                                                                                                                                               Nö skottlossning i Farsta i Stockholm                                           Skott mot lägenhetsdörr * Två gripna                     106                                                                    von der Leyen besöker                   president Biden i USA                            133                                                            Flicka allvarligt skadad i knivattack                                           Göteborgspolisen har gripit misstänkt                    110                                                            Jazzikonen Wayne Shorter är död - 150                                             Februari: Milt och rätt blåsigt 417f"
 """