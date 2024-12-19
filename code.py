import time
import re
from adafruit_matrixportal.matrixportal import MatrixPortal
import board
import random
from adafruit_bitmap_font import bitmap_font

# Initialize MatrixPortal
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL)

# Add text labels
matrixportal.add_text(  # Header text
    text_font="lib/font_free_mono_12/font.pcf",
    text_position=(0, 1),
    text_anchor_point=(0, 1),
    scrolling=False,
)
matrixportal.add_text(  # Scrolling text
    text_font="lib/font_free_sans_12/font.pcf",
    text_position=(0, 1),
    text_anchor_point=(0, 0),
    scrolling=True,
)

# Set up the texttv URL
texttv_url = "https://texttv.nu/api/get/100?includePlainTextContent=1"

# Function to set text color based on the number
def set_text_color_based_on_number(text, index):
    # Manually check for three-digit numbers
    words = text.split()
    for word in words:
        if word.isdigit() and len(word) == 3:
            number = int(word)
            if number >= 130:
                matrixportal.set_text_color(0xFFFF00, index)  # Yellow
            else:
                matrixportal.set_text_color(0x008080, index)  # Teal
            return
    matrixportal.set_text_color(0xFFFFFF, index)  # Default to white if no number is found

# Get the texttv data
try:
    texttv_response = matrixportal.network.fetch(texttv_url)
    texttv_data = texttv_response.json()
    content = texttv_data[0]["content_plain"][0]
    print("response", content)

    # Remove everything up to and including the year
    remaining_text = re.sub(r'.*?20[2-3]\d', '', content, 1)

    # Step 2: Manually split remaining content by three-digit numbers
    segments = []
    current_segment = []
    temp_segment = ""

    # Loop over each character to manually detect where to split based on three-digit numbers
    for char in remaining_text:
        temp_segment += char

        # Detect when a three-digit number is found
        if len(temp_segment) >= 3 and temp_segment[-3:].isdigit():
            if temp_segment[-3:] == "000":
                continue  # Skip splitting at "000"
            # Check if it's a three-digit number (with optional 'f')
            if temp_segment[-3:].isdigit() or (len(temp_segment) >= 4 and temp_segment[-4] == 'f' and temp_segment[-3:].isdigit()):
                if current_segment:
                    segments.append(' '.join(current_segment).strip())
                current_segment = [temp_segment.strip()]
                temp_segment = ""
        elif char == "\n":
            # Avoid splitting on newlines or other unwanted characters
            continue

    if temp_segment.strip():
        current_segment.append(temp_segment.strip())

    if current_segment:
        segments.append(' '.join(current_segment).strip())

    # Step 3: Remove everything after "Inrikes", "Utrikes", or "Innehåll"
    cleaned_segments = []
    for seg in segments:
        if "Inrikes" in seg or "Utrikes" in seg or "Innehåll" in seg:
            break
        # Normalize spaces
        words = seg.split()
        cleaned_words = []
        for word in words:
            cleaned_words.append(word)
        cleaned_segment = ' '.join(cleaned_words).replace(" - ", " ").strip()
        cleaned_segments.append(cleaned_segment)

    # Final result list
    result_list = cleaned_segments
    print("reslist", result_list)

except Exception as e:
    print("Error:", e)
    result_list = ["Pauliskolan", "Teknikprogrammet", "Error fetching data"]

# Main loop
current_index = 0
#matrixportal.set_text(result_list[current_index], 1)
#set_text_color_based_on_number(result_list[current_index], 1)
# Fetch and set the local time
matrixportal.get_local_time()
last_update_time = time.monotonic()
now= time.localtime()
# Display the header text on the matrix portal


while True:
    # Set a random color for the header text
    random_color = random.randint(0, 0xFFFFFF)
    matrixportal.set_text_color(random_color, 0)
    header_text = f"{now.tm_hour:02d}:{now.tm_min:02d} {now.tm_mday}{'a' if now.tm_mday in [1, 2, 21, 22] else 'e'}"
    matrixportal.set_text(header_text, 0)
    
    # Scroll the non-header text
    matrixportal.set_text(result_list[current_index], 1)
    set_text_color_based_on_number(result_list[current_index], 1)
    matrixportal.scroll_text()

    current_index += 1
    if current_index >= len(result_list):
        current_index = 0  # Reset to the 

    # Update the scrolling text after it has scrolled through completely
    current_time = time.monotonic()
    if current_time - last_update_time > 600: #update texttv and weather
        last_update_time = current_time

    # Perform other tasks here
    # ...
