# 🌧️ Sri Lanka Flood & Rainfall Risk Intelligence System

An AI-powered GIS disaster intelligence dashboard developed for monitoring rainfall patterns, flood-prone regions, environmental risk levels, and flood risk prediction across Sri Lanka using geospatial analytics and Machine Learning.

---

# 🌍 Live Demo

https://sri-lanka-flood-rainfall-risk-gis-sanjula2003.streamlit.app/

---

# 📌 Project Overview

This project was developed as part of a Sri Lanka-focused GIS & AI portfolio aligned with environmental monitoring, disaster intelligence, and national-scale decision-support systems.

The platform combines:

* GIS-based flood monitoring
* Rainfall analytics
* District flood risk intelligence
* Environmental monitoring
* Machine Learning-based flood risk prediction
* Interactive operational dashboard UI

The dashboard helps identify flood-prone districts and supports disaster preparedness analysis using geospatial intelligence techniques.

---

# ✨ Main Features

## 🗺️ Flood Risk GIS Mapping

Interactive GIS visualization of flood-prone districts and environmental risk zones across Sri Lanka.

## 🌧️ Rainfall Monitoring Analytics

District-wise rainfall distribution and trend monitoring.

## 🚨 Flood Risk Intelligence

Risk scoring system using:

* Rainfall intensity
* River level
* Soil saturation
* Flood history

## 🌊 AI Flood Risk Prediction

Machine Learning model predicts:

* Low Flood Risk
* Medium Flood Risk
* High Flood Risk

based on environmental conditions.

## 📈 Rainfall Trend Analysis

Time-series monitoring of rainfall conditions.

## 🔎 Interactive Filtering

Filter by:

* Flood risk level
* Drainage condition

## ⬇️ Downloadable Processed Datasets

Users can download processed environmental datasets directly from the dashboard.

---

# 🛠️ Technologies Used

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python       | Core Programming          |
| Streamlit    | Dashboard Development     |
| Pandas       | Data Processing           |
| Plotly       | Interactive Visualization |
| Folium       | GIS Mapping               |
| Scikit-learn | Machine Learning          |
| Joblib       | Model Serialization       |

---

# 🧠 Machine Learning Model

The flood prediction module uses:

* Random Forest Classifier
* Label Encoding
* Environmental Feature Engineering
* Flood Risk Classification

### Prediction Inputs

* District
* Monthly Rainfall
* River Level
* Soil Saturation
* Population Density
* Flood History Count
* Drainage Condition

### Prediction Output

* Low Flood Risk
* Medium Flood Risk
* High Flood Risk

---

# 📂 Project Structure

```text id="jlwmr9"
Sri-Lanka-Flood-Rainfall-Risk-GIS/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── rainfall_flood_risk.csv
│
├── models/
│   ├── flood_risk_model.pkl
│   ├── label_encoders.pkl
│   └── model_train.py
│
├── assets/
│   └── dashboard_preview.png
```

---

# ⚙️ Installation Guide

## Clone Repository

```bash id="bg3q3w"
git clone https://github.com/Sanjula2003/Sri-Lanka-Flood-Rainfall-Risk-GIS.git
```

## Navigate to Project

```bash id="11kqz8"
cd Sri-Lanka-Flood-Rainfall-Risk-GIS
```

## Install Requirements

```bash id="6uy3kt"
pip install -r requirements.txt
```

## Run Application

```bash id="3pivpn"
streamlit run app.py
```

---

# 📈 Future Improvements

* Real-time rainfall API integration
* Satellite rainfall monitoring
* Deep Learning flood forecasting
* Real-time disaster alerts
* Historical flood intelligence analysis
* National disaster early-warning system

---

# 👨‍💻 Developer

Sanjula Bandara
BSc (Hons) in Data Science
NSBM Green University

Focused Areas:

* Data Science
* GIS Analytics
* Disaster Intelligence
* Machine Learning
* Environmental Monitoring Systems

---

# 📜 License

This project is developed for educational, research, and portfolio purposes.
