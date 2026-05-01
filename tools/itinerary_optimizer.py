import math

class TrevoItineraryOptimizer:
    """
    Trevo Itinerary Optimizer (Alpha)
    Optimizes travel routes using a Nearest Neighbor algorithm to minimize 
    travel time and distance for tourists.
    """

    def __init__(self):
        # List of locations: {"name": str, "lat": float, "lng": float, "duration": int (mins)}
        self.locations = []

    def add_location(self, name, lat, lng, duration=60):
        """Adds a destination to the potential itinerary."""
        self.locations.append({
            "name": name,
            "lat": lat,
            "lng": lng,
            "duration": duration
        })

    def _calculate_haversine(self, lat1, lng1, lat2, lng2):
        """Internal method to calculate distance between two coordinates."""
        R = 6371.0  # Earth radius in KM
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def optimize_route(self, start_index=0):
        """
        Optimizes the sequence of locations starting from a specific point.
        Uses a greedy approach to find the most efficient path.
        """
        if not self.locations:
            return []

        unvisited = list(range(len(self.locations)))
        current_index = unvisited.pop(start_index)
        optimized_path = [self.locations[current_index]]
        total_distance = 0.0

        while unvisited:
            next_index = min(
                unvisited,
                key=lambda x: self._calculate_haversine(
                    self.locations[current_index]['lat'], 
                    self.locations[current_index]['lng'],
                    self.locations[x]['lat'], 
                    self.locations[x]['lng']
                )
            )
            
            dist = self._calculate_haversine(
                self.locations[current_index]['lat'], 
                self.locations[current_index]['lng'],
                self.locations[next_index]['lat'], 
                self.locations[next_index]['lng']
            )
            
            total_distance += dist
            current_index = unvisited.pop(unvisited.index(next_index))
            optimized_path.append(self.locations[current_index])

        return {
            "optimized_itinerary": optimized_path,
            "total_travel_distance_km": round(total_distance, 2),
            "estimated_travel_time_mins": round(total_distance * 1.5, 0) # Assuming 40km/h avg speed
        }

# Logic Testing with Beachhead Market Data (Egypt)
if __name__ == "__main__":
    optimizer = TrevoItineraryOptimizer()

    # Sample One-Day Trip in Cairo
    optimizer.add_location("Hotel (Downtown)", 30.0444, 31.2357, 0)
    optimizer.add_location("Giza Pyramids", 29.9792, 31.1342, 180)
    optimizer.add_location("Egyptian Museum", 30.0478, 31.2336, 120)
    optimizer.add_location("Khan el-Khalili", 30.0477, 31.2622, 90)
    optimizer.add_location("Cairo Citadel", 30.0299, 31.2611, 90)

    print("--- Trevo Itinerary Optimization Engine ---")
    result = optimizer.optimize_route(start_index=0)

    print(f"Total Distance: {result['total_travel_distance_km']} KM")
    print(f"Total Travel Time: {result['estimated_travel_time_mins']} Mins")
    print("\nOptimized Sequence:")
    for i, spot in enumerate(result['optimized_itinerary']):
        print(f"{i+1}. {spot['name']} ({spot['duration']} mins on site)")
