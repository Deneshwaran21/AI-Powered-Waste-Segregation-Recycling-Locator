import torch
import torch.nn as nn
from torchvision import transforms, models
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os


app = FastAPI()

# Allow Streamlit to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Rebuild the exact same architecture used in training
model = models.resnet50(weights=None)
num_features = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(num_features, 512),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(512, 5)
)

# Load the trained weights
model.load_state_dict(torch.load("waste_model.pth", map_location=device))
model = model.to(device)
model.eval()
print("Model loaded successfully!")


CLASS_NAMES = ["cardboard_paper", "chips_packets", "metal_cans", "organic_kitchen", "plastic_bottles"]

# Emojis for the frontend
CLASS_EMOJIS = {
    "cardboard_paper": "📦",
    "chips_packets": "🍟",
    "metal_cans": "🥫",
    "organic_kitchen": "🍃",
    "plastic_bottles": "🧴"
}

# Dummy recycling agents (You can edit these addresses)
RECYCLERS = {
    "cardboard_paper": [{"name": "PaperCycle Hub", "address": "12/B, Nehru Nagar", "distance": "3.1 km"}],
    "chips_packets": [{"name": "GreenLayer Solutions", "address": "Shop 5, MG Road", "distance": "1.8 km"}],
    "metal_cans": [{"name": "MetalMithra", "address": "G-7, Auto Nagar", "distance": "4.0 km"}],
    "organic_kitchen": [{"name": "Compost Kings", "address": "Farm 23, Outer Ring Road", "distance": "5.2 km"}],
    "plastic_bottles": [{"name": "EcoPlast Recyclers", "address": "Plot 42, Industrial Area", "distance": "2.3 km"}]
}


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Preprocess
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    class_idx = predicted.item()
    class_name = CLASS_NAMES[class_idx]
    conf_score = round(confidence.item() * 100, 2)
    
    # Get recyclers
    recyclers = RECYCLERS.get(class_name, [])
    
    return {
        "class": class_name,
        "emoji": CLASS_EMOJIS.get(class_name, "♻️"),
        "confidence": conf_score,
        "recyclers": recyclers
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)