from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        #Get the current session key if it exists
        cart = self.session.get('session_key')
        #Get request
        self.request = request

        # if the user is new, no session key create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        #keep track of all pages by cart being available 
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] ={'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #Deal with the logged in user
        if self.request.user.is_authenticated:
            #Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert the cart to a string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to the profile model
            current_user.update(old_cart=str(carty))
        

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] ={'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #Deal with the logged in user
        if self.request.user.is_authenticated:
            #Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert the cart to a string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to the profile model
            current_user.update(old_cart=str(carty))
        
    def cart_total(self):
        #Get the cart
        ourcart = self.cart
        #Get the product ids
        product_ids = ourcart.keys()
        #Use ids to look up products in database model
        products = Product.objects.filter(id__in=product_ids)
        #Get the total price of all products in the cart
        total = 0
        for key in ourcart:
            for product in products:
                if key == str(product.id):
                    if product.is_sale:
                        #If the product is on sale, use the sale price
                        total += int(ourcart[key]) * float(product.sale_price)
                    else: 
                        total += int(ourcart[key]) * float(product.price)

        #return the total
        return total
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Get Ids from cart
        product_ids = self.cart.keys()
        #Use ids to look up products in database model
        products = Product.objects.filter(id__in=product_ids)
        #returns the looked up products
        return products
    
    def get_quants(self):
        quantites = self.cart
        return quantites
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #Get cart
        ourcart = self.cart
        #Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        
        #Deal with the logged in user
        if self.request.user.is_authenticated:
            #Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert the cart to a string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to the profile model
            current_user.update(old_cart=str(carty))
        
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        #Get cart
        ourcart = self.cart
        #Delete from Dictionary/cart
        if product_id in ourcart:
            del ourcart[product_id]

        self.session.modified = True
        
        #Deal with the logged in user
        if self.request.user.is_authenticated:
            #Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert the cart to a string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to the profile model
            current_user.update(old_cart=str(carty))
        