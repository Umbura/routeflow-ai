from typing import Optional
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from src.models import Location

class GeoService:
    """Serviço responsável pela conversão de endereços em coordenadas geográficas."""
    
    def __init__(self):
        # O user-agent é um requisito da política de uso do Nominatim (OpenStreetMap)
        self.geolocator = Nominatim(user_agent="routeflow_ai_agent_production_v1")

    def get_coordinates(self, address: str) -> Optional[Location]:
        """
        Converte um endereço (string) em um objeto Location (Lat/Lon).
        Retorna None se o endereço não for encontrado.
        """
        try:
            # Adiciona sufixo 'Brasil' para melhorar a precisão da busca
            clean_address = f"{address}, Brasil"
            loc = self.geolocator.geocode(clean_address, timeout=10)
            
            if loc:
                return Location(
                    address=address,
                    latitude=loc.latitude,
                    longitude=loc.longitude
                )
            return None
        except Exception as e:
            print(f"Erro de Geolocalização para '{address}': {e}")
            return None

class RouteOptimizer:
    """Serviço responsável pelos algoritmos de otimização de rotas (TSP)."""
    
    @staticmethod
    def optimize_nearest_neighbor(locations: list[Location]) -> list[Location]:
        """
        Implementa a heurística do Vizinho Mais Próximo (Nearest Neighbor) 
        para resolver o problema do Caixeiro Viajante (TSP).
        
        Complexidade: O(N^2) - Eficiente para rotas de entrega típicas (< 50 pontos).
        """
        if not locations:
            return []

        # Assume que o primeiro endereço da lista é o ponto de partida (Depósito)
        start = locations[0]
        start.is_start_point = True
        
        optimized_route = [start]
        remaining = locations[1:]

        while remaining:
            current = optimized_route[-1]
            
            # Encontra o ponto restante mais próximo do atual
            nearest = min(
                remaining,
                key=lambda x: geodesic(
                    (current.latitude, current.longitude),
                    (x.latitude, x.longitude)
                ).km
            )
            
            optimized_route.append(nearest)
            remaining.remove(nearest)

        return optimized_route

    @staticmethod
    def calculate_total_distance(route: list[Location]) -> float:
        """Calcula a distância total da rota em quilômetros."""
        total_km = 0.0
        for i in range(len(route) - 1):
            p1 = (route[i].latitude, route[i].longitude)
            p2 = (route[i+1].latitude, route[i+1].longitude)
            total_km += geodesic(p1, p2).km
        return round(total_km, 2)