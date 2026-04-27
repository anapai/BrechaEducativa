import pandas as pd

df = pd.read_csv("BrechaEducativa/data/serie_historica_entidades_sep.csv", encoding="latin1")

df.columns = df.columns.str.strip()

df_long = df.melt(
    id_vars=["Estado", "Sector", "Tipo"],
    var_name="Año",
    value_name="Matricula"
)

df_long["Matricula"] = df_long["Matricula"].astype(str).str.replace(",", "")
df_long["Matricula"] = pd.to_numeric(df_long["Matricula"], errors="coerce")
df_long["Año"] = df_long["Año"].astype(int)

df_filtrado = df_long[df_long["Tipo"].isin(["PÚBLICO", "PRIVADO"])]

print(df_filtrado.head())
print(df_filtrado.shape)