\# DocAI



DocAI est une application web intelligente permettant de prédire une maladie probable à partir d'une liste de symptômes sélectionnés par l'utilisateur.



Le projet utilise un modèle de Machine Learning entraîné en Python et intégré dans une application Flask.



> Ce projet est réalisé dans un cadre pédagogique. Il ne remplace pas un avis médical professionnel.



\## Fonctionnalités



\- Sélection des symptômes via une interface web

\- Prédiction automatique d'une maladie probable

\- Affichage d'une description de la maladie

\- Affichage des précautions recommandées

\- Application Flask déployable localement ou avec Docker



\## Structure du projet



```text

DocAI/

│

├── diagnostic\_app/

│   ├── app.py

│   ├── model.joblib

│   ├── disease\_descriptions.csv

│   ├── precautions.csv

│   ├── requirements.txt

│   ├── Dockerfile

│   ├── static/

│   └── templates/

│

├── v2.ipynb

└── README.md

