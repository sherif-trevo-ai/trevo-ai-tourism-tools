# Simple Marketing Content Generator for Tourism Businesses

def generate_marketing_message(destination, duration, price, audience):
    """
    Generate a simple marketing message for a tourism offer
    """

    message = f"""
Discover an unforgettable trip to {destination} for {duration} days at an exclusive price of {price} USD.

This offer is perfect for {audience} looking for comfort, adventure, and memorable experiences.

Book now and enjoy a unique travel journey with professional service and outstanding value.
"""

    return message


print("Tourism Marketing Content Generator")

destination = input("Enter destination: ")
duration = input("Enter duration (days): ")
price = input("Enter price: ")
audience = input("Enter target audience: ")

result = generate_marketing_message(
    destination,
    duration,
    price,
    audience
)

print("\nGenerated Marketing Message:")
print(result)
