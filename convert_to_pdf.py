# -*- coding: utf-8 -*-

import argparse
import os

from PIL import Image
from rich import print
from rich.progress import Progress

ROOT_FOLDER = "DL SushiScan"

def convert_to_pdf(folder_to_convert, quality):
    main_folder_path = os.path.join(ROOT_FOLDER, folder_to_convert)

    if not os.path.exists(main_folder_path):
        print(f"[bold red]Le dossier '{main_folder_path}' n'existe pas.[/bold red]")
        exit()

    subfolders = [f.path for f in os.scandir(main_folder_path) if f.is_dir()]

    if not subfolders:
        print("[bold yellow]Aucun sous-dossier trouvé dans le dossier principal.[/bold yellow]")
        exit()

    with Progress() as progress:
        task = progress.add_task("[cyan]Conversion des sous-dossiers...", total=len(subfolders))
        
        for subfolder in subfolders:
            subfolder_name = os.path.basename(subfolder)
            image_files = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]
            image_files.sort()

            if not image_files:
                print(f"[bold yellow]Aucune image trouvée dans le sous-dossier '{subfolder_name}'.[/bold yellow]")
                progress.advance(task)
                continue

            try:
                first_image = Image.open(os.path.join(subfolder, image_files[0]))
                other_images = [
                    Image.open(os.path.join(subfolder, image)).convert('RGB') for image in image_files[1:]
                ]

                output_folder = os.path.join(ROOT_FOLDER, folder_to_convert + " - PDF")
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                output_pdf_path = os.path.join(output_folder, f"{subfolder_name}.pdf")
                first_image.save(
                    output_pdf_path,
                    save_all=True,
                    append_images=other_images,
                    quality=quality,
                )
                print(f"[bold green]Les images du sous-dossier '{subfolder_name}' ont été fusionnées dans '{output_pdf_path}'.[/bold green]")

            except Exception as e:
                print(f"[bold red]Erreur lors de la conversion du sous-dossier '{subfolder_name}' : {e}[/bold red]")

            finally:
                first_image.close()
                for img in other_images:
                    img.close()

            progress.advance(task)

def main():
    parser = argparse.ArgumentParser(description="Convertir des images en PDF avec une qualité choisie.")
    parser.add_argument("-f", "--folder", required=True, help="Nom du dossier à convertir (doit être dans le répertoire racine).")
    parser.add_argument("-q", "--quality", type=int, default=95, help="Qualité des PDF (par défaut : 95, minimum : 1, maximum : 100).")
    args = parser.parse_args()

    print("[bold cyan]Conversion en cours...[/bold cyan]")
    convert_to_pdf(args.folder, args.quality)
    print("[bold green]Conversion terminée ![/bold green]")

if __name__ == "__main__":
    main()
