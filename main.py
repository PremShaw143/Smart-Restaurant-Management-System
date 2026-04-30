from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

Menu = {
    'Burger': 50, 'Pizza': 120, 'Cola': 60, 'Pasta': 150, 'Coffee': 70,
    'Sandwich': 90, 'Ice Cream': 90, 'Tea': 50, 'Samosa': 30, 'Chai': 40,
    'Pav Bhaji': 120, 'Chole': 140, 'Vada Pav': 50, 'Dosa': 130, 'Paneer': 180
}

Sales_Report = {}

class OrderItem(BaseModel):
    item: str
    quantity: int

@app.get("/")
def home():
    return {"message": "Restaurant API Running 🚀"}

@app.get("/menu")
def get_menu():
    return Menu

@app.post("/order")
def place_order(order: OrderItem):
    item = order.item.title()
    if item not in Menu:
        raise HTTPException(status_code=404, detail="Item not available")
    
    cost = Menu[item] * order.quantity
    Sales_Report[item] = Sales_Report.get(item, 0) + order.quantity
    
    return {"item": item, "quantity": order.quantity, "cost": cost}

@app.get("/sales")
def get_sales():
    return Sales_Report