from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
import urllib.parse

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4173",      # local dev
        "http://localhost:5174",      # local dev vite
        "https://priyamfoods.vercel.app",  # Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    quantity: int

class Customer(BaseModel):
    first_name: str
    last_name: str
    whatsapp_number: str
    address: str
    email: EmailStr

class Order(BaseModel):
    customer: Customer
    items: List[Item]

menu = [
    {"category": "Podi", "items": [
        {"name": "Idli podi - 250gm", "price": 5.00},
        {"name": "Dosa podi - 250gm", "price": 5.00},
        {"name": "Sambar podi - 250gm", "price": 5.00},
        {"name": "Rasam podi - 250gm", "price": 5.00},
        {"name": "Paruppu podi - 250gm", "price": 5.00},
        {"name": "Curry leaves podi - 250gm", "price": 5.00},
    ]},
    {"category": "Thokku", "items": [
        {"name": "Tomato thokku - 250gm", "price": 5.00},
        {"name": "Tamarind thokku - 250gm", "price": 5.00},
        {"name": "Curry leaves thokku - 250gm", "price": 5.00},
        {"name": "Mint thokku - 250gm", "price": 5.00},
    ]},
    {"category": "Teig", "items": [
        {"name": "Idli teig - 250gm", "price": 5.00},
        {"name": "Dosa teig - 250gm", "price": 5.00},
        {"name": "Linsen teig - 250gm", "price": 5.00},
        {"name": "Millet teig - 250gm", "price": 5.00},
    ]},
    {"category": "Food", "items": [
        {"name": "Chicken biryani - 500gm", "price": 10.00},
        {"name": "Mutton biryani - 500gm", "price": 12.00},
        {"name": "Veg biryani - 500gm", "price": 8.00},
        {"name": "Paneer biryani - 500gm", "price": 9.00},
        {"name": "Egg biryani - 500gm", "price": 9.00},
        {"name": "Fish biryani - 500gm", "price": 11.00},
        {"name": "Prawn biryani - 500gm", "price": 12.00},
    ]},
]

def create_order(items):
    total_price = 0.0
    order_items = []

    menu_dict = {item["name"]: item["price"] for category in menu for item in category["items"]}
    for item_obj in items:
        item_name = item_obj.name
        quantity = item_obj.quantity

        if item_name not in menu_dict:
            return {"error": f"Item '{item_name}' not found"}

        price = menu_dict[item_name]
        total = price * quantity
        total_price += total

        order_items.append({
            "item": item_name,
            "quantity": quantity,
            "price": price,
            "total": total
        })

    return {
        "orders": order_items,
        "total_price": total_price
    }


@app.get("/menu")
def get_menu():
    return menu

@app.post("/order")
def create_order_endpoint(order: Order):
    order_details = create_order(order.items)

    if "error" in order_details:
        return {"error": order_details["error"]}

    admin_whatsapp_number = "919840606082"  # Replace with actual admin number
    whatsapp_message = generate_whatsapp_message(order_details, order.customer)
    wa_link = generate_whatsapp_link(admin_whatsapp_number, whatsapp_message)

    return {
        #"order_details": order_details,
        "message": whatsapp_message,
        "whatsapp_link": wa_link
    }

def generate_whatsapp_message(order_details, customer: Customer):
    message = "Hallo, \n* My Order Details:*\n🛒"
    for item in order_details["orders"]:
        message += f"{item['quantity']} x {item['item']} | {item['quantity']} x ${item['price']:.2f} = ${item['total']:.2f}\n"
    message += f"Total Price: ${order_details['total_price']:.2f}\n\n"
    message += f"🧾 *Name: {customer.first_name} {customer.last_name}*\n"
    message += f"🏠 Address: {customer.address}\n"
    message += f"📧 Email: {customer.email}\n"
    message += f"📞 WhatsApp: {customer.whatsapp_number}\n\n"    
    return message

def generate_whatsapp_link(number, message):
    # message = generate_whatsapp_message(order_details, customer)
    encoded_message = urllib.parse.quote(message)
    wa_link = f"https://wa.me/{number}?text={encoded_message}"
    return wa_link