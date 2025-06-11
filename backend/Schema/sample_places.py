from backend.search.weav_client_ops import add_place

places = [
    "Taj Mahal", "Goa Beaches", "Jaipur Fort", "Ladakh", "Kerala Backwaters"
]

for place in places:
    add_place(place)
print("Sample data inserted.")
