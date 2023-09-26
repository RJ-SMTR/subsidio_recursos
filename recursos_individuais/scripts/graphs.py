import folium
import io
import pandas as pd
from PIL import Image
from shapely import wkt


def create_point_element_map(map_point, color, tooltip):
    return folium.Circle(
        location=[map_point.y, map_point.x],
        radius=10,
        fill=True,
        fill_opacity=1,
        color=color,
        tooltip=tooltip,
    )


def create_marker_element_map(map_point, color, tooltip):
    return folium.Marker(
        location=[map_point.y, map_point.x],
        icon=folium.Icon(color=color),
        tooltip=tooltip,
    )


def create_radius_element_map(
    map_point, color, tooltip, weight=0.3, fill=True, radius=500
):
    return folium.Circle(
        location=[map_point.y, map_point.x],
        radius=radius,
        weight=weight,
        fill=True,
        fill_opacity=0.1,
        color=color,
        tooltip=tooltip,
    )


def create_polyline_element_map(line, color):
    return folium.PolyLine(line, color=color, line_weight=5)


def create_trip_map(posicoes, shapes_geom):
    """
    Cria um mapa iterativo (html) comparando as posições de GPS de um veículo
    num determinado período com o shape do serviço operado.

    posicoes (pd.DataFrame): Tabela de posições de GPS. Deve conter as colunas:
    id_veiculo,servico,timestamp_gps,posicao_veiculo_geo,status_viagem(opcional);

    shapes_geom (pd.DataFrame): Tabela do shape em linestring. Deve
    conter as colunas: shape_id,shape,start_pt,end_pt;
    """
    # Gera layout do mapa
    title = f"""
    <h4 align='center' style='font-size:16px'><b>Posições de GPS do período/viagem</b><br><br>
    Serviço: {posicoes.servico.iloc[0]}; Veículo: {posicoes.id_veiculo.iloc[0]}; Horário:
    {posicoes.timestamp_gps.min()} a {posicoes.timestamp_gps.max()}</h4>
    """

    # f = folium.Figure(width=800, height=600)

    mapa = folium.Map(
        location=[-22.908333, -43.396388],
        zoom_start=11,
        width=1200,
        height=800,
    )

    mapa.get_root().html.add_child(folium.Element(title))

    # colors = ["#fc0000", "#00b7ff", "#00FF00"]

    status_colors = {"start": "green", "middle": "blue", "end": "red", "out": "gray"}

    shape_colors = ["red", "green"]

    # Adiciona posições do GPS
    feature_gps_radius = folium.FeatureGroup(name="gps_radius")
    feature_gps_points = folium.FeatureGroup(name="gps_points")

    posicoes["posicao_veiculo_geo"] = posicoes["posicao_veiculo_geo"].astype(str)
    posicoes["posicao_veiculo_geo"] = posicoes["posicao_veiculo_geo"].apply(wkt.loads)


    for _, p in posicoes.iterrows():
        ## Define cor padrão de status "out" quando GPS não é classificado
        if "status_viagem" in posicoes.columns:
            status = p.status_viagem
        else:
            status = "out"

        ## Adiciona raio da posição classificada pelo status
        create_radius_element_map(
            map_point=p.posicao_veiculo_geo,
            color=status_colors[status],
            tooltip=f"{p['timestamp_gps']} - Status: ({status})",  # ({p['status']})
            #tooltip=f"{p.timestamp_gps} - Status: ({p.status_viagem})",
            radius=100,
        ).add_to(feature_gps_radius)

        ## Adiciona a posição de GPS classificada pelo status (centro do raio)
        create_point_element_map(
            map_point=p.posicao_veiculo_geo,
            color=status_colors[status],
            tooltip=f"{p['timestamp_gps']} - Status: ({status})",
            # tooltip=f"{p.timestamp_gps} - Status: ({p.status_viagem})",
        ).add_to(feature_gps_points)

    ## Adiciona o(s) shape(s)
    list_shape_id = shapes_geom.shape_id.unique()

    for idx, shape_id in enumerate(list_shape_id):
        feature_shape = folium.FeatureGroup(name="shape: " + shape_id)

        df_shape = shapes_geom[shapes_geom.shape_id == shape_id]
        shape = wkt.loads(df_shape["shape"].values[0])
        start_pt = wkt.loads(df_shape["start_pt"].values[0])
        end_pt = wkt.loads(df_shape["end_pt"].values[0])

        if shape.geom_type == "LineString":
            line = [[y, x] for x, y in shape.coords]
        else:
            line = []
            for s in shape.geoms:
                for x, y in s.coords:
                    line.append([y, x])

        create_polyline_element_map(line, shape_colors[idx]).add_to(feature_shape)

        ## Ponto inicial do shape:

        create_marker_element_map(
            map_point=start_pt,
            color=shape_colors[idx],
            tooltip=f"Ponto inicial - Shape: {shape_id}",
        ).add_to(feature_shape)

        create_radius_element_map(
            map_point=start_pt,
            color=shape_colors[idx],
            tooltip=f"Ponto inicial - Shape: {shape_id}",
            fill=True,
            weight=3,
        ).add_to(feature_shape)

        create_radius_element_map(
            map_point=end_pt,
            color=shape_colors[idx],
            tooltip=f"Ponto inicial - Shape: {shape_id}",
            fill=True,
            weight=3,
        ).add_to(feature_shape)

        feature_shape.add_to(mapa)

    # Adiciona camada de GPS acima do shape
    feature_gps_radius.add_to(mapa)
    feature_gps_points.add_to(mapa)

    folium.TileLayer("cartodbpositron").add_to(mapa)
    folium.TileLayer("cartodbdark_matter").add_to(mapa)
    # other mapping code (e.g. lines, markers etc.)
    folium.LayerControl(collapsed=False).add_to(mapa)

    return mapa


if __name__ == "__main__":
    posicoes = pd.read_csv("data_graph_test/gps_check.csv") # gps_pre.csv

    shapes = pd.read_csv("data_graph_test/shape_check.csv")
    title = "nome_do_mapa"  # definir quando for criar

    # Cria mapa da viagem  - TODO: adicionar sentido no tooltip do shape
    map = create_trip_map(posicoes=posicoes, shapes_geom=shapes)

    # Salva em html - TODO: ver como salvar em png
    map.save(f"data_graph_test/{title}.html")