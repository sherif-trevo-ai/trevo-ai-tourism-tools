# ROI Calculator for Tourism Businesses

def calculate_roi(revenue, cost):
    """
    Calculate Return on Investment (ROI)

    ROI = (Revenue - Cost) / Cost * 100
    """

    if cost == 0:
        return "Cost cannot be zero"

    roi = (revenue - cost) / cost * 100
    return round(roi, 2)


print("Tourism ROI Calculator")

revenue = float(input("Enter total revenue: "))
cost = float(input("Enter total cost: "))

result = calculate_roi(revenue, cost)

print("ROI:", result, "%")
