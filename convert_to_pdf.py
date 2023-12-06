from PIL import Image
import os

'''
pip install pillow
'''

root_folder = "DL SushiScan"

folder_to_convert = input("Please enter the name of the folder to convert: ")
main_folder_path = os.path.join(root_folder, folder_to_convert)

if not os.path.exists(main_folder_path):
    print(f"The folder '{main_folder_path}' does not exist.")
    exit()

subfolders = [f.path for f in os.scandir(main_folder_path) if f.is_dir()]

if not subfolders:
    print("No subfolders found in the main folder.")
    exit()

for subfolder in subfolders:
    subfolder_name = os.path.basename(subfolder)
    image_files = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]
    image_files.sort()

    if not image_files:
        print(f"No images found in the subfolder '{subfolder_name}'.")
        continue

    first_image = Image.open(os.path.join(subfolder, image_files[0]))

    other_images = [Image.open(os.path.join(subfolder, image)).convert('RGB') for image in image_files[1:]]

    output_folder = os.path.join(root_folder, folder_to_convert + " - PDF")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_pdf_path = os.path.join(output_folder, f"{subfolder_name}.pdf")
    first_image.save(output_pdf_path, save_all=True, append_images=other_images)
    print(f"Images from subfolder '{subfolder_name}' have been merged into '{output_pdf_path}'.")

    first_image.close()
    for img in other_images:
        img.close()
