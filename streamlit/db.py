from supabase import create_client
import pandas as pd

SUPABASE_URL = "https://yuwtoyxuqjnkhsguefmr.supabase.co"  # substitui pelo teu
SUPABASE_KEY = "sb_secret_UNtoxf6NAzMgDDRwXBQ1XA_LXZSkEmo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_table(table_name):
    res = supabase.table(table_name).select("*").execute()
    return pd.DataFrame(res.data if res.data else [])

def get_all_data():
    return {
        "laps": load_table("f1_laps"),
        "drivers": load_table("f1_drivers"),
        "races": load_table("f1_races"),
        "circuits": load_table("f1_circuits"),
        "ac_laps": load_table("ac_laps")
    }
