from pathlib import Path
import pandas as pd
import requests
import time

CSV_PATH = Path("data/FC26_20250921.csv")
OUT_DIR = Path("assets/player_faces")

OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")

total = len(df)
baixadas = 0
ignoradas = 0
erros = 0

headers = {
    "User-Agent": "Mozilla/5.0"
}

for i, row in df.iterrows():
    player_id = row.get("player_id")
    url = row.get("player_face_url")

    if pd.isna(player_id) or pd.isna(url) or not str(url).startswith("http"):
        ignoradas += 1
        continue

    out_file = OUT_DIR / f"{int(player_id)}.png"

    if out_file.exists():
        ignoradas += 1
        continue

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            out_file.write_bytes(response.content)
            baixadas += 1
            print(f"[{i+1}/{total}] Baixada: {player_id}")
        else:
            erros += 1
            print(f"[{i+1}/{total}] Erro HTTP {response.status_code}: {player_id}")

        time.sleep(0.05)

    except Exception as e:
        erros += 1
        print(f"[{i+1}/{total}] Erro em {player_id}: {e}")

print("\nFinalizado!")
print(f"Baixadas: {baixadas}")
print(f"Ignoradas: {ignoradas}")
print(f"Erros: {erros}")
print(f"Pasta: {OUT_DIR}")