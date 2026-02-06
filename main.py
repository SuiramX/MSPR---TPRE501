import pandas as pd
import numpy as np

# =========================
# 1. Chargement du dataset
# =========================
df = pd.read_csv("FOOD-DATA-GROUP1.csv")

print("Dataset original :", df.shape)

# =========================
# 2. Suppression des colonnes inutiles
# =========================
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# =========================
# 3. Nettoyage des noms d'aliments
# =========================
df["food"] = (
    df["food"]
    .str.lower()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# =========================
# 4. Conversion des colonnes numériques
# =========================
numeric_cols = df.columns.drop("food")

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# 5. Gestion des valeurs manquantes
# =========================
# Remplacer les NaN par la médiane (plus robuste que la moyenne)
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# =========================
# 6. Suppression des doublons
# =========================
df = df.drop_duplicates(subset=["food"])

# =========================
# 7. Correction des valeurs aberrantes (outliers)
# =========================
def remove_outliers(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return column.clip(lower, upper)

for col in numeric_cols:
    df[col] = remove_outliers(df[col])

# =========================
# 8. Correction des incohérences nutritionnelles
# =========================
# Exemple : calories négatives ou absurdes
df["Caloric Value"] = df["Caloric Value"].clip(lower=0, upper=900)

# Lipides, glucides, protéines >= 0
macro_cols = ["Fat", "Carbohydrates", "Protein"]
for col in macro_cols:
    if col in df.columns:
        df[col] = df[col].clip(lower=0)

# =========================
# 9. Normalisation (optionnelle)
# =========================
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# =========================
# 10. Export du dataset propre
# =========================
df.to_csv("FOOD-DATA-CLEAN.csv", index=False)

print("Dataset nettoyé :", df.shape)
print("✅ Nettoyage terminé !")
