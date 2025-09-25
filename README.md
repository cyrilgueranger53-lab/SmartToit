# SmartToit - Streamlit Version

Cette application permet de :
- Upload d'une photo de toiture
- Détection d'ardoises cassées/fissurées/manquantes avec YOLOv8
- Affichage de l'image annotée
- Visualisation 3D de la toiture avec Three.js
- Génération d'un rapport PDF

## Déploiement Streamlit
1. Installer Streamlit et dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lancer l'application :
   ```bash
   streamlit run streamlit_app.py
   ```
3. Déployer sur Streamlit Cloud :
   - Connecter le dépôt GitHub
   - Choisir `streamlit_app.py` comme fichier principal
