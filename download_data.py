import kagglehub
import os
import shutil

path = kagglehub.dataset_download("mostafaabla/garbage-classification")

print(f"✅ Dataset downloaded to: {path}")

desktop = os.path.expanduser("~/Desktop")
target_base = os.path.join(desktop, "waste_dataset")
os.makedirs(target_base, exist_ok=True)

mapping = {
    "plastic": "plastic_bottles",
    "metal": "metal_cans",
    "paper": "cardboard_paper",
    "cardboard": "cardboard_paper",
    "trash": "organic_kitchen",
    "glass": None
}

for root, dirs, files in os.walk(path):
    for dir_name in dirs:
        if dir_name in mapping and mapping[dir_name] is not None:
            src = os.path.join(root, dir_name)
            dst = os.path.join(target_base, mapping[dir_name])
            
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"📁 Copied {dir_name} -> {mapping[dir_name]}")

print(f"📍 Location: {target_base}")
