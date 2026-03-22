from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# ================= MODELS =================

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"


class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True


class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


# ================= DATA =================

menu = [
{"id":1,"name":"Margherita Pizza","price":299,"category":"Pizza","is_available":True},
{"id":2,"name":"Veg Burger","price":149,"category":"Burger","is_available":True},
{"id":3,"name":"Chicken Burger","price":199,"category":"Burger","is_available":False},
{"id":4,"name":"Coke","price":59,"category":"Drink","is_available":True},
{"id":5,"name":"Chocolate Cake","price":179,"category":"Dessert","is_available":True},
{"id":6,"name":"Garlic Bread","price":129,"category":"Pizza","is_available":True}
]

orders=[]
order_counter=1
cart=[]


# ================= HELPERS =================

def find_menu_item(item_id:int):
    for item in menu:
        if item["id"]==item_id:
            return item
    return None


def calculate_bill(price:int, quantity:int, order_type:str):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total


def filter_menu_logic(category=None,max_price=None,is_available=None):

    result = menu

    if category is not None:

        result=[

        m for m in result

        if m["category"].lower()==category.lower()

        ]

    if max_price is not None:

        result=[

        m for m in result

        if m["price"]<=max_price

        ]

    if is_available is not None:

        result=[

        m for m in result

        if m["is_available"]==is_available

        ]

    return result


# ================= BASIC ROUTES =================

@app.get("/")
def home():
    return {"message":"Welcome to QuickBite Food Delivery"}


@app.get("/menu")
def get_menu():
    return {
        "menu":menu,
        "total":len(menu)
    }


@app.get("/menu/summary")
def summary():

    available=[m for m in menu if m["is_available"]]
    unavailable=len(menu)-len(available)

    categories=list(set([m["category"] for m in menu]))

    return{
        "total_items":len(menu),
        "available":len(available),
        "unavailable":unavailable,
        "categories":categories
    }


# ================= SEARCH / FILTER / SORT =================

@app.get("/menu/filter")
def filter_menu(
category:str = Query(None),
max_price:int = Query(None),
is_available:bool = Query(None)
):

    result = filter_menu_logic(category,max_price,is_available)

    return{
        "items":result,
        "count":len(result)
    }


@app.get("/menu/search")
def search_menu(keyword:str = Query(...)):

    results=[
        item for item in menu
        if keyword.lower() in item["name"].lower()
        or keyword.lower() in item["category"].lower()
    ]

    if not results:
        return{
            "message":f"No menu items found for '{keyword}'",
            "total_found":0,
            "results":[]
        }

    return{
        "keyword":keyword,
        "total_found":len(results),
        "results":results
    }


@app.get("/menu/sort")
def sort_menu(
sort_by:str = Query("price"),
order:str = Query("asc")
):

    if sort_by not in ["price","name","category"]:
        return{"error":"sort_by must be price, name or category"}

    if order not in ["asc","desc"]:
        return{"error":"order must be asc or desc"}

    sorted_menu = sorted(
        menu,
        key=lambda x:x[sort_by],
        reverse=(order=="desc")
    )

    return{
        "sort_by":sort_by,
        "order":order,
        "items":sorted_menu
    }


