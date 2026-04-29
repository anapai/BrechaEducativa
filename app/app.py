from shiny import App, ui, reactive
from shinywidgets import output_widget, render_widget

import plotly.express as px
import json

COLOR_FONDO = "#f7f3ef"
COLOR_VERDE_OSCURO = "#10312b"
COLOR_VINO = "#621132"
COLOR_DORADO = "#bc955c"
COLOR_TARJETA = "#ffffff"

COLORES_TIPO = {
    "PUBLICO": "#621132",
    "PRIVADO": "#bc955c"
}
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
equivalencias_estados = {
    "Ciudad de Mexico": "Ciudad de México",
    "Coahuila": "Coahuila de Zaragoza",
    "Collima": "Colima",
    "Mexico": "México",
    "Michoacan": "Michoacán de Ocampo",
    "Nuevo Leon": "Nuevo León",
    "Queretaro": "Querétaro",
    "Veracruz": "Veracruz de Ignacio de la Llave",
    "Yucatan": "Yucatán"
}

df_filtrado["Estado_mapa"] = df_filtrado["Estado"].replace(equivalencias_estados)
with open("data/states_full.geojson", "r", encoding="utf-8") as f:
    geojson_mexico = json.load(f)

app_ui = ui.page_fluid(
    ui.tags.style("""
        body {
            background-color: #f7f3ef;
            font-family: Arial, sans-serif;
            color: #1f2933;
        }

        .titulo {
            background: linear-gradient(135deg, #621132, #10312b);
            color: white;
            padding: 34px;
            border-radius: 18px;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0px 4px 14px rgba(0,0,0,0.25);
        }

        .filtros {
            background-color: #ffffff;
            padding: 22px;
            border-radius: 16px;
            margin-bottom: 25px;
            border-left: 8px solid #bc955c;
            box-shadow: 0px 3px 12px rgba(0,0,0,0.12);
        }

        .contenedor {
            background-color: #ffffff;
            padding: 26px;
            border-radius: 16px;
            margin-bottom: 28px;
            box-shadow: 0px 3px 12px rgba(0,0,0,0.12);
        }

        h3 {
            color: #621132;
        }

        p {
            color: #334155;
            font-size: 16px;
        }
    """),

    ui.div(
        ui.h3("Pregunta de investigación"),
        ui.p("¿Cómo se distribuye la matrícula entre educación pública y privada en México, y cómo cambia esta diferencia según el estado, el nivel educativo y el año?"),

        ui.h3("Hipótesis"),
        ui.p("La educación pública concentra la mayor parte de la matrícula en México; sin embargo, la participación de la educación privada varía según el nivel educativo y la entidad federativa."),

        ui.h3("Narrativa del análisis"),
        ui.p("Primero se observa la evolución nacional de la matrícula pública y privada. Después, se comparan los niveles educativos para identificar dónde la participación privada tiene mayor peso. Finalmente, se analiza la brecha territorial entre estados mediante un ranking y un mapa interactivo."),

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
    ui.p("El primer paso es observar la tendencia nacnal: la matrícula pública domina el sistema educativo, pero la comparación con la matrícula privada permite identificar cambios a lo largo del tiempo."),
        ui.p("Esta gráfica muestra la evolución de la matrícula pública y privada a lo largo de los años."),
        output_widget("grafica_tiempo"),
        class_="contenedor"
    ),

    ui.div(
    ui.p("La brecha no se comporta igual en todos los niveles educativos. Esta gráfica permite comparar en qué etapa escolar la educación privada tiene mayor o menor presencia."),
        ui.p("Esta visualización compara la matrícula pública y privada según el nivel educativo."),
        output_widget("grafica_nivel"),
        class_="contenedor"
    ),

    ui.div(
    ui.p("Después de observar el comportamiento general, esta gráfica identifica los estados donde la diferencia entre matrícula pública y privada es más amplia."),
        ui.p("Aquí se observan los estados donde la diferencia entre matrícula pública y privada es mayor."),
        output_widget("grafica_estado"),
        class_="contenedor"
    ),
    

    ui.div(
    ui.p("El mapa permite ubicar territorialmente la brecha público-privada y observar cómo cambia al seleccionar diferentes anos."),
        ui.p("El mapa muestra la diferencia de matrícula entre el sector público y privado según el año y nivel educativo seleccionado."),
        output_widget("mapa_estado"),
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
            title="Matrícula en México: Público vs Privado",
            hover_data=["Tipo", "Matricula"], 
            color_discrete_map=COLORES_TIPO
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor=COLOR_TARJETA,
            plot_bgcolor=COLOR_FONDO,
            font_color="#1f2933"
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
            hover_data=["Sector", "Tipo", "Matricula"],
            color_discrete_map=COLORES_TIPO
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor=COLOR_TARJETA,
            plot_bgcolor=COLOR_FONDO,
            font_color="#1f2933"
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
    
    @output
    @render_widget
    def mapa_estado():
        data = df_filtrado[df_filtrado["Año"] == input.anio()]

        if input.sector() != "Todos":
            data = data[data["Sector"] == input.sector()]
        df_mapa = data.groupby(["Estado", "Estado_mapa", "Tipo"])["Matricula"].sum().unstack().reset_index()
        df_mapa["Brecha"] = df_mapa["PUBLICO"] - df_mapa["PRIVADO"]

        fig = px.choropleth(
            df_mapa,
            geojson=geojson_mexico,
            locations="Estado_mapa",
            featureidkey="properties.NOMGEO",
            color="Brecha",
            hover_name="Estado",
            hover_data=["PUBLICO", "PRIVADO", "Brecha"],
            color_continuous_scale=["#f7f3ef", "#bc955c", "#621132"],
            title=f"Brecha público-privada por estado en {input.anio()}",
            
        )

        fig.update_geos(
            fitbounds="locations",
            visible=False
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor=COLOR_TARJETA,
            plot_bgcolor=COLOR_FONDO,
            font_color="#1f2933",
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )

        return fig


app = App(app_ui, server)