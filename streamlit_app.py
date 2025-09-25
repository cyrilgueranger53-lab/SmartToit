import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
import os
import uuid
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet

UPLOAD_DIR = "uploads"
RESULTS_DIR = "results"
REPORTS_DIR = "reports"
MODELS_DIR = "models"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

st.title("SmartToit - Détection de Défauts sur Toitures")

uploaded_files = st.file_uploader(
    "Uploader des photos de toiture", 
    type=["jpg","png","jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    model_path = os.path.join(MODELS_DIR, "roof_defects.pt")
    model = YOLO(model_path)  # modèle fissures / cassures / manquantes
    for uploaded_file in uploaded_files:
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_DIR, f"{file_id}_{uploaded_file.name}")
        with open(input_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(input_path, caption=f"Photo uploadée: {uploaded_file.name}")

        results = model.predict(input_path, conf=0.25, imgsz=1280)
        r = results[0]
        annotated = r.plot()
        out_name = f"{file_id}_annotated.jpg"
        out_path = os.path.join(RESULTS_DIR, out_name)
        cv2.imwrite(out_path, annotated)
        st.image(out_path, caption=f"Image annotée: {uploaded_file.name}")

        stats = {}
        try:
            classes = r.boxes.cls.cpu().numpy().astype(int)
            unique, counts = np.unique(classes, return_counts=True)
            names = model.names if hasattr(model, 'names') else {}
            for u,c in zip(unique,counts):
                label = names.get(int(u), str(int(u)))
                stats[label] = int(c)
        except:
            stats['detections'] = len(r.boxes) if r.boxes is not None else 0
        st.subheader(f"Statistiques pour {uploaded_file.name}")
        st.json(stats)

        if st.button(f"Générer PDF pour {uploaded_file.name}"):
            report_path = os.path.join(REPORTS_DIR, f"{file_id}.pdf")
            doc = SimpleDocTemplate(report_path)
            styles = getSampleStyleSheet()
            story = [Paragraph("Rapport d'analyse de toiture", styles['Title']), Spacer(1,12)]
            for k,v in stats.items():
                story.append(Paragraph(f"{k}: {v}", styles['Normal']))
            story.append(Spacer(1,12))
            story.append(Image(out_path, width=400, height=300))
            doc.build(story)
            st.success(f"PDF généré: {report_path}")

    st.subheader("Toiture 3D")
    lat = st.number_input("Latitude", value=48.8566)
    lng = st.number_input("Longitude", value=2.3522)
    st.markdown("<div id='roof3d' style='width:600px; height:400px; border:1px solid #000;'></div>", unsafe_allow_html=True)
    st.components.v1.html(f'''
        <script src="https://cdn.jsdelivr.net/npm/three@0.154.0/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.154.0/examples/js/controls/OrbitControls.js"></script>
        <script src="static/three_toit.js"></script>
        <script>
            const ardoises = [{{x:2,z:1}},{{x:-1,z:-2}},{{x:3,z:-1}}];
            initRoof3D({{lat}},{{lng}},10,5,ardoises);
        </script>
    ''', height=420)
