from sklearn.cluster import KMeans
import numpy as np
from termcolor import colored
import argparse
import csv
import json 
from PIL import Image
import matplotlib.pyplot as plt

def extract_colors(image_path, num_colors):
    image = Image.open(image_path)
    image = image.resize((150, 150))  # reduce size to speed up processing
    image_np = np.array(image)
    flattened = image_np.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=num_colors)
    labels = kmeans.fit_predict(flattened)
    
    colors = kmeans.cluster_centers_
    return colors

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def plot_colors(colors, filename):
    fig, ax = plt.subplots(1, 1, figsize=(12, 7.2), dpi=100)
    plt.axis('off')
    plt.imshow([colors.astype(int)], aspect='auto')

    hex_colors = [rgb_to_hex(color) for color in colors]
    x_positions = np.linspace(start=0, stop=1, num=len(hex_colors), endpoint=False)
    for hex_color, pos in zip(hex_colors, x_positions):
        plt.text(pos, 0.5, hex_color, color='white' if np.mean(colors) < 128 else 'black', 
                 horizontalalignment='left', verticalalignment='top', 
                 transform=ax.transAxes, rotation='vertical', fontsize=40)

    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(filename, bbox_inches=extent)
    

def save_colors_to_file(colors, txt_filename, json_filename):
    hex_colors = [rgb_to_hex(color) for color in colors]

    with open(txt_filename+".txt", 'w') as f:
        for color in hex_colors:
            f.write(color + '\n')

    with open(json_filename+".json", 'w') as f:
        json.dump(hex_colors, f)


def main():
    parser = argparse.ArgumentParser(description='Extract dominant colors from an image.')
    parser.add_argument('-p', type=str, nargs='+', help='The path to the image file.')
    parser.add_argument('-n', type=int, default=5, help='The number of colors to extract.')
    parser.add_argument('-o', type=str, default='colors_palte', help='The path to  output file.')

    args = parser.parse_args()

    for image_path in args.p:
        try:
            colors = extract_colors(image_path, args.n)
            txt_filename = f'{image_path}_colors.txt'
            json_filename = f'{image_path}_colors.json'
            # save_colors_to_file(colors, txt_filename, json_filename)
            plot_filename = f'{image_path}_color_palette.png'
            plot_colors(colors, plot_filename)
            print(f"Color palette saved as '{plot_filename}'")
            # print(f"Colors saved as '{txt_filename}' and '{json_filename}'")
        except Exception:
            print(colored(f"Image {image_path} color not extracted", 'red'))
            pass

if __name__ == '__main__':
    main()

