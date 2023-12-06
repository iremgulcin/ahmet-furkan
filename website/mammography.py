import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image


birads_weight = r"static\assets\models\birads_weight.pth"
composition_weight = r"static\assets\models\composition_weight.pth"

class MultiViewGoogleNet(nn.Module):
    def __init__(self, num_classes=3):
        super(MultiViewGoogleNet, self).__init__()

        self.googlenet = models.googlenet(pretrained=True)
        num_ftrs = self.googlenet.fc.in_features
        self.googlenet.fc = nn.Identity()

        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(num_ftrs * 2, num_classes)

    def forward(self, x1, x2):
        x1 = self.googlenet(x1)
        x2 = self.googlenet(x2)

        x = torch.cat((x1, x2), dim=1)
        x = self.dropout(x)
        x = self.classifier(x)

        return x


class MultiViewVGG16(nn.Module):
    def __init__(self, num_classes=4):
        super(MultiViewVGG16, self).__init__()

        self.vgg16 = models.vgg16(pretrained=True)
        self.vgg16.classifier = nn.Sequential(*list(self.vgg16.classifier.children())[:-1])

        self.dropout = nn.Dropout(0.4)
        self.classifier = nn.Linear(4096 * 4, num_classes)

    def forward(self, x1, x2, x3, x4):
        x1 = self.vgg16(x1)
        x2 = self.vgg16(x2)
        x3 = self.vgg16(x3)
        x4 = self.vgg16(x4)

        x = torch.cat((x1, x2, x3, x4), dim=1)
        x = self.dropout(x)
        x = self.classifier(x)

        return x


def predict_birads_right(image_path_rcc, image_path_rmlo, model_path = birads_weight):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MultiViewGoogleNet(num_classes=3)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.RandomHorizontalFlip(p=1.0),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    rcc_image = Image.open(image_path_rcc).convert('RGB')
    rmlo_image = Image.open(image_path_rmlo).convert('RGB')
    rcc_image = preprocess(rcc_image).unsqueeze(0).to(device)
    rmlo_image = preprocess(rmlo_image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(rcc_image, rmlo_image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        prediction = torch.argmax(probabilities).item()
        max_probability = max(probabilities[0]) * 100  # Yüzde cinsinden
        predicted_class = prediction
        print(f"Predicted BIRADS RIGHT Class: {predicted_class}, Probability: {max_probability:.2f}%")

    return predicted_class, max_probability.numpy()



def predict_birads_left(image_path_lcc, image_path_lmlo, model_path = birads_weight):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MultiViewGoogleNet(num_classes=3)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    lcc_image = Image.open(image_path_lcc).convert('RGB')
    lmlo_image = Image.open(image_path_lmlo).convert('RGB')
    lcc_image = preprocess(lcc_image).unsqueeze(0).to(device)
    lmlo_image = preprocess(lmlo_image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(lcc_image, lmlo_image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        prediction = torch.argmax(probabilities).item()
        max_probability = max(probabilities[0]) * 100  # Yüzde cinsinden
        predicted_class = prediction
        print(f"Predicted BIRADS LEFT Class: {predicted_class}, Probability: {max_probability:.2f}%")

    return predicted_class, max_probability.numpy()


def predict_composition(image_path_rcc, image_path_lcc, image_path_rmlo, image_path_lmlo, model_path = composition_weight):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MultiViewVGG16(num_classes=4)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    rcc_image = Image.open(image_path_rcc).convert('RGB')
    lcc_image = Image.open(image_path_lcc).convert('RGB')
    rmlo_image = Image.open(image_path_rmlo).convert('RGB')
    lmlo_image = Image.open(image_path_lmlo).convert('RGB')
    rcc_image = preprocess(rcc_image).unsqueeze(0).to(device)
    lcc_image = preprocess(lcc_image).unsqueeze(0).to(device)
    rmlo_image = preprocess(rmlo_image).unsqueeze(0).to(device)
    lmlo_image = preprocess(lmlo_image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(rcc_image, lcc_image, rmlo_image, lmlo_image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        prediction = torch.argmax(probabilities).item()
        max_probability = max(probabilities[0]) * 100  # Yüzde cinsinden
        predicted_class = prediction
        print(f"Predicted Composition Class: {predicted_class}, Probability: {max_probability:.2f}%")

    return predicted_class, max_probability.numpy()



# def predict_single_view(image_path, model_path):

#     VGG16 = models.vgg16(weights="VGG16_Weights.IMAGENET1K_V1")
#     num_ftrs = VGG16.classifier[6].in_features
#     VGG16.classifier[6].in_features = nn.Linear(num_ftrs, 3)
#     model = VGG16
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model.to(device)
#     model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

#     model.eval()
    
#     image = Image.open(image_path)
#     image = image.convert('RGB')
#     preprocess = transforms.Compose([
#         transforms.Resize((512,512)),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ])
#     image = preprocess(image).unsqueeze(0)

#     with torch.no_grad():
#         output = VGG16(image)
#         probabilities = torch.nn.functional.softmax(output, dim=1)
#         prediction = torch.argmax(probabilities).item()
#         # print(prediction, probabilities[0].numpy())
#     return prediction, probabilities[0].numpy()

# preprocess = transforms.Compose([
#     transforms.Resize((256, 256)),
#     transforms.ToTensor(),
# ])


# rcc = r"C:\Users\FURKA\Desktop\jobs\RDIX\MAMOGRAFI_JPG\822670235\RCC.jpg"
# lcc = r"C:\Users\FURKA\Desktop\jobs\RDIX\MAMOGRAFI_JPG\822670235\LCC.jpg"
# rmlo = r"C:\Users\FURKA\Desktop\jobs\RDIX\MAMOGRAFI_JPG\822670235\RMLO.jpg"
# lmlo = r"C:\Users\FURKA\Desktop\jobs\RDIX\MAMOGRAFI_JPG\822670235\LMLO.jpg"
# birads_weight = r"static\assets\models\birads_weight.pth"
# composition_weight = r"static\assets\models\composition_weight.pth"
# prediction, probabilities = predict_birads(lcc, lmlo, birads_weight)
# prediction, probabilities = predict_composition(rcc, lcc, rmlo, lmlo, composition_weight)

