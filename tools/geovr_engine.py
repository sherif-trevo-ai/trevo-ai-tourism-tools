import math

class TrevoGeoVREngine:
    """
    Trevo Geospatial VR Engine (Alpha)
    Bridges real-world GPS coordinates with immersive 360° VR content.
    Part of the Trevo AI Tourism Tools ecosystem.
    """
    
    def __init__(self):
        # Database of VR hotspots: {id: {"lat": float, "lng": float, "vr_url": str}}
        self.vr_hotspots = {}

    def add_vr_hotspot(self, spot_id, lat, lng, vr_url, metadata=None):
        """Adds a new VR experience linked to specific GPS coordinates."""
        self.vr_hotspots[spot_id] = {
            "lat": lat,
            "lng": lng,
            "vr_url": vr_url,
            "metadata": metadata or {}
        }
        return f"Hotspot {spot_id} added successfully at ({lat}, {lng})."

    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculates distance between two points using the Haversine formula."""
        R = 6371  # Earth radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def find_nearest_vr_experience(self, user_lat, user_lng, radius_km=5.0):
        """Finds the closest VR experiences within a given radius."""
        nearby_spots = []
        for spot_id, data in self.vr_hotspots.items():
            dist = self.calculate_distance(user_lat, user_lng, data['lat'], data['lng'])
            if dist <= radius_km:
                nearby_spots.append({
                    "id": spot_id,
                    "distance_km": round(dist, 2),
                    "vr_link": data['vr_url']
                })
        
        # Sort by distance
        return sorted(nearby_spots, key=lambda x: x['distance_km'])

# Example Usage for Tourism Agencies
if __name__ == "__main__":
    engine = TrevoGeoVREngine()
    
    # Adding historical sites in Egypt (Example)
    engine.add_vr_hotspot("Giza_Pyramids", 29.9792, 31.1342, "https://vr.trevo.ai/pyramids")
    engine.add_vr_hotspot("Luxor_Temple", 25.6995, 32.6391, "https://vr.trevo.ai/luxor")
    
    # Simulate a user tracking their trip on a map
    user_location = (29.9760, 31.1310) # Near Pyramids
    print(f"Searching for VR content near: {user_location}...")
    
    results = engine.find_nearest_vr_experience(user_location[0], user_location[1])
    for spot in results:
        print(f"Found: {spot['id']} at {spot['distance_km']} km. Experience here: {spot['vr_link']}")
