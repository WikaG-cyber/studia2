import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj dane
@st.cache
def load_data():
    try:
        return pd.read_csv('shopping_trends.csv')
    except FileNotFoundError:
        st.error("Plik 'shopping_trends.csv' nie został znaleziony.")
        return pd.DataFrame()  # Zwróć pustą ramkę danych

data = load_data()

if not data.empty:
    # Ustawienia strony
    st.title("Shopping Trends Dashboard")
    st.sidebar.title("Opcje analizy")

    # Filtry
    age_filter = st.sidebar.slider(
        "Wiek klienta", 
        int(data["Age"].min()), 
        int(data["Age"].max()), 
        (18, 60)
    )
    category_filter = st.sidebar.multiselect(
        "Kategorie produktów", 
        data["Category"].unique(), 
        data["Category"].unique()
    )
    season_filter = st.sidebar.multiselect(
        "Sezon", 
        data["Season"].unique(), 
        data["Season"].unique()
    )
    purchase_filter = st.sidebar.slider(
        "Kwota zakupów (USD)", 
        int(data["Purchase Amount (USD)"].min()), 
        int(data["Purchase Amount (USD)"].max()), 
        (0, 500)
    )

    # Filtruj dane
    filtered_data = data[
        (data["Age"] >= age_filter[0]) &
        (data["Age"] <= age_filter[1]) &
        (data["Category"].isin(category_filter)) &
        (data["Season"].isin(season_filter)) &
        (data["Purchase Amount (USD)"] >= purchase_filter[0]) &
        (data["Purchase Amount (USD)"] <= purchase_filter[1])
    ]

    # Wyświetlanie danych
    st.write("### Filtrowane dane", filtered_data)

    # Wykresy
    st.write("## Analiza wizualna")

    if not filtered_data.empty:
        # Wykres 1: Zakupy wg kategorii
        st.write("### Liczba zakupów wg kategorii")
        category_counts = filtered_data["Category"].value_counts()
        fig, ax = plt.subplots()
        category_counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Kategoria")
        ax.set_ylabel("Liczba zakupów")
        st.pyplot(fig)

        # Wykres 2: Średnia kwota zakupów wg sezonu
        st.write("### Średnia kwota zakupów wg sezonu")
        season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
        fig, ax = plt.subplots()
        season_mean.plot(kind="bar", ax=ax)
        ax.set_xlabel("Sezon")
        ax.set_ylabel("Średnia kwota zakupów (USD)")
        st.pyplot(fig)

        # Wykres 3: Liczba klientów wg wieku
        st.write("### Liczba klientów wg wieku")
        fig, ax = plt.subplots()
        filtered_data["Age"].hist(bins=20, ax=ax)
        ax.set_xlabel("Wiek")
        ax.set_ylabel("Liczba klientów")
        st.pyplot(fig)

        # Wykres 4 - Wykres rozrzutu
        st.write("### Wykres rozrzutu: Wiek vs Kwota zakupów")
        fig, ax = plt.subplots()
        ax.scatter(filtered_data["Age"], filtered_data["Purchase Amount (USD)"], alpha=0.7)
        ax.set_xlabel("Wiek")
        ax.set_ylabel("Kwota zakupów (USD)")
        st.pyplot(fig)

        # Wykres 5 - Wykres kołowy
        st.write("### Udział kategorii produktów w zakupach")
        fig, ax = plt.subplots()
        category_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")  # usunięcie etykiety dla lepszego wyglądu
        st.pyplot(fig)

        # Wykres 6: Najpopularniejszy dzień tygodnia
st.write("### Najpopularniejszy dzień tygodnia")
if "Day of Week" in data.columns:
    # Jeśli kolumna "Day of Week" istnieje, używamy jej
    day_counts = filtered_data["Day of Week"].value_counts()
else:
    # Jeśli brak kolumny "Day of Week", spróbujemy ją utworzyć na podstawie kolumny "Date"
    if "Date" in data.columns:
        try:
            data["Date"] = pd.to_datetime(data["Date"])
            data["Day of Week"] = data["Date"].dt.day_name()  # Utwórz kolumnę z dniami tygodnia
            filtered_data["Day of Week"] = data["Day of Week"]
            day_counts = filtered_data["Day of Week"].value_counts()
        except Exception as e:
            st.error(f"Nie udało się utworzyć kolumny 'Day of Week': {e}")
            day_counts = None
    else:
        st.warning("Brak danych o dniach tygodnia lub daty zakupów.")
        day_counts = None

if day_counts is not None:
    st.write("Najczęstszy dzień zakupów:", day_counts.idxmax())
    fig, ax = plt.subplots()
    day_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Dzień tygodnia")
    ax.set_ylabel("Liczba zakupów")
    st.pyplot(fig)
else:
    st.write("Brak danych do analizy najpopularniejszych dni tygodnia.")




        # Wykres 7: Średnia kwota zakupów w przedziałach wiekowych
        st.write("### Średnia kwota zakupów w przedziałach wiekowych")
        bins = range(int(data["Age"].min()), int(data["Age"].max()) + 10, 10)
        filtered_data["Age Group"] = pd.cut(filtered_data["Age"], bins=bins)
        age_group_means = filtered_data.groupby("Age Group")["Purchase Amount (USD)"].mean()
        fig, ax = plt.subplots()
        age_group_means.plot(kind="bar", ax=ax)
        ax.set_xlabel("Grupa wiekowa")
        ax.set_ylabel("Średnia kwota zakupów (USD)")
        st.pyplot(fig)
    else:
        st.write("Brak danych spełniających podane kryteria filtrowania.")

