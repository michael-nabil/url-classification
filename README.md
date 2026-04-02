# url-classification
Classifying URLs into either safe or malicious.
## URL Security Classification System

This project implements a **machine learning-based security system** designed to classify URLs as either **Safe** or **Malicious** in real time.

Unlike traditional blacklist-based approaches, this system uses a **Hybrid Feature Extraction** technique, combining:

- **Lexical Analysis** (mathematical properties of the URL string)
- **Character-level NLP** using **TF-IDF N-grams**

This allows the system to detect **malicious patterns and substrings**, even in previously unseen URLs.

---

## Dataset

- Source: [Kaggle](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls)

---

## Feature Engineering

The system extracts two types of features:

1. **Lexical Features**
   - URL length  
   - Host name length  
   - Dot count
   - Digit count
   - Other structural properties  

2. **TF-IDF Features**
   - Character-level N-grams  
   - Captures hidden and suspicious substrings inside URLs  

---

## Models Used

### 1. Random Forest (Lexical Features Only)
- Trained using only extracted lexical features  
- Learns structural patterns of malicious URLs  

### 2. Random Forest (Hybrid Features)
- Combines:
  - TF-IDF features  
  - Lexical features  
- Provides improved detection by leveraging both structure and text patterns  

---

## Frontend

- A simple frontend page was created to:
  - Input URLs  
  - Display prediction results (Safe / Malicious)  

---

## Deployment

- The model is deployed using **FastAPI**
- Exposes an API endpoint for real-time predictions  

---

## Project Goal

To build a **robust and scalable system** capable of detecting malicious URLs in real time using machine learning techniques.

---
