import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/serie_historica_entidades_sep.csv", encoding="latin1")
df.columns = df.columns.str.strip()

df_long = df.melt(
    id_vars=["Estado", "Sector", "Tipo"],
    var_name="Año",
    value_name="Matricula"
)

#FILTRADOSS
df_long["Matricula"] = df_long["Matricula"].astype(str).str.replace(",", "")
df_long["Matricula"] = pd.to_numeric(df_long["Matricula"], errors="coerce")
df_long["Año"] = df_long["Año"].astype(int)
df_long["Tipo"] = df_long["Tipo"].astype(str).str.strip()
df_long["Tipo"] = df_long["Tipo"].replace({
    "Pï¿½BLICO": "PUBLICO",
    "PRIVADO": "PRIVADO",
    "TOTAL": "TOTAL"
})

df_filtrado = df_long[df_long["Tipo"].isin(["PUBLICO", "PRIVADO"])]

#propuesta grafica 1
df_grafica = df_filtrado.groupby(["Año", "Tipo"])["Matricula"].sum().reset_index()
for tipo in df_grafica["Tipo"].unique():
    data = df_grafica[df_grafica["Tipo"] == tipo]
    plt.plot(data["Año"], data["Matricula"], label=tipo)
plt.title("Matrícula en México: Público vs Privado")
plt.xlabel("Año")
plt.ylabel("Matrícula")
plt.legend()






#2
df_pivot = df_filtrado.groupby(["Sector", "Tipo"])["Matricula"].sum().unstack()
df_pivot.plot(kind="bar")
plt.title("Matrícula por Nivel Educativo: Público vs Privado")
plt.xlabel("Nivel Educativo")
plt.ylabel("Matrícula")
plt.xticks(rotation=45)


#3
df_estado = df_filtrado.groupby(["Estado", "Tipo"])["Matricula"].sum().unstack()
df_estado["Diferencia"] = df_estado["PUBLICO"] - df_estado["PRIVADO"]
df_estado = df_estado.sort_values(by="Diferencia", ascending=False)
top_estados = df_estado.head(10)
top_estados["Diferencia"].plot(kind="bar")
plt.title("Estados con mayor brecha educativa (Público - Privado)")
plt.xlabel("Estado")
plt.ylabel("Diferencia de Matrícula")
plt.xticks(rotation=45)

