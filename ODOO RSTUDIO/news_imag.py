from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from textwrap import wrap

df = pd.DataFrame(data)

# Clean up extra whitespace in the 'body' column
df['body'] = df['body'].str.strip().str.replace(r'\s+', ' ', regex=True)

# Path to the image
image_path = r"C:\Users\freedom\Desktop\sample_background_news.jpg"  # Replace with your image path

# Set the margins
top_margin = 250
bottom_margin = 250
left_margin = 40
right_margin = 280

# Font settings (use your desired font and size)
try:
    font = ImageFont.truetype("arial.ttf", 20)  # Adjust font size as needed
except IOError:
    font = ImageFont.load_default()

# Function to draw wrapped text and handle overflow across multiple images
def draw_wrapped_text_on_image(df, image_path, font, left_margin, right_margin, top_margin, bottom_margin, max_images=5):
    image_counter = 1
    image = Image.open(image_path)
    image_width, image_height = image.size
    drawable_width = image_width - left_margin - right_margin
    drawable_height = image_height - top_margin - bottom_margin
    y_offset = top_margin

    # Function to draw text and return updated y position
    def draw_text(draw, text, position, font, max_width):
        lines = wrap(text, width=int(max_width / font.getlength(' ')))  # Get character width
        x, y = position
        for line in lines:
            draw.text((x, y), line, font=font, fill="black")
            line_height = draw.textbbox((x, y), line, font=font)[3] - draw.textbbox((x, y), line, font=font)[1]
            y += line_height  # Adjust y position for the next line
        return y  # Return updated y position

    draw = ImageDraw.Draw(image)

    # Iterate through the DataFrame and draw text across images
    for index, row in df.iterrows():
        title = row['title']
        body = row['body']
        
        # Draw title
        y_offset = draw_text(draw, title, (left_margin, y_offset), font, drawable_width)
        
        # Draw body
        y_offset = draw_text(draw, body, (left_margin, y_offset), font, drawable_width)
        
        # Check if we need to create a new image
        if y_offset > drawable_height:
            image.save(f"output_image_{image_counter}.jpg")
            image_counter += 1
            if image_counter > max_images:  # Stop after the specified max number of images
                break
            image = Image.open(image_path)  # Start a new image
            draw = ImageDraw.Draw(image)
            y_offset = top_margin  # Reset the y_offset for the new image

        y_offset += 30  # Add space between rows

    # Save the last image
    if image_counter <= max_images:
        image.save(f"output_image_{image_counter}.jpg")

# Call the function to draw text on images
draw_wrapped_text_on_image(df, image_path, font, left_margin, right_margin, top_margin, bottom_margin)
