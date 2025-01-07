# SushiScan DownLoader

Script Python simple et efficace pour télécharger des scans depuis sushiscan.net et les convertir en PDF.

## Installation des dépendances

Commencez par installer ces packages :
```bash
pip install curl_cffi rich pillow
```

---

## Téléchargement des scans

- **`-u` ou `--url`** *(obligatoire)* :  
  L'URL du catalogue à télécharger depuis sushiscan.net.

- **`-c` ou `--cookie`** *(obligatoire)* :  
  La valeur du cookie `cf_clearance` récupéré après avoir passé le captcha sur sushiscan.net.

- **`-ua` ou `--user-agent`** *(obligatoire)* :  
  L'User-Agent de votre navigateur.

- **`-t` ou `--threads`** *(optionnel)* :  
  Nombre de threads à utiliser, par défaut 10.

### Exemple d'utilisation

```bash
py main.py -u "https://sushiscan.net/catalogue/dragon-ball-z-les-films/" -c "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" -ua "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

Entrez la plage de volumes à télécharger (par exemple, pour tout télécharger : 1-7) : 1-7
Nombre de volumes à télécharger : 7
Téléchargement des volumes de 1 à 7...
Image téléchargée : https://sushiscan.net/wp-content/uploads27/DBFilm1-001.jpg
...
Image téléchargée : https://sushiscan.net/wp-content/uploads27/DBFilm7-132.jpg
Image téléchargée : https://sushiscan.net/wp-content/uploads27/DBFilm7-134.jpg
Téléchargement terminé.
```

---

## Conversion en PDF

- **`-f` ou `--folder`** *(obligatoire)* :  
  Indique le nom du dossier à convertir en PDF. Le dossier doit être dans `DL SushiScan`.

- **`-q` ou `--quality`** *(optionnel)* :  
  Définit la qualité des images dans le PDF, entre 1 et 100, par défaut 95.

### Exemple d'utilisation

```bash
py convert_to_pdf.py -f "Dragon Ball Z - Les Films" -q 80

Conversion en cours...
Les images du sous-dossier 'Film 1' ont été fusionnées dans 'DL SushiScan\Dragon Ball Z - Les Films - PDF\Film 1.pdf'.
Les images du sous-dossier 'Film 2' ont été fusionnées dans 'DL SushiScan\Dragon Ball Z - Les Films - PDF\Film 2.pdf'.
Les images du sous-dossier 'Film 3' ont été fusionnées dans 'DL SushiScan\Dragon Ball Z - Les Films - PDF\Film 3.pdf'.
Les images du sous-dossier 'Film 4' ont été fusionnées dans 'DL SushiScan\Dragon Ball Z - Les Films - PDF\Film 4.pdf'.
Les images du sous-dossier 'Film 5' ont été fusionnées dans 'DL SushiScan\Dragon Ball Z - Les Films - PDF\Film 5.pdf'.
Les images du sous-dossier 'Film 6' ont été fusionnées dans 'DL SushiScan\Dragon Ball Z - Les Films - PDF\Film 6.pdf'.
Les images du sous-dossier 'Film 7' ont été fusionnées dans 'DL SushiScan\Dragon Ball Z - Les Films - PDF\Film 7.pdf'.
Conversion des sous-dossiers... ---------------------------------------- 100% 0:00:00
Conversion terminée !
```

---

## Structure finale du répertoire

Une fois tous les fichiers téléchargés et convertis, la structure du répertoire ressemblera à ceci :

```plaintext
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
