# SushiScan DownLoader

Simple Python script for bulk download scans from sushiscan.net.

## FR - Exemple d'utilisation

Commencez par installer ces packages :
```bash
pip install pillow httpx colorama
```

### Téléchargement

```bash
py main.py

Please enter the URL of catalogue: https://sushiscan.net/catalogue/dragon-ball-z-les-films/
Access denied with status code 403. Please enter 'cf_clearance' cookie value.
```

Visitez le site web sushiscan.net et complétez le captcha Cloudflare Turnstile pour accéder au site. Une fois sur la page de SushiScan, récupérez le cookie "cf_clearance" ainsi que votre User Agent.

```bash
Cookie value for 'cf_clearance': xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Please enter your User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

### Tout convertir au format PDF

```bash
py convert_to_pdf.py
Please enter the name of the folder to convert: Dragon Ball Z – Les Films
Images from subfolder 'Film 1' have been merged into 'DL SushiScan\Dragon Ball Z – Les Films - PDF\Film 1.pdf'.
Images from subfolder 'Film 2' have been merged into 'DL SushiScan\Dragon Ball Z – Les Films - PDF\Film 2.pdf'.
Images from subfolder 'Film 3' have been merged into 'DL SushiScan\Dragon Ball Z – Les Films - PDF\Film 3.pdf'.
Images from subfolder 'Film 4' have been merged into 'DL SushiScan\Dragon Ball Z – Les Films - PDF\Film 4.pdf'.
Images from subfolder 'Film 5' have been merged into 'DL SushiScan\Dragon Ball Z – Les Films - PDF\Film 5.pdf'.
Images from subfolder 'Film 6' have been merged into 'DL SushiScan\Dragon Ball Z – Les Films - PDF\Film 6.pdf'.
Images from subfolder 'Film 7' have been merged into 'DL SushiScan\Dragon Ball Z – Les Films - PDF\Film 7.pdf'.
```

### Répertoire final
```txt
│   convert_to_pdf.py
│   main.py
│
└───DL SushiScan
    ├───Dragon Ball Z – Les Films
    │   ├───Film 1
    │   │       DBFilm1-001.jpg
    │   │       ...
    │   │       DBFilm1-138.jpg
    │   │
    │   ├───Film 2
    │   │       DBFilm2-001.jpg
    │   │       ...
    │   │       DBFilm2-140.jpg
    │   │
    │   ├───Film 3
    │   │       DBFilm3-001.jpg
    │   │       ...
    │   │       DBFilm3-144.jpg
    │   │
    │   ├───Film 4
    │   │       DBFilm4-001.jpg
    │   │       ...
    │   │       DBFilm4-140.jpg
    │   │
    │   ├───Film 5
    │   │       DBFilm5-001.jpg
    │   │       ...
    │   │       DBFilm5-141.jpg
    │   │
    │   ├───Film 6
    │   │       DBFilm6-001.jpg
    │   │       ...
    │   │       DBFilm6-135.jpg
    │   │
    │   └───Film 7
    │           DBFilm7-001.jpg
    │           ...
    │           DBFilm7-134.jpg
    │
    └───Dragon Ball Z – Les Films - PDF
            Film 1.pdf
            Film 2.pdf
            Film 3.pdf
            Film 4.pdf
            Film 5.pdf
            Film 6.pdf
            Film 7.pdf
```

