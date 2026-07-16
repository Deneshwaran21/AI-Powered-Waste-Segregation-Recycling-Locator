import kagglehub
import os
import shutil

# Download the latest version of the Garbage Classification dataset
path = kagglehub.dataset_download("mostafaabla/garbage-classification")

print(f"✅ Dataset downloaded to: {path}")

# The dataset usually comes in a folder with subfolders like 'cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash'
# We only need to map these to our 5 categories.
# Let's copy them to a clean 'waste_dataset' folder on your desktop

desktop = os.path.expanduser("~/Desktop")
target_base = os.path.join(desktop, "waste_dataset")
os.makedirs(target_base, exist_ok=True)

# Map Kaggle's folder names to ours
# (If the dataset has 'plastic', we copy to 'plastic_bottles', etc.)
mapping = {
    "plastic": "plastic_bottles",
    "metal": "metal_cans",
    "paper": "cardboard_paper",
    "cardboard": "cardboard_paper",  # Just in case
    "trash": "organic_kitchen",      # We will manually filter these
    "glass": None  # We don't need glass for our 5 classes
}

# Walk through the downloaded path
for root, dirs, files in os.walk(path):
    for dir_name in dirs:
        if dir_name in mapping and mapping[dir_name] is not None:
            src = os.path.join(root, dir_name)
            dst = os.path.join(target_base, mapping[dir_name])
            
            # Copy the folder
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"📁 Copied {dir_name} -> {mapping[dir_name]}")

print("\n🎉 Dataset is ready on your Desktop inside 'waste_dataset'!")
print(f"📍 Location: {target_base}")