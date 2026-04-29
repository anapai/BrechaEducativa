from shiny import App, ui, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

posibles_data = [
    BASE_DIR / "data",
    BASE_DIR / "BrechaEducativa" / "data",
    BASE_DIR.parent / "data"
]

DATA_DIR = None

for carpeta in posibles_data:
    if (carpeta / "serie_historica_entidades_sep.csv").exists():
        DATA_DIR = carpeta
        break

if DATA_DIR is None:
    raise FileNotFoundError("No se encontró la carpeta data con el archivo serie_historica_entidades_sep.csv")

COLOR_FONDO = "#f4f6f8"
COLOR_TARJETA = "#ffffff"
COLOR_TEXTO = "#1f2937"
COLOR_AZUL = "#2563eb"
COLOR_GRIS = "#64748b"

COLORES_TIPO = {
    "PUBLICO": "#2563eb",
    "PRIVADO": "#64748b"
}

df = pd.read_csv(DATA_DIR / "serie_historica_entidades_sep.csv", encoding="latin1")

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

df_filtrado = df_long[df_long["Tipo"].isin(["PUBLICO", "PRIVADO"])].copy()

app_ui = ui.page_fluid(
    ui.tags.style("""
        body {
            background-color: #f4f6f8;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #1f2937;
        }

        .titulo {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            color: white;
            padding: 42px;
            border-radius: 18px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0px 8px 24px rgba(15, 23, 42, 0.22);
        }

        .titulo h1 {
            color: white;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: 0.3px;
        }

        .titulo p {
            color: #e5e7eb;
            font-size: 17px;
        }

        .contenedor {
            background-color: white;
            padding: 28px;
            border-radius: 16px;
            margin-bottom: 26px;
            box-shadow: 0px 4px 16px rgba(15, 23, 42, 0.08);
            border: 1px solid #e5e7eb;
        }

        .filtros {
            background-color: white;
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 26px;
            border-left: 6px solid #2563eb;
            box-shadow: 0px 4px 16px rgba(15, 23, 42, 0.08);
        }
    """),

    ui.div(
        ui.h1("Educación pública vs privada en México"),
        ui.p("Análisis interactivo de matrícula por estado, nivel educativo y año."),
        class_="titulo"
    ),

    ui.div(
        ui.h3("Pregunta de investigación"),
        ui.p("¿Cómo se distribuye la matrícula entre educación pública y privada en México, y cómo cambia esta diferencia según el estado, el nivel educativo y el año?"),
        ui.h3("Hipótesis"),
        ui.p("La educación pública concentra la mayor parte de la matrícula en México; sin embargo, la participación de la educación privada varía según el nivel educativo y la entidad federativa."),
        ui.h3("Narrativa del análisis"),
        ui.p("Primero se observa la evolución nacional. Después se comparan los niveles educativos. Finalmente se analiza la brecha territorial mediante un ranking por estado."),
        class_="contenedor"
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
        ui.p("El primer paso es observar la tendencia nacional."),
        output_widget("grafica_tiempo"),
        class_="contenedor"
    ),

    ui.div(
        ui.p("Comparación por nivel educativo."),
        output_widget("grafica_nivel"),
        class_="contenedor"
    ),

    ui.div(
        ui.p("Estados con mayor brecha."),
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
        data = data[data["Año"] <= input.anio()]

        df_grafica = data.groupby(["Año", "Tipo"])["Matricula"].sum().reset_index()

        fig = px.line(
            df_grafica,
            x="Año",
            y="Matricula",
            color="Tipo",
            markers=True,
            color_discrete_map=COLORES_TIPO
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor=COLOR_TARJETA,
            plot_bgcolor=COLOR_FONDO,
            font_color=COLOR_TEXTO
        )

        return fig

    @output
    @render_widget
    def grafica_nivel():
        data = datos_filtrados()
        data = data[data["Año"] == input.anio()]

        df_nivel = data.groupby(["Sector", "Tipo"])["Matricula"].sum().reset_index()

        fig = px.bar(
            df_nivel,
            x="Sector",
            y="Matricula",
            color="Tipo",
            barmode="group",
            color_discrete_map=COLORES_TIPO
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor=COLOR_TARJETA,
            plot_bgcolor=COLOR_FONDO,
            font_color=COLOR_TEXTO
        )

        return fig

    @output
    @render_widget
    def grafica_estado():
        data = datos_filtrados()
        data = data[data["Año"] == input.anio()]

        df_estado = data.groupby(["Estado", "Tipo"])["Matricula"].sum().unstack().reset_index()

        if "PUBLICO" not in df_estado.columns or "PRIVADO" not in df_estado.columns:
            return px.bar()

        df_estado["Brecha"] = df_estado["PUBLICO"] - df_estado["PRIVADO"]
        df_estado = df_estado.sort_values(by="Brecha", ascending=False).head(10)

        fig = px.bar(
            df_estado,
            x="Estado",
            y="Brecha",
            color_discrete_sequence=[COLOR_AZUL]
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor=COLOR_TARJETA,
            plot_bgcolor=COLOR_FONDO,
            font_color=COLOR_TEXTO
        )

        return fig

app = App(app_ui, server)