from shiny import App, ui, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/serie_historica_entidades_sep.csv", encoding="latin1")

df.columns = df.columns.str.strip()

df_long = df.melt(
    id_vars=["Estado", "Sector", "Tipo"],
    var_name="Año",
    value_name="Matricula"
)

df_long["Tipo"] = df_long["Tipo"].astype(str).str.strip()
df_long["Tipo"] = df_long["Tipo"].replace({
    "Pï¿½BLICO": "PUBLICO",
    "PÚBLICO": "PUBLICO",
    "PRIVADO": "PRIVADO",
    "TOTAL": "TOTAL"
})

df_long["Matricula"] = df_long["Matricula"].astype(str).str.replace(",", "")
df_long["Matricula"] = pd.to_numeric(df_long["Matricula"], errors="coerce")
df_long["Año"] = df_long["Año"].astype(int)

df_filtrado = df_long[df_long["Tipo"].isin(["PUBLICO", "PRIVADO"])]

# propuesta grafica 1
# df_grafica = df_filtrado.groupby(["Año", "Tipo"])["Matricula"].sum().reset_index()
# for tipo in df_grafica["Tipo"].unique():
#     data = df_grafica[df_grafica["Tipo"] == tipo]
#     plt.plot(data["Año"], data["Matricula"], label=tipo)
# plt.title("Matrícula en México: Público vs Privado")
# plt.xlabel("Año")
# plt.ylabel("Matrícula")
# plt.legend()

# propuesta grafica 2
# df_pivot = df_filtrado.groupby(["Sector", "Tipo"])["Matricula"].sum().unstack()
# df_pivot.plot(kind="bar")
# plt.title("Matrícula por Nivel Educativo: Público vs Privado")
# plt.xlabel("Nivel Educativo")
# plt.ylabel("Matrícula")
# plt.xticks(rotation=45)

# propuesta grafica 3
# df_estado = df_filtrado.groupby(["Estado", "Tipo"])["Matricula"].sum().unstack()
# df_estado["Diferencia"] = df_estado["PUBLICO"] - df_estado["PRIVADO"]
# df_estado = df_estado.sort_values(by="Diferencia", ascending=False)
# top_estados = df_estado.head(10)
# top_estados["Diferencia"].plot(kind="bar")
# plt.title("Estados con mayor brecha educativa (Público - Privado)")
# plt.xlabel("Estado")
# plt.ylabel("Diferencia de Matrícula")
# plt.xticks(rotation=45)

app_ui = ui.page_fluid(
    ui.tags.style("""
        body {
            background-color: #0f172a;
            font-family: Arial, sans-serif;
            color: white;
        }

        .titulo {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0px 4px 14px rgba(0,0,0,0.35);
        }

        .filtros {
            background-color: #334155;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.35);
        }

        .contenedor {
            background-color: #1e293b;
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 28px;
            box-shadow: 0px 3px 12px rgba(0,0,0,0.4);
        }

        h3 {
            color: #bfdbfe;
        }

        p {
            color: #e5e7eb;
        }
    """),

    ui.div(
        ui.h1("Educación pública vs privada en México"),
        ui.p("Análisis interactivo de matrícula por estado, nivel educativo y año."),
        class_="titulo"
    ),

    ui.div(
        ui.h3("Filtros"),
        ui.input_select(
            "estado",
            "Estado:",
            choices=["Todos"] + sorted(df_filtrado["Estado"].unique().tolist())
        ),
        ui.input_select(
            "sector",
            "Nivel educativo:",
            choices=["Todos"] + sorted(df_filtrado["Sector"].unique().tolist())
        ),
        ui.input_slider(
            "anio",
            "Año:",
            min=int(df_filtrado["Año"].min()),
            max=int(df_filtrado["Año"].max()),
            value=int(df_filtrado["Año"].max()),
            step=1
        ),
        class_="filtros"
    ),

    ui.div(
        ui.h3("1. Matrícula pública vs privada en el tiempo"),
        ui.p("Esta gráfica muestra la evolución de la matrícula pública y privada a lo largo de los años."),
        output_widget("grafica_tiempo"),
        class_="contenedor"
    ),

    ui.div(
        ui.h3("2. Matrícula por nivel educativo"),
        ui.p("Esta visualización compara la matrícula pública y privada según el nivel educativo."),
        output_widget("grafica_nivel"),
        class_="contenedor"
    ),

    ui.div(
        ui.h3("3. Estados con mayor brecha público-privada"),
        ui.p("Aquí se observan los estados donde la diferencia entre matrícula pública y privada es mayor."),
        output_widget("grafica_estado"),
        class_="contenedor"
    )
)


def server(input, output, session):

    @reactive.calc
    def datos_filtrados():
        data = df_filtrado.copy()

        if input.estado() != "Todos":
            data = data[data["Estado"] == input.estado()]

        if input.sector() != "Todos":
            data = data[data["Sector"] == input.sector()]

        return data

    @output
    @render_widget
    def grafica_tiempo():
        data = datos_filtrados()
        df_grafica = data.groupby(["Año", "Tipo"])["Matricula"].sum().reset_index()

        fig = px.line(
            df_grafica,
            x="Año",
            y="Matricula",
            color="Tipo",
            markers=True,
            title="Matrícula en México: Público vs Privado",
            hover_data=["Tipo", "Matricula"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1e293b",
            plot_bgcolor="#0f172a",
            font_color="white"
        )

        return fig

    @output
    @render_widget
    def grafica_nivel():
        data = df_filtrado[df_filtrado["Año"] == input.anio()]

        if input.estado() != "Todos":
            data = data[data["Estado"] == input.estado()]

        df_nivel = data.groupby(["Sector", "Tipo"])["Matricula"].sum().reset_index()

        fig = px.bar(
            df_nivel,
            x="Sector",
            y="Matricula",
            color="Tipo",
            barmode="group",
            title=f"Matrícula por nivel educativo en {input.anio()}",
            hover_data=["Sector", "Tipo", "Matricula"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1e293b",
            plot_bgcolor="#0f172a",
            font_color="white"
        )

        return fig

    @output
    @render_widget
    def grafica_estado():
        data = df_filtrado[df_filtrado["Año"] == input.anio()]

        if input.sector() != "Todos":
            data = data[data["Sector"] == input.sector()]

        df_estado = data.groupby(["Estado", "Tipo"])["Matricula"].sum().unstack()
        df_estado["Brecha"] = df_estado["PUBLICO"] - df_estado["PRIVADO"]
        df_estado = df_estado.sort_values(by="Brecha", ascending=False).head(10).reset_index()

        fig = px.bar(
            df_estado,
            x="Estado",
            y="Brecha",
            title=f"Top 10 estados con mayor brecha público-privada en {input.anio()}",
            hover_data=["Estado", "Brecha"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1e293b",
            plot_bgcolor="#0f172a",
            font_color="white"
        )

        return fig


app = App(app_ui, server)