import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone, timedelta
import pytz
import time

# GET TIME FROM FILE
def get_modification_time(input_path):
    # Get the modification time of the input image file
    modification_time = os.path.getmtime(input_path)
    utc_time = datetime.utcfromtimestamp(modification_time)
    # Format the Chicago time
    chicago_timezone = pytz.timezone('America/Chicago')
    chicago_time = utc_time.replace(tzinfo=timezone.utc).astimezone(chicago_timezone)
    return chicago_time.strftime("%m-%d-%Y %H:%M:%S")

# ADD TIMESTAMP ON TOP OF THE PNG FILE
def add_timestamp_to_image(input_path, output_path):
    # Load the image
    img = plt.imread(input_path)
    # Get creation time of the input image file
    creation_time = get_modification_time(input_path)
    # Add timestamp to the image
    plt.imshow(img)
    plt.text(10, -150, f'Modified at: {creation_time}', color='white', fontsize=12,
             bbox=dict(facecolor='black', alpha=0.7), verticalalignment='top')
    # Remove axis
    plt.axis('off')
    # Save the modified image
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

# EXECUTE CONTINUOUS PLOT TRANSFERING
if __name__ == "__main__":

    # Iterate over each file in the directory
    directory = "/home/nfs/minerva/dqmtest_cpernas/SL7_testing/gmbrowser/plots/tmp/"

    while True:
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                # Input and output paths for each file
                input_path = os.path.join(directory, filename)
                output_path = os.path.join("/data/grafana/Mx2/", os.path.basename(input_path))
                
                # Add timestamp to the image
                add_timestamp_to_image(input_path, output_path)
        
        # Add timestamp to the image
        add_timestamp_to_image(input_path, output_path)
        # Sleep for 5 minutes
        time.sleep(5 * 60)