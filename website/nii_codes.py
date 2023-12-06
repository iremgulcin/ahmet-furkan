import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from scipy.ndimage import zoom
import torch
from math import ceil
from torchvision import transforms
from PIL import Image
from segmentation_model import UNet
import shutil
import os
import subprocess




def show_nii(nii_file,TCNumber=None, image_date=None, image_type=None, ID = None):

    nii_img = nib.load(nii_file)
    axial_slices = nii_img.get_fdata()

    num_slices = axial_slices.shape[2]

    fig, axes = plt.subplots(num_slices, 1, figsize=(8, 4*num_slices))

    for i in range(num_slices):
        slice_2d = axial_slices[:, :, i]
        img_uint8 = ((slice_2d - np.min(slice_2d)) / (np.max(slice_2d) - np.min(slice_2d)) * 255).astype(np.uint8)
        y, x = img_uint8.shape
        y_factor = 256 / y
        x_factor = 256 / x
        img_uint8 = zoom(img_uint8, (y_factor, x_factor), order=0)

        axes[i].imshow(img_uint8, cmap='gray')
        axes[i].set_title(f"Orijinal Kesit: {i}")
        axes[i].axis('off')

    plt.tight_layout()
    plt.savefig(f'./static/assets/img/{TCNumber}/{image_date}_{image_type}_{ID}output_path.png')
    plt.close(fig)



def predict_unet(weights_path, original_nii_path, device="cpu", TCNumber=None, ID = None):
    model = UNet(n_channels=1, n_classes=3)
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)
    model.eval()

    nii_img = nib.load(original_nii_path)
    original_header = nii_img.header
    original_affine = nii_img.affine

    axial_slices = nii_img.get_fdata()
    num_slices = axial_slices.shape[2]

    output_dir = f'./static/assets/img/{TCNumber}/{ID}'

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(num_slices):
        slice_2d = axial_slices[:, :, i]

        img_uint8 = ((slice_2d - np.min(slice_2d)) / (np.max(slice_2d) - np.min(slice_2d)) * 255).astype(np.uint8)
        y, x = img_uint8.shape
        y_factor = 256 / y
        x_factor = 256 / x
        img_uint8 = zoom(img_uint8, (y_factor, x_factor), order=0)

        # Ön işleme ve tensora dönüştürme
        preprocess_unet = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])
        image_pil = Image.fromarray(img_uint8)
        tensor_image = preprocess_unet(image_pil).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(tensor_image)
            mask = torch.softmax(output, dim=1)
            mask = (mask > 0.5).float()
            mask = torch.argmax(mask, dim=1, keepdim=True)

        mask_np = mask.cpu().squeeze(0).numpy()
        mask_np = mask_np[0,:,:]

        np.save(f'./static/assets/img/{TCNumber}/{ID}/sub-x_mask_{i}.npy', mask_np)

    input_directory = f"./static/assets/img/{TCNumber}/{ID}"
    output_directory = f"./static/assets/img/{TCNumber}"
    original_nii_path = original_nii_path

    file_list = [f for f in os.listdir(input_directory) if f.endswith('.npy')]
    file_list = sorted(file_list, key= extract_number)
    
    combined_data = [np.load(os.path.join(input_directory, file)) for file in file_list]
    volume_data = np.stack(combined_data, axis=-1).astype("int16")
    nifti_image = nib.Nifti1Image(volume_data, affine=original_affine)

    for key in original_header.keys():
        if key in nifti_image.header:
            nifti_image.header[key] = original_header[key]

    output_file_path = os.path.join(output_directory, f'{ID}_AI_Analysis.nii.gz')
    nib.save(nifti_image, output_file_path)

    cmd1 = "cd ./3d-nii-visualizer"
    cmd2 = "conda activate guncel"
    cmd3 = f"python ./visualizer/brain_tumor_3d.py -i \".{original_nii_path}.gz\" -m \"../static/assets/img/{TCNumber}/{ID}_AI_Analysis.nii.gz\""
    run_command(f"{cmd1} && {cmd2} && {cmd3}")


def extract_number(filename):
    # Dosya adından numarayı çıkarır (e.g., 'sub-1_mask_45.npy' -> 45)
    return int(filename.split('_')[2].split('.')[0])

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Komut hata verdi: {err.decode('utf-8')}")
    else:
        print(out.decode('utf-8'))
