
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

def load_data():
    """
    GDP verisini CSV'den yükle ve temizle
    """
    path = r"D:\\python\\flask_simple_todo\\project_new\\data\\GDP.csv"  # kendi dosya yoluna göre ayarla
    df = pd.read_csv(path, encoding="utf-8")
    df.columns = df.columns.str.strip()

    # Eğer Year ve GDP sütunları yoksa, sütunları yeniden düzenle
    if not {"Year", "GDP"}.issubset(df.columns):
        # Örnek: Eğer veriler yıllara göre sütunlarda ise melt işlemiyle uzun forma çevir
        year_cols = [col for col in df.columns if col.isdigit()]
        if year_cols:
            df = df.melt(id_vars=["Country"], value_vars=year_cols,
                         var_name="Year", value_name="GDP")
        else:
            raise KeyError("Veri dosyasında Year veya GDP sütunları bulunamadı.")

    # Sayısal hale getir
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")

    # Boşları sil
    df = df.dropna(subset=["Country", "Year", "GDP"])
    return df


def get_countries(df):
    #Veri setindeki ülkeleri  döndürdüm sorted ile 
    return sorted(df["Country"].dropna().unique().tolist())


def predict_gdp_for_year(df_country, year):
  
     # Basit Linear Regression ile bir ülke için GDP tahmini yaptım
   
    X = df_country[["Year"]].values
    y = df_country["GDP"].values
    model = LinearRegression()
    model.fit(X, y)
    predicted = model.predict(np.array([[year]]))[0]
    return predicted


def create_plot(df_country, country_name="Country", predicted_year=None, predicted_value=None):
    
    # Seçilen ülkenin GDP verisini ve tahminini gösteren grafiği oluşturur.
   
    plt.figure(figsize=(10, 5))
    plt.plot(df_country["Year"], df_country["GDP"], 'o-', color='teal', label='Historical GDP')

    # Tahmin çizgisi
    X = df_country[["Year"]].values
    y = df_country["GDP"].values
    model = LinearRegression()
    model.fit(X, y)
    future_years = np.arange(df_country["Year"].min(), (df_country["Year"].max() + 2)).reshape(-1, 1)
    plt.plot(future_years, model.predict(future_years), '--', color='orange', label='Trend')

    # Kullanıcı girdisine göre tahmin edilen nokta
    if predicted_year and predicted_value:
        plt.scatter(predicted_year, predicted_value, color='red', s=80, label='Predicted (Your Input)')
        plt.text(predicted_year + 0.2, predicted_value, f"{predicted_value:,.0f}", color='red')

    plt.title(f"GDP Trend - {country_name}")
    plt.xlabel("Year")
    plt.ylabel("GDP (Billion USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Kaydet
    static_path = os.path.join("static", "plot.png")
    plt.savefig(static_path)
    plt.close()


