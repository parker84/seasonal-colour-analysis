from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os
from tqdm import tqdm
from decouple import config
import logging, coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'), logger=logger)

def extract_hex_codes(image_path, num_colors):
    # Load image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Resize image to reduce processing time (optional)
    # img = img.resize((100, 100))

    # Convert image to numpy array
    img_array = np.array(img)
    
    # Reshape array to 2D array (rows represent pixels)
    img_flat = img_array.reshape(-1, 3)
    
    # Use K-means clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(img_flat)
    
    # Get the RGB values of the cluster centers
    cluster_centers = kmeans.cluster_centers_
    
    # Convert RGB values to hexadecimal format
    hex_codes = ['#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b)) for r, g, b in cluster_centers]
    
    return hex_codes

if __name__ == '__main__':
    # Example usage
    for fname in tqdm(os.listdir('./data')):
        if fname.endswith('.png'):
            logger.info(f"Processing {fname}")
            image_path = os.path.join('./data', fname)
            num_colors = 30  # Number of dominant colors to extract
            hex_codes = extract_hex_codes(image_path, num_colors)
            logger.info(f"Extracted Hex Codes: {hex_codes} from {fname} ✅")