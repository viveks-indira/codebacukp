import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pywhatkit as kit
from PIL import Image, ImageDraw, ImageFont

class MarketScraper:
    def _init_(self):
        self.url = self.construct_url()
        self.soup = None
        self.data = []
        self.df = pd.DataFrame()  # Initialize an empty DataFrame

    def construct_url(self):
        # today = datetime.now()
        # month = 'oct' if today.strftime("%b").lower() == 'oct' else today.strftime("%b").lower()
        # formatted_date = f"{month}-{today.day}"
        # print(f"Formatted Date: {formatted_date}")
        today = datetime.now()
        # Get the first three characters of the current month in lowercase
        month = today.strftime("%B")[:3].lower()
        formatted_date = f"{month}-{today.day}"
        print(f"Formatted Date: {formatted_date}")

        url = f"https://www.ndtvprofit.com/markets/stock-market-today-all-you-need-to-know-going-into-trade-on-{formatted_date}"
        print(f"URL: {url}")
        return url

    def fetch_html(self):
        time.sleep(5)  # Pause to prevent overwhelming the server
        response = requests.get(self.url)

        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Failed to retrieve data from {self.url}, Status Code: {response.status_code}")

    def parse_html(self):
        if not self.soup:
            raise Exception("HTML content not fetched. Call fetch_html() first.")

        ul_elements = self.soup.find_all('ul')
        x, y, z = 0, 0, 0

        for ul in ul_elements:
            li_elements = ul.find_all('li')
            for li in li_elements:
                p_elements = li.find_all('p')
                for p in p_elements:
                    content_text = p.get_text(separator="\n").strip()
                    self.data.append({
                        'content': content_text,
                        'para': z,
                        'li': y,
                        'ul': x
                    })
                    z += 1
                y += 1
            x += 1

    def create_dataframe(self):
        self.df = pd.DataFrame(self.data)
        self.df = self.df[self.df.ul == 2]  # Filtering specific <ul> elements
        self.df['title'] = self.df['content'].str.split(':').str[0].str.upper()
        self.df['body'] = self.df['content'].str.split(':').str[1].fillna('')  # Handle missing body
        return self.df

    def format_json(self):
        #print(self.df.to_json())
        formatted_text = ""
        for index, row in self.df.iterrows():
            formatted_text += f"{row['title']}: {row['body']}\n\n"
        return formatted_text.strip()

    def send_whatsapp_message(self, phone_number, message, image_paths=None):
     #   kit.sendwhatmsg_instantly(phone_number, message, wait_time=30)
     #   print(f"Message sent to {phone_number}")
         current_date = datetime.now().strftime("%B %d, %Y")  # Format the date as needed

         # Print the number of images to send
         if image_paths:
             print(f"Sending {len(image_paths)} images to {phone_number}...")

             for index, image_path in enumerate(image_paths):
                 try:
                     kit.sendwhats_image(
                         phone_number,
                         image_path,
                         f"{current_date} Market Update {index + 1}/{len(image_paths)}",
                         wait_time=25  # Increase wait time for better reliability
                     )
                     time.sleep(10)  # Ensure a delay between image sends
                     print(f"Image {index + 1} sent to {phone_number}: {image_path}")
                 except Exception as e:
                     print(f"Failed to send image {image_path}: {e}")
         else:
             print("No images to send.")

    def draw_wrapped_text_on_image(self, image_path, font_path="arial.ttf", max_images=2, line_spacing=5):
        df = self.df
        df['body'] = df['body'].str.strip().str.replace(r'\s+', ' ', regex=True)

        # Set the margins
        top_margin = 380  # Increased top margin for better readability
        bottom_margin = 150  # Increased bottom margin to prevent overflow
        left_margin = 50  # Left margin adjusted
        right_margin = 150  # Right margin adjusted

        # Page Area length and width to be text print
        image_counter = 1
        image_paths = []  # List to hold image paths
        image = Image.open(image_path)
        image_width, image_height = image.size
        drawable_width = image_width - left_margin - right_margin + 100
        drawable_height = image_height - top_margin - bottom_margin + 350

        y_offset = top_margin

        # Get current date
        current_date = datetime.now().strftime("%B %d, %Y")  # Format the date as needed
        date_position = (750, 280)  # Position for the date

        # Font settings (use your desired font and size)
        try:
            title_font = ImageFont.truetype("arialbd.ttf", 24)  # Title font
            body_font = ImageFont.truetype(font_path, 22)  # Body font
            date_font = ImageFont.truetype(font_path, 22)  # Date font
        except IOError:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            date_font = ImageFont.load_default()

        def draw_text(draw, text, position, font, max_width, text_type):
            """Draw left-aligned text on the image and return the updated y-offset."""
            x, y = position
            lines = []
            words = text.split()
            current_line = ""

            # Define color based on text type
            color = "black"  # Default color for body text
            if text_type == "title":
                color = (37, 164, 138)  # Greenish color for title
                font = title_font  # Use the title font

            else:
                font = body_font  # Use the body font

            # Split text into lines that fit within the drawable width
            for word in words:
                test_line = current_line + word + " "
                test_line_width = draw.textlength(test_line, font=font)

                if test_line_width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "

            if current_line:
                lines.append(current_line.strip())

            # Draw each line
            for line in lines:
                draw.text((x, y), line, font=font, fill=color)
                line_bbox = draw.textbbox((x, y), line, font=font)
                line_height = line_bbox[3] - line_bbox[1]
                y += line_height + line_spacing

            return y  # Return updated y position

        # Function to draw justified text for the body with special handling for the last line
        def draw_text_justified(draw, text, position, font, max_width):
            """Draw justified text on the image, handling the last line as start-aligned (left-aligned)."""
            x, y = position
            words = text.replace('\n', ' ').split()  # Replace newlines with spaces and split into words
            lines = []
            current_line = []
            current_line_width = 0

            # Split text into lines that fit within the drawable width
            for word in words:
                word_width = draw.textlength(word + " ", font=font)
                if current_line_width + word_width <= max_width:
                    current_line.append(word)
                    current_line_width += word_width
                else:
                    lines.append((current_line, current_line_width))
                    current_line = [word]
                    current_line_width = word_width

            if current_line:
                lines.append((current_line, current_line_width))

            # Draw each line with proper justification
            for i, (line, line_width) in enumerate(lines):
                # If this is the last line or the line has only one word, left-align it
                if i == len(lines) - 1 or len(line) == 1:
                    # Left-align the text (start-aligned)
                    draw.text((x, y), " ".join(line), font=font, fill="black")
                else:
                    # Justify the text (distribute space between words)
                    total_spaces = len(line) - 1
                    space_width = (max_width - line_width) / total_spaces if total_spaces > 0 else 0
                    x_offset = x
                    for word in line:
                        draw.text((x_offset, y), word, font=font, fill="black")
                        word_width = draw.textlength(word + " ", font=font)
                        x_offset += word_width + space_width

                line_bbox = draw.textbbox((x, y), " ".join(line), font=font)
                line_height = line_bbox[3] - line_bbox[1]
                y += line_height + line_spacing

            return y  # Return updated y position

        draw = ImageDraw.Draw(image)

        print("Starting to draw text on the image...")
        # Iterate through the DataFrame and draw text across images
        for index, row in df.iterrows():
            title = row['title']
            body = row['body']

            # Draw title without justification (left-aligned)
            y_offset = draw_text(draw, title, (left_margin, y_offset), title_font, drawable_width, "title")
            y_offset += line_spacing  # Add space after title

            y_offset += 10
            # Draw body with justification
            y_offset = draw_text_justified(draw, body, (left_margin, y_offset), body_font, drawable_width)

            # Draw separator line
            y_offset += 10  # Add space before separator line
            # Draw a horizontal line
            draw.line([(left_margin, y_offset), (drawable_width + left_margin, y_offset)], fill="black", width=1)
            y_offset += 15  # Add space after the line

            # Check if we need to create a new image
            if y_offset > drawable_height:
                #image.save(f"output_image_{image_counter}.jpg")
                image.save(f"C:/Users/freedom/Desktop/StocksDailyNew/output_image_{image_counter}.jpg")
                image_paths.append(f"output_image_{image_counter}.jpg")  # Add the image path to the list
                print(f"Image {image_counter} created successfully!")
                image_counter += 1
                if image_counter > max_images:  # Stop after the specified max number of images
                    break
                image = Image.open(image_path)  # Start a new image
                draw = ImageDraw.Draw(image)
                y_offset = top_margin  # Reset the y_offset for the new image

                # Draw the date on the image
            draw.text(date_position, current_date, font=date_font, fill="white", weight="5")  # Draw date
            y_offset += line_spacing  # Add space between rows

        # Save the last image if it hasn't been saved
        if image_counter <= max_images:
            final_image_path = f"output_image_{image_counter}.jpg"
            image.save(final_image_path)
            image_paths.append(final_image_path)  # Add the last image path to the list
            print(f"Image {image_counter} created successfully!")

        return image_paths  # Return the list of image paths

    def scrape(self):
        self.fetch_html()
        self.parse_html()
        self.create_dataframe()
        formatted_text = self.format_json()
        #print(formatted_text)

        # Draw the images and get their paths
        image_paths = self.draw_wrapped_text_on_image(
            r"C:/Users/freedom/Desktop/StocksDailyNew/sample_background_news.jpeg")

        print("Image paths:", image_paths)
        # Send message and images
        self.send_whatsapp_message("+919977769297", formatted_text, image_paths)


if _name_ == "_main_":
    scraper = MarketScraper()
    scraper.scrape()