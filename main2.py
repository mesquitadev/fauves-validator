# import json
# import os
# import traceback
#
# from shapely.geometry import Point, shape
# from shapely.validation import explain_validity
# import asyncio
#
# from utils import process_geojson
#
# UPLOAD_DIR = "utils/geojson_files"
#
#
# def calcular_raio_voo(tipo, especie=None):
#     if tipo == 'MELIPONICULTOR':
#         if especie in ['Frieseomelitta silvestrii', 'Frieseomelitta longipes', 'Frieseomelitta doederleini',
#                        'Tetragonisca angustula']:
#             return 0.5
#         elif especie in ['Scaptotrigona polysticta', 'Melipona subnitida', 'Melipona seminigra',
#                          'Melipona flavolineata', 'Melipona fasciculata']:
#             return 2.5
#         else:
#             return 1.2
#     else:
#         return 1.5
#
#
# def calcular_capacidade_suporte_apicultura(area_total):
#     capacidade_suporte = area_total / 7.07
#     return round(capacidade_suporte)
#
#
# def calcular_capacidade_suporte_meliponicultura(hectares):
#     arvores_por_hectare = 570
#     quantidade_arvores = hectares * arvores_por_hectare
#     arvores_pasto = quantidade_arvores * 0.45
#     colmeias_por_hectare = arvores_pasto / 100
#     return round(colmeias_por_hectare)
#
#
# # async def process_geojson(latitude, longitude, tipo, especie=None):
# #     try:
# #         centro = Point(float(longitude), float(latitude))
# #         raio_voo_dec = calcular_raio_voo(tipo, especie)
# #         buffer = centro.buffer(raio_voo_dec * 1000)  # Convert to meters
# #
# #         areas = {}
# #
# #         for filename in os.listdir(UPLOAD_DIR):
# #             if filename.endswith('.geojson'):
# #                 file_path = os.path.join(UPLOAD_DIR, filename)
# #                 with open(file_path, 'r') as file:
# #                     geojson_data = json.load(file)
# #                     layers = geojson_data['features']
# #
# #                     for layer in layers:
# #                         geom = shape(layer['geometry'])
# #                         if not geom.is_valid:
# #                             print(f"Invalid geometry in {filename}: {explain_validity(geom)}")
# #                             continue
# #
# #                         if geom.intersects(buffer):
# #                             print(f"Intersects {layer}")
# #                             nome_camada = layer['properties']['VEGETAÇÃ']
# #                             area = float(layer['properties']['AREA (Ha)'])
# #                             if nome_camada not in areas:
# #                                 areas[nome_camada] = 0
# #                             areas[nome_camada] += area
# #
# #         area_total = (areas.get('URBANO', 0) + areas.get('ARBUSTIVO', 0) + areas.get('HERBACEO', 0))
# #         suporte_apicultura = calcular_capacidade_suporte_apicultura(area_total)
# #         pasto = calcular_capacidade_suporte_meliponicultura(areas.get('ARBOREO', 0))
# #
# #         if tipo == 'APICULTOR':
# #             return suporte_apicultura
# #         elif tipo == 'MELIPONICULTOR':
# #             return pasto
# #     except Exception as e:
# #         print('Erro:', str(e))
# #         traceback.print_exc()
#
#
# # Exemplo de uso
# latitude = -2.527237213627997
# longitude = -44.19919967651368
# tipo = 'MELIPONICULTOR'
#
#
# def main():
#     result = asyncio.run(process_geojson(latitude, longitude, tipo))
#     print(result)
#
#
# if __name__ == "__main__":
#     main()
