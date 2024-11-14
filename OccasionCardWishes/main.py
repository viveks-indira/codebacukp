from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Load the Excel file
df = pd.read_excel(r"E:\OccasionCardWishes\sampledata.xlsx")  # Ensure the file is .xlsx and has the correct columns

# Load the background image
img_path = r"E:\OccasionCardWishes\cardsample.jpg"  # Replace with your image path
img = Image.open(img_path)

# Set up font and size
font_path = "arialbd.ttf"  # Change to the path of your font file
font_size = 32
font = ImageFont.truetype(font_path, font_size)

# Container dimensions (reduced height)
container_width = 1356
container_height = 200  # Adjusted container height
container_x = 0  # Left position of container
container_y = 1000  # Top position of container

# Create a drawing context
draw = ImageDraw.Draw(img)

# Loop over each row in the DataFrame
for index, row in df.iterrows():
    # Draw the white container rectangle
    draw.rectangle(
        [(container_x, container_y), (container_x + container_width, container_y + container_height)],
        fill="white"
    )

    # Center-align each text element within the container
    text_y = container_y + 20
    texts = [("Name", str(row['Name'])), ("Company", str(row['Company'])), ("Member", str(row['Member']))]

    for label, text in texts:
        # Calculate text width to center-align using textbbox
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = container_x + (container_width - text_width) / 2  # Center horizontally within the container

        # Set color based on the field
        text_color = "#178f86" if label == "Company" else "black"

        # Draw text
        draw.text((text_x, text_y), text, fill=text_color, font=font)
        text_y += 40  # Move down for the next line of text

    # Save each modified image with a unique name
    img.save(f"E:\\OccasionCardWishes\\output_image_{index + 1}.jpg")

print("Images with centered text in container created successfully.")