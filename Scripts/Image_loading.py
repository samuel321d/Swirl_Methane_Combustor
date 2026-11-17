# This file reads and loads a spe image into an array

# Libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import spe_loader as sl
import spe2py
from pathlib import Path
from spexread import read_spe_file

# Script Path 
path = Path.cwd()
# Path of folder containing images
combustion_images_folder = path / "Scripts" / "Data" / "Combustion"

folders = [
    f for f in combustion_images_folder.iterdir()
    if f.is_dir()
]

print("Combustion images:", [f.name for f in folders])

# Function to load an image
def open_image(folder_path):
    # This function receives as input a desired path in where the image is located and extracts the 50x512x512 frames
    folder_path = Path(folder_path)

    files = list(folder_path.glob("*.SPE"))

    if not files:
        raise FileNotFoundError(f"No SPE files found in {folder_path}")

    return read_spe_file(files[0])

# Background Frames
RR = open_image(folders[5])
print(RR)
print(RR.data_vars)

images_rr = RR["ROI 0"]

# A mean of the background is going to be calculated

BG_prom = images_rr.mean(dim = "frame")

plt.figure(figsize = (10,6))
plt.imshow(BG_prom, cmap = "turbo", origin = "lower")
plt.colorbar(label = "Intensity")
plt.xlabel("x pixels")
plt.ylabel("y pixels")
plt.title("Average intensity from BackGround frames")
plt.show()


# REFERENCE FRAMES

ref = open_image(folders[-1])
images_ref = ref["ROI 0"]
images_ref_new = images_ref - BG_prom

ref_prom = images_ref_new.mean(dim = "frame")

plt.figure(figsize = (10,6))
plt.imshow(ref_prom, cmap = "gray", origin = "lower")
plt.colorbar(label = "Intensity")
plt.xlabel("x pixels")
plt.ylabel("y pixels")
plt.title("Average intensity from BackGround frames")
# plt.show()

cut_ref_prom = ref_prom[50:200, 50:200]

plt.figure(figsize = (10,6))
plt.imshow(cut_ref_prom, cmap = "gray", origin = "lower")
plt.colorbar(label = "Intensity")
plt.xlabel("x pixels")
plt.ylabel("y pixels")
plt.title("Average intensity from BackGround frames")
plt.show()



"""



fig, ax = plt.subplots(2, 3, figsize=(14, 8))

frames = [0, 10, 20, 30, 40, 49]

for i, a in enumerate(ax.flat):
    a.imshow(images_rr.isel(frame=frames[i]), cmap="inferno", origin="lower")
    a.set_title(f"Frame {frames[i]}")
    a.set_xlabel("Pixel X")
    a.set_ylabel("Pixel Y")

plt.tight_layout()
plt.show()"""