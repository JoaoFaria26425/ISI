import streamlit as st  # 👈 isto precisa vir primeiro
import pandas as pd
from db import get_all_data
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="🏎️ F1 vs Assetto Corsa Leaderboard", layout="wide")

st.title("🏎️ F1 vs Assetto Corsa Leaderboard")

# ------------------------------------------------------------
# 🔹 Carregar dados
# ------------------------------------------------------------
data = get_all_data()
laps_df = data["laps"]
drivers_df = data["drivers"]
races_df = data["races"]
circuits_df = data["circuits"]

# Garantir que há dados
if laps_df.empty or drivers_df.empty or races_df.empty or circuits_df.empty:
    st.warning("Sem dados suficientes para gerar o leaderboard.")
    st.stop()

# ------------------------------------------------------------
# 🔹 Preparar dataset completo
# ------------------------------------------------------------
merged = (
    laps_df
    .merge(drivers_df, on="driver_ref", how="left")
    .merge(races_df, left_on=["season", "round"], right_on=["year", "round"], how="left")
    .merge(circuits_df, on="circuit_ref", how="left", suffixes=("", "_circuit"))
)

# Verifica nome do circuito
if "name" in merged.columns:
    circuit_col = "name"
elif "circuit" in merged.columns:
    circuit_col = "circuit"
elif "circuit_ref" in merged.columns:
    circuit_col = "circuit_ref"
else:
    st.error("❌ Nenhuma coluna de circuito encontrada (name, circuit ou circuit_ref).")
    st.stop()

# ------------------------------------------------------------
# 🔹 Filtros (Season, Round, Circuito)
# ------------------------------------------------------------

# Season
season_list = sorted(merged["season"].dropna().unique().tolist(), reverse=True)
season_selected = st.selectbox("📅 Escolhe a Season", season_list)

# Filtrar rounds dessa season
round_list = sorted(merged[merged["season"] == season_selected]["round"].dropna().unique().tolist())
round_selected = st.selectbox("🔁 Escolhe o Round", round_list)

# Filtrar corridas dessa season/round
filtered_round = merged[(merged["season"] == season_selected) & (merged["round"] == round_selected)]

# Circuitos disponíveis
circuit_list = filtered_round[circuit_col].dropna().unique().tolist()
circuit_selected = st.selectbox("🏁 Escolhe o Circuito", sorted(circuit_list))

# ------------------------------------------------------------
# 🔹 Filtrar dados do circuito selecionado
# ------------------------------------------------------------
circuit_data = filtered_round[filtered_round[circuit_col] == circuit_selected]

if circuit_data.empty:
    st.warning("Sem voltas disponíveis para este circuito.")
    st.stop()

# ------------------------------------------------------------
# 🔹 Calcular tempos e leaderboard
# ------------------------------------------------------------
if "milliseconds" in circuit_data.columns:
    circuit_data["lap_time_ms"] = pd.to_numeric(circuit_data["milliseconds"], errors="coerce")
else:
    circuit_data["lap_time_ms"] = pd.to_numeric(circuit_data["lap_time"], errors="coerce")

# Agrupar por piloto
leaderboard = (
    circuit_data.groupby(["forename", "surname"], dropna=False)
    .agg(
        best_lap_ms=("lap_time_ms", "min"),
        avg_lap_ms=("lap_time_ms", "mean")
    )
    .reset_index()
)

# Converter tempos para segundos
leaderboard["Melhor Volta (s)"] = (leaderboard["best_lap_ms"] / 1000).round(3)
leaderboard["Média (s)"] = (leaderboard["avg_lap_ms"] / 1000).round(3)

# Ordenar pela melhor volta
leaderboard = leaderboard.sort_values("best_lap_ms", ascending=True).reset_index(drop=True)

# Criar coluna de posição
leaderboard.insert(0, "Posição 🏁", leaderboard.index + 1)

# Renomear colunas
leaderboard_display = leaderboard[["Posição 🏁", "forename", "surname", "Melhor Volta (s)", "Média (s)"]].rename(
    columns={
        "forename": "Nome",
        "surname": "Apelido"
    }
)

# Mostrar leaderboard
st.subheader(f"🏆 Leaderboard — Season {season_selected}, Round {round_selected}: {circuit_selected}")
st.data_editor(
    leaderboard_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Posição 🏁": st.column_config.Column("Posição 🏁", width="small"),
        "Nome": st.column_config.Column("Nome", width="medium"),
        "Apelido": st.column_config.Column("Apelido", width="medium"),
        "Melhor Volta (s)": st.column_config.Column("Melhor Volta (s)", width="medium"),
        "Média (s)": st.column_config.Column("Média (s)", width="medium"),
    },
    disabled=True,
)

# ------------------------------------------------------------
# 🔹 Mostrar imagem do circuito (do Wikipedia)
# ------------------------------------------------------------
from PIL import Image
import requests
from io import BytesIO

search_name = circuit_selected.replace(" ", "_") + "_circuit"
image_url = f"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/{search_name}.png/800px-{search_name}.png"

try:
    response = requests.get(image_url, timeout=5)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f"{circuit_selected} Circuit", use_container_width=True)
    else:
        st.warning(f"🔎 Não encontrei imagem automática para **{circuit_selected}**.")
except Exception as e:
    st.warning(f"⚠️ Erro ao carregar imagem: {e}")