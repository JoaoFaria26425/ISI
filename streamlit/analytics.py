import pandas as pd

def analyze_laps(laps_df, drivers_df, races_df, circuits_df, ac_laps_df):
    # ⚙️ Normalizar tipos
    for df, col in [
        (laps_df, "season"),
        (laps_df, "round"),
        (races_df, "year"),
        (races_df, "round"),
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # ⚙️ Merge em 3 etapas
    merged = (
        laps_df
        .merge(drivers_df, on="driver_ref", how="left")
        .merge(races_df, left_on=["season", "round"], right_on=["year", "round"], how="left")
    )

    # Adiciona info de circuito (races → circuits)
    if "circuit_ref" in merged.columns and "circuit_ref" in circuits_df.columns:
        merged = merged.merge(circuits_df, on="circuit_ref", how="left")

    if merged.empty:
        print("⚠️ Merge resultou vazio — verifica correspondência entre season/year e round.")
        return pd.DataFrame()

    # ⚙️ Determinar o tempo da volta
    if "milliseconds" in merged.columns:
        merged["lap_time_ms"] = merged["milliseconds"]
    elif "lap_time" in merged.columns:
        merged["lap_time_ms"] = pd.to_numeric(merged["lap_time"], errors="coerce")
    else:
        raise KeyError("❌ Nenhuma coluna de tempo ('milliseconds' ou 'lap_time') encontrada!")

    merged = merged.dropna(subset=["lap_time_ms"])

    # ⚙️ Nome do circuito
    circuit_col = None
    for c in ["name", "circuit_name", "circuit", "track", "location"]:
        if c in merged.columns:
            circuit_col = c
            break
    if not circuit_col:
        raise KeyError("❌ Nenhuma coluna de nome de circuito encontrada!")

    # ⚙️ Média por circuito (F1)
    f1_avg = (
        merged.groupby(circuit_col, dropna=False)["lap_time_ms"]
        .mean()
        .reset_index()
        .rename(columns={circuit_col: "circuit_name", "lap_time_ms": "f1_avg_lap_ms"})
    )

    # ⚙️ Média por circuito (Assetto Corsa)
    if not ac_laps_df.empty and "circuit" in ac_laps_df.columns:
        ac_avg = (
            ac_laps_df.groupby("circuit", dropna=False)["lap_time_ms"]
            .mean()
            .reset_index()
            .rename(columns={"lap_time_ms": "ac_avg_lap_ms"})
        )
    else:
        ac_avg = pd.DataFrame(columns=["circuit", "ac_avg_lap_ms"])

    # ⚙️ Comparação
    comparison = f1_avg.merge(ac_avg, left_on="circuit_name", right_on="circuit", how="outer")
    comparison["diff_ms"] = comparison["ac_avg_lap_ms"] - comparison["f1_avg_lap_ms"]
    comparison = comparison.fillna(0).sort_values(by="diff_ms", ascending=True)

    print(f"✅ Análise concluída — {len(comparison)} circuitos comparados.")
    return comparison
