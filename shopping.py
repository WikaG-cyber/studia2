import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj dane z pliku CSV, korzystając z funkcji z pamięcią podręczną (cache) Streamlit
@st.cache
def load_data():
    try:
        # Próba wczytania danych z pliku CSV
        return pd.read_csv('shopping_trends.csv')
    except FileNotFoundError:
        # Obsługa błędu, gdy plik nie zostanie znaleziony
        st.error("Plik 'shopping_trends.csv' nie został znaleziony.")
        return pd.DataFrame()  # Zwrócenie pustej ramki danych w przypadku błędu

# Wczytaj dane do zmiennej `data`
data = load_data()

# Sprawdź, czy dane zostały poprawnie załadowane (nie są puste)
if not data.empty:
    # Ustawienia strony głównej
    st.title("Shopping Trends Dashboard")  # Tytuł głównego dashboardu
    st.sidebar.title("Opcje analizy")  # Tytuł paska bocznego z opcjami

    # --- Definicja filtrów ---
    # Filtr wieku klientów
    age_filter = st.sidebar.slider(
        "Wiek klienta",  # Nazwa suwaka
        int(data["Age"].min()),  # Minimalna wartość
        int(data["Age"].max()),  # Maksymalna wartość
        (18, 60)  # Domyślny przedział
    )
    # Filtr kategorii produktów
    category_filter = st.sidebar.multiselect(
        "Kategorie produktów",  # Nazwa filtra
        data["Category"].unique(),  # Lista unikalnych kategorii
        data["Category"].unique()  # Domyślnie wybrane wszystkie kategorie
    )
    # Filtr sezonu zakupów
    season_filter = st.sidebar.multiselect(
        "Sezon",
        data["Season"].unique(),
        data["Season"].unique()
    )
    # Filtr kwoty zakupów
    purchase_filter = st.sidebar.slider(
        "Kwota zakupów (USD)",
        int(data["Purchase Amount (USD)"].min()),
        int(data["Purchase Amount (USD)"].max()),
        (0, 500)  # Domyślny przedział kwot
    )

    # --- Filtrowanie danych ---
    # Tworzenie filtrowanej ramki danych na podstawie wybranych kryteriów
    filtered_data = data[
        (data["Age"] >= age_filter[0]) &  # Zakres wieku
        (data["Age"] <= age_filter[1]) &
        (data["Category"].isin(category_filter)) &  # Wybrane kategorie
        (data["Season"].isin(season_filter)) &  # Wybrane sezony
        (data["Purchase Amount (USD)"] >= purchase_filter[0]) &  # Minimalna kwota
        (data["Purchase Amount (USD)"] <= purchase_filter[1])  # Maksymalna kwota
    ]

    # Wyświetlenie przefiltrowanych danych w tabeli
    st.write("### Filtrowane dane", filtered_data)

    # --- Wykresy ---
    st.write("## Analiza wizualna")  # Sekcja z wykresami

    if not filtered_data.empty:
        # Wykres 1: Liczba zakupów w podziale na kategorie
        st.write("### Liczba zakupów wg kategorii")
        category_counts = filtered_data["Category"].value_counts()  # Zliczanie zakupów dla każdej kategorii
        fig, ax = plt.subplots()
        category_counts.plot(kind="bar", ax=ax)  # Wykres słupkowy
        ax.set_xlabel("Kategoria")
        ax.set_ylabel("Liczba zakupów")
        st.pyplot(fig)  # Wyświetlenie wykresu w Streamlit

        # Wykres 2: Średnia kwota zakupów w podziale na sezony
        st.write("### Średnia kwota zakupów wg sezonu")
        season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()  # Oblicz średnie
        fig, ax = plt.subplots()
        season_mean.plot(kind="bar", ax=ax)
        ax.set_xlabel("Sezon")
        ax.set_ylabel("Średnia kwota zakupów (USD)")
        st.pyplot(fig)

        # Wykres 3: Rozkład liczby klientów wg wieku
        st.write("### Liczba klientów wg wieku")
        fig, ax = plt.subplots()
        filtered_data["Age"].hist(bins=20, ax=ax)  # Histogram liczby klientów
        ax.set_xlabel("Wiek")
        ax.set_ylabel("Liczba klientów")
        st.pyplot(fig)

        # Wykres 4: Rozrzut wieku vs kwota zakupów
        st.write("### Wykres rozrzutu: Wiek vs Kwota zakupów")
        fig, ax = plt.subplots()
        ax.scatter(filtered_data["Age"], filtered_data["Purchase Amount (USD)"], alpha=0.7)  # Wykres rozrzutu
        ax.set_xlabel("Wiek")
        ax.set_ylabel("Kwota zakupów (USD)")
        st.pyplot(fig)

        # Wykres 5: Udział kategorii produktów w zakupach (wykres kołowy)
        st.write("### Udział kategorii produktów w zakupach")
        fig, ax = plt.subplots()
        category_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax)  # Wykres kołowy z procentami
        ax.set_ylabel("")  # Usunięcie etykiety dla lepszego wyglądu
        st.pyplot(fig)

        # Wykres 6: Analiza najpopularniejszego dnia tygodnia
        st.write("### Najpopularniejszy dzień tygodnia")
        if "Day of Week" in data.columns:
            day_counts = filtered_data["Day of Week"].value_counts()  # Zliczanie zakupów wg dni tygodnia
            st.write("Najczęstszy dzień zakupów:", day_counts.idxmax())  # Wyświetlenie najczęstszego dnia
            fig, ax = plt.subplots()
            day_counts.plot(kind="bar", ax=ax)
            ax.set_xlabel("Dzień tygodnia")
            ax.set_ylabel("Liczba zakupów")
            st.pyplot(fig)
        else:
            st.write("Brak danych o dniach tygodnia.")

        # Wykres 7: Średnia kwota zakupów w przedziałach wiekowych
        st.write("### Średnia kwota zakupów w przedziałach wiekowych")
        bins = range(int(data["Age"].min()), int(data["Age"].max()) + 10, 10)  # Tworzenie przedziałów wiekowych
        filtered_data["Age Group"] = pd.cut(filtered_data["Age"], bins=bins)  # Grupowanie wieku
        age_group_means = filtered_data.groupby("Age Group")["Purchase Amount (USD)"].mean()  # Obliczanie średnich kwot
        fig, ax = plt.subplots()
        age_group_means.plot(kind="bar", ax=ax)
        ax.set_xlabel("Grupa wiekowa")
        ax.set_ylabel("Średnia kwota zakupów (USD)")
        st.pyplot(fig)
    else:
        # Informacja, jeśli po filtracji brak danych
        st.write("Brak danych spełniających podane kryteria filtrowania.")