@app.get("/menu/page")
def menu_page(
page:int = Query(1,ge=1),
limit:int = Query(3,ge=1,le=10)
):

    start=(page-1)*limit

    paged=menu[start:start+limit]

    return{
        "page":page,
        "limit":limit,
        "total":len(menu),
        "total_pages":-(-len(menu)//limit),
        "items":paged
    }


@app.get("/menu/browse")
def browse_menu(
keyword:str = Query(None),
sort_by:str = Query("price"),
order:str = Query("asc"),
page:int = Query(1),
limit:int = Query(4)
):

    result=menu

    if keyword:
        result=[
            i for i in result
            if keyword.lower() in i["name"].lower()
            or keyword.lower() in i["category"].lower()
        ]

    if sort_by in ["price","name","category"]:
        result=sorted(
            result,
            key=lambda x:x[sort_by],
            reverse=(order=="desc")
        )

    total=len(result)

    start=(page-1)*limit

    paged=result[start:start+limit]

    return{
        "keyword":keyword,
        "sort_by":sort_by,
        "order":order,
        "page":page,
        "limit":limit,
        "total_found":total,
        "total_pages":-(-total//limit),
        "items":paged
    }


# ================= CRUD =================

@app.post("/menu")
def add_menu_item(new_item:NewMenuItem,response:Response):

    next_id=max(item["id"] for item in menu)+1

    item={
        "id":next_id,
        "name":new_item.name,
        "price":new_item.price,
        "category":new_item.category,
        "is_available":new_item.is_available
    }

    menu.append(item)

    response.status_code=status.HTTP_201_CREATED

    return{
        "message":"Menu item added",
        "item":item
    }


@app.delete("/menu/{item_id}")
def delete_item(item_id:int):

    item=find_menu_item(item_id)

    if not item:
        return{"error":"Item not found"}

    menu.remove(item)

    return{
        "message":"Item deleted",
        "item":item["name"]
    }


@app.get("/menu/{item_id}")
def get_item(item_id:int):

    item=find_menu_item(item_id)

    if not item:
        return{"error":"Item not found"}

    return item


# ================= ORDERS =================

@app.post("/orders")
def place_order(order:OrderRequest):

    global order_counter

    item=find_menu_item(order.item_id)

    if not item:
        return{"error":"Menu item not found"}

    if not item["is_available"]:
        return{"error":f"{item['name']} is not available"}

    total=calculate_bill(
        item["price"],
        order.quantity,
        order.order_type
    )

    new_order={
        "order_id":order_counter,
        "customer_name":order.customer_name,
        "item":item["name"],
        "quantity":order.quantity,
        "delivery_address":order.delivery_address,
        "order_type":order.order_type,
        "total_price":total,
        "status":"confirmed"
    }

    orders.append(new_order)

    order_counter+=1

    return{
        "message":"Order placed successfully",
        "order":new_order
    }


@app.get("/orders")
def get_orders():

    return{
        "orders":orders,
        "total_orders":len(orders)
    }


@app.get("/orders/search")
def search_orders(customer_name:str = Query(...)):

    results=[
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return{
            "message":f"No orders found for {customer_name}",
            "total_found":0
        }

    return{
        "customer_name":customer_name,
        "total_found":len(results),
        "orders":results
    }


@app.get("/orders/sort")
def sort_orders(order:str = Query("asc")):

    sorted_orders=sorted(
        orders,
        key=lambda x:x["total_price"],
        reverse=(order=="desc")
    )

    return{
        "order":order,
        "orders":sorted_orders
    }


# ================= CART =================

@app.post("/cart/add")
def add_to_cart(item_id:int=Query(...),quantity:int=Query(1)):

    item=find_menu_item(item_id)

    if not item:
        return{"error":"Item not found"}

    if not item["is_available"]:
        return{"error":"Item not available"}

    for c in cart:

        if c["item_id"]==item_id:

            c["quantity"]+=quantity

            c["subtotal"]=calculate_bill(
                item["price"],
                c["quantity"],
                "pickup"
            )

            return{
                "message":"Cart updated",
                "cart_item":c
            }

    cart_item={
        "item_id":item_id,
        "name":item["name"],
        "quantity":quantity,
        "price":item["price"],
        "subtotal":calculate_bill(
            item["price"],
            quantity,
            "pickup"
        )
    }

    cart.append(cart_item)

    return{
        "message":"Added to cart",
        "cart_item":cart_item
    }


@app.get("/cart")
def view_cart():

    if not cart:
        return{"message":"Cart empty"}

    total=sum(c["subtotal"] for c in cart)

    return{
        "items":cart,
        "total_items":len(cart),
        "grand_total":total
    }


@app.delete("/cart/{item_id}")
def remove_cart_item(item_id:int):

    for item in cart:

        if item["item_id"]==item_id:

            cart.remove(item)

            return{
                "message":"Item removed",
                "item":item["name"]
            }

    return{"error":"Item not in cart"}


@app.post("/cart/checkout")
def checkout(data:CheckoutRequest,response:Response):

    global order_counter

    if not cart:

        response.status_code=status.HTTP_400_BAD_REQUEST

        return{"error":"Cart is empty"}

    placed_orders=[]
    grand_total=0

    for item in cart:

        order={
            "order_id":order_counter,
            "customer_name":data.customer_name,
            "item":item["name"],
            "quantity":item["quantity"],
            "delivery_address":data.delivery_address,
            "total_price":item["subtotal"],
            "status":"confirmed"
        }

        orders.append(order)

        placed_orders.append(order)

        grand_total+=item["subtotal"]

        order_counter+=1

    cart.clear()

    response.status_code=status.HTTP_201_CREATED

    return{
        "message":"Checkout successful",
        "orders_placed":placed_orders,
        "grand_total":grand_total
    }