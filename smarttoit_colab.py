{
 "cells": [
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "!pip install ultralytics==8.0.134",
    "!pip install torch==2.1.0 torchvision==0.18.1",
    "!pip install opencv-python",
    "!pip install reportlab",
    "!pip install numpy",
    "!pip install matplotlib",
    "!pip install ipywidgets"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import os",
    "UPLOAD_DIR = '/content/uploads'",
    "RESULTS_DIR = '/content/results'",
    "REPORTS_DIR = '/content/reports'",
    "MODELS_DIR = '/content/models'",
    "os.makedirs(UPLOAD_DIR, exist_ok=True)",
    "os.makedirs(RESULTS_DIR, exist_ok=True)",
    "os.makedirs(REPORTS_DIR, exist_ok=True)",
    "os.makedirs(MODELS_DIR, exist_ok=True)",
    "print('Dossiers prêts !')"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from ultralytics import YOLO",
    "model_path = os.path.join(MODELS_DIR, 'roof_defects.pt')",
    "model = YOLO(model_path)",
    "print('Modèle chargé !')"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from google.colab import files",
    "uploaded = files.upload()",
    "for filename in uploaded.keys():",
    "    dest_path = os.path.join(UPLOAD_DIR, filename)",
    "    with open(dest_path, 'wb') as f:",
    "        f.write(uploaded[filename])",
    "    print(f'{filename} uploadé dans {UPLOAD_DIR}')"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import cv2",
    "import numpy as np",
    "from matplotlib import pyplot as plt",
    "for img_name in os.listdir(UPLOAD_DIR):",
    "    img_path = os.path.join(UPLOAD_DIR, img_name)",
    "    results = model.predict(img_path, conf=0.25, imgsz=1280)",
    "    r = results[0]",
    "    annotated = r.plot()",
    "    out_path = os.path.join(RESULTS_DIR, f'annotated_{img_name}')",
    "    cv2.imwrite(out_path, annotated)",
    "    img_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)",
    "    plt.figure(figsize=(10,8))",
    "    plt.imshow(img_rgb)",
    "    plt.axis('off')",
    "    plt.title(f'Annotations : {img_name}')",
    "    plt.show()",
    "    print(f'Image annotée enregistrée dans {out_path}')"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer",
    "from reportlab.lib.styles import getSampleStyleSheet",
    "for img_name in os.listdir(RESULTS_DIR):",
    "    img_path = os.path.join(RESULTS_DIR, img_name)",
    "    pdf_path = os.path.join(REPORTS_DIR, img_name.replace('.jpg','.pdf'))",
    "    doc = SimpleDocTemplate(pdf_path)",
    "    styles = getSampleStyleSheet()",
    "    story = [Paragraph('Rapport d\'analyse de toiture', styles['Title']), Spacer(1,12)]",
    "    story.append(Image(img_path, width=400, height=300))",
    "    doc.build(story)",
    "    print(f'PDF généré : {pdf_path}')"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import matplotlib.pyplot as plt",
    "from mpl_toolkits.mplot3d import Axes3D",
    "import numpy as np",
    "fig = plt.figure(figsize=(8,6))",
    "ax = fig.add_subplot(111, projection='3d')",
    "coords = np.array([[2,0,1], [-1,0,-2], [3,0,-1]])",
    "for x,y,z in coords:",
    "    ax.bar3d(x, z, 0, 0.5, 0.5, 0.5, color='red', alpha=0.8)",
    "ax.set_xlabel('X')",
    "ax.set_ylabel('Z')",
    "ax.set_zlabel('Y')",
    "ax.set_title('Toiture 3D (simulation)')",
    "plt.show()"
   ]
  }
 ],
 "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.11"}},
 "nbformat": 4,
 "nbformat_minor": 5
}
