
from flask import Flask, render_template, request
import model
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    prediction = None
    predicted_gdp = None
    predicted_year = None
    selected_country = None

    # veri yükle
    try:
        df = model.load_data()
    except Exception as e:
        return render_template("index.html", error=f"Veri yüklenemedi: {e}", countries=[], selected_country=None, prediction=None)

    countries = model.get_countries(df)
    selected_country = request.form.get("country") if request.method == "POST" else ("Japan" if "Japan" in countries else (countries[0] if countries else None))
    df_country = df[df["Country"] == selected_country].sort_values("Year") if selected_country else df.sort_values("Year")

    if request.method == "POST":
        try:
            interest = float(request.form.get("interest", 0))
            inflation = float(request.form.get("inflation", 0))
            gdp_growth = float(request.form.get("gdp", 0))

            # Gelecek yıl GDP tahmini
            last_year = int(df_country["Year"].max())
            predicted_year = last_year + 1

            # Linear Regression ile tahmin edilen baz GDP
            base_predicted_gdp = model.predict_gdp_for_year(df_country, predicted_year)

            # Kullanıcı girdilerine göre GDP tahminini ayarlıyoruz
            # Pozitif etki: gdp_growth (+), Negatif etki: inflation (-), interest (-)
            adjusted_gdp = base_predicted_gdp * (1 + gdp_growth / 100 - inflation / 200 - interest / 300)
            predicted_gdp = adjusted_gdp

            # Basit hisse fiyat tahmini
            share_price = predicted_gdp * 0.002  # örnek oransal ilişki
            prediction = round(share_price, 2)
        except Exception as e:
            error = f"Hata: {e}"
            prediction = None

    # grafik oluştur
    try:
        model.create_plot(df_country, country_name=selected_country or "Country",
                          predicted_year=predicted_year, predicted_value=predicted_gdp)
    except Exception as e:
        error = (error + " | Grafik hata: " + str(e)) if error else ("Grafik hata: " + str(e))

    return render_template("index.html", error=error, prediction=prediction,
                           countries=countries, selected_country=selected_country)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request
import model
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    prediction = None
    predicted_gdp = None
    predicted_year = None
    selected_country = None

    # veri yükle
    try:
        df = model.load_data()
    except Exception as e:
        return render_template("index.html", error=f"Veri yüklenemedi: {e}", countries=[], selected_country=None, prediction=None)

    countries = model.get_countries(df)
    selected_country = request.form.get("country") if request.method == "POST" else ("Japan" if "Japan" in countries else (countries[0] if countries else None))
    df_country = df[df["Country"] == selected_country].sort_values("Year") if selected_country else df.sort_values("Year")

    if request.method == "POST":
        try:
            interest = float(request.form.get("interest", 0))
            inflation = float(request.form.get("inflation", 0))
            gdp_growth = float(request.form.get("gdp", 0))

            # Gelecek yıl GDP tahmini
            last_year = int(df_country["Year"].max())
            predicted_year = last_year + 1

            # Linear Regression ile tahmin edilen baz GDP
            base_predicted_gdp = model.predict_gdp_for_year(df_country, predicted_year)

            # Kullanıcı girdilerine göre GDP tahminini ayarlıyoruz
            # Pozitif etki: gdp_growth , Negatif etki: inflation , interest 
            adjusted_gdp = base_predicted_gdp * (1 + gdp_growth / 100 - inflation / 200 - interest / 300)
            predicted_gdp = adjusted_gdp

            # Basit hisse fiyat tahmini
            share_price = predicted_gdp * 0.002  # örnek oransal ilişki
            prediction = round(share_price, 2)
        except Exception as e:
            error = f"Hata: {e}"
            prediction = None

    # grafik oluştur
    try:
        model.create_plot(df_country, country_name=selected_country or "Country",
                          predicted_year=predicted_year, predicted_value=predicted_gdp)
    except Exception as e:
        error = (error + " | Grafik hata: " + str(e)) if error else ("Grafik hata: " + str(e))

    return render_template("index.html", error=error, prediction=prediction,
                           countries=countries, selected_country=selected_country)

if __name__ == "__main__":
    app.run(debug=True)
