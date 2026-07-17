import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
import time

DATA_DIR = "waste_dataset"
NUM_CLASSES = 5
BATCH_SIZE = 32
EPOCHS = 25
LEARNING_RATE = 0.001

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

train_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


print("Loading dataset...")
full_dataset = datasets.ImageFolder(root=DATA_DIR, transform=train_transform)


if len(full_dataset) == 0:
    print(f"ERROR: No images found in '{DATA_DIR}'.")
    print("Please make sure your folder has subfolders like 'plastic_bottles', 'chips_packets', etc.")
    exit()


class_names = full_dataset.classes
print(f"Found {len(full_dataset)} images across {len(class_names)} classes:")
for i, name in enumerate(class_names):
    print(f"   {i}: {name}")


train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])


val_dataset.dataset.transform = val_transform

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

print(f"Train samples: {train_size}, Validation samples: {val_size}")


print("Building ResNet-50 model...")
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)


for param in model.parameters():
    param.requires_grad = False


num_features = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(num_features, 512),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(512, NUM_CLASSES)
)

model = model.to(device)


criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)


print("Starting training...\n")
best_val_acc = 0.0

for epoch in range(1, EPOCHS + 1):
    # --- Training Phase ---
    model.train()
    running_loss = 0.0
    correct_train = 0
    total_train = 0
    
    loop = tqdm(train_loader, desc=f"Epoch {epoch}/{EPOCHS} [Train]")
    for images, labels in loop:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total_train += labels.size(0)
        correct_train += (predicted == labels).sum().item()
        
        loop.set_postfix(loss=loss.item(), acc=100 * correct_train / total_train)
    
    train_acc = 100 * correct_train / total_train
    avg_loss = running_loss / len(train_loader)
    
    # --- Validation Phase ---
    model.eval()
    correct_val = 0
    total_val = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total_val += labels.size(0)
            correct_val += (predicted == labels).sum().item()
    
    val_acc = 100 * correct_val / total_val
    
    print(f"Epoch {epoch} | Loss: {avg_loss:.4f} | Train Acc: {train_acc:.2f}% | Val Acc: {val_acc:.2f}%")
    
    # Save the best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "waste_model.pth")
        print(f"New best model saved! (Val Acc: {best_val_acc:.2f}%)")
    
    print("-" * 50)

print(f" Best Validation Accuracy: {best_val_acc:.2f}%")
print(f" Model saved as: waste_model.pth")
