# Declaration
# Product ID in inventory only start with tp (for deigital product) and sr (for service and repair) then comes with 3 digit such as tp001 or sr017
super_user_email = 'superuser@gmail.com'                            # Super User Email
super_user_password = '123'                                         # Super User Password
user_file = 'user.txt'                                              # Txt file that store user's information
inventory_file = 'inventory.txt'                                    # Txt file that store KLCCC's inventory
customer_cart_file = 'customer_cart.txt'                            # Txt file that store customer's cart information
customer_order_file = 'customer_order.json'                         # Json file that store customer's order
log_file = 'log.txt'                                                # Txt file that store user's log
inventory_staff_purchase_file = 'inventory_staff_purchase.json'     # Json file that store inventory staff's order for requesting restock or add new stock from supplier
inventory_staff_cart_file = 'inventory_staff_cart.txt'              # Txt file that store inventory staff's cart information
inventory_staff_order_file = 'inventory_staff_order.json'           # Json file that store inventory staff's order

from datetime import datetime as dt
import json


########################################################    MAIN MENU      ##############################################################


# Main menu
def main_menu(email):
    klccc = """
            Welcome to

                ██╗  ██╗██╗     ███████╗ ███████╗ ███████╗
                ██║ ██╔╝██║     ██╔════╝ ██╔════╝ ██╔════╝
                █████╔╝ ██║     ██║      ██║      ██║
                ██╔═██╗ ██║     ██║      ██║      ██║ 
                ██║  ██╗███████╗███████╗ ███████╗ ███████╗
                ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══════╝ ╚══════╝ 
                                                        System
    """
    print(f'\n{klccc}')
    print('\n=================================================   MAIN MENU   ====================================================')
    print('\n[1. Register]')
    print('[2. Login]')
    print('[X. Exit]')

    while True:
        main_menu_choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if main_menu_choice == '1':
            log_message('INFO', 'main_menu', email, 'User selected register')
            register(email)
            break
        
        elif main_menu_choice == '2':
            log_message('INFO', 'main_menu', email, 'User selected login')
            login(email)
            break

        elif main_menu_choice == 'x':
            log_message('INFO', 'main_menu', email, 'User exiting the application')
            print('\nSee you next time ^_^')
            print('\n====================================================================================================================')
            exit()

        else:
            log_message('ERROR', 'main_menu', email, 'Invalid input received')
            invalid_input()


##########################################################  REGISTER   ###############################################################


# Register
def register(email):
    new_users = []

    print('\n=================================================   REGISTER   =====================================================')
    available_status = ['customers', 'admin', 'inventory staff']
    print('\nEnter \'x\' to exit')
    while True:
        register_status = input('\nWhat role would you like to register as? (customers / admin / inventory staff): ').lower()

        if register_status == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'register', None, 'User exiting registration to main menu')
            main_menu(None) # email = None because as long as user not successful register, the email is not exist in this system
            return
        
        if register_status in available_status:
            log_message('INFO', 'register', email, f'User selected to register as {register_status}')
            break

        else:
            log_message('ERROR', 'register', email, 'Invalid input received')
            invalid_input()

    while True:
        email = (input('\nPlease enter your email (e.g. xxx@gmail.com): ')).lower()

        if email == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'register', None, 'User exiting registration to main menu')
            main_menu(None) # email = None because as long as user not successful register, the email is not exist in this system
            return
        
        elif email == super_user_email:
            print(f'\n----- [System Message]: You are not allowed to register as \'{email}\'')
            print('\n====================================================================================================================')
            log_message('WARNING', 'register', None, 'Attempted to register as super user')
            main_menu(None)
            return
        
        else:        
            if check_email_validity(email):
                # Checking existence of email
                if find_user_email(email):
                    print(f'\n----- [System Message]: A user with email \'{email}\' is already registered')
                    print('\n====================================================================================================================')
                    log_message('INFO', 'register', None, 'User already registered with email')

                    while True:
                        selection = input('\nWould you like to proceed to login page? (y/n): ').lower()

                        if selection == 'y':
                            log_message('INFO', 'register', None, 'User choosing to proceed to login')
                            login(None)
                            return
                            
                        elif selection == 'n':
                            log_message('INFO', 'register', None, 'User choosing to re-register')
                            register(None)
                            return
                            
                        else:
                            log_message('ERROR', 'register', email, 'Invalid input received')
                            invalid_input()
                else:
                    break
            else:
                continue
                
    
    while True:
        password = input('\nPlease enter your password\nMinimum 8 characters long, contain special character, number and upper lower case): ')

        if password.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'register', None, 'User exiting during password entry to main menu')
            main_menu(None)
            return

        elif not check_password_strength(password): # If the check_password_strength function return FALSE, it will loops again
            log_message('WARNING', 'register', None, 'Password does not meet strength requirements')
            continue

        else:
            break
    
    # Double checking of password
    while True:
        dc_password = input('\nPlease double confirm your password: ')

        if dc_password.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'register', None, 'User exiting during password confirmation to main menu')
            main_menu(None)
            return
        
        elif password != dc_password:
            print('\n----- [System Message]: Please check again your password. It is CASE SENSITIVE')
            print('\n====================================================================================================================')
            log_message('WARNING', 'register', None, 'Double confirm password doesn\'t match with initial password')
        
        else:
            password = hashing(password)
            break

    while True:
        name = input('\nPlease enter your name: ')

        if name == '' or name.isspace() or any(is_symbol(char) for char in name):
            log_message('ERROR', 'register', None, 'Invalid input received')
            invalid_input()

        else:
            break

    # IC format checking
    while True:
        ic = input('\nPlease enter your 12 digit IC number (without hyphens \'-\'): ')
        if len(ic) == 12 and ic.isdigit():
            break

        else:
            print('\n----- [System Message]: Please enter a valid IC number')
            print('\n===================================================================================================================')
            log_message('WARNING', 'register', None, 'Invalid IC number entered')

    # Phone format checking
    while True:
        phone = input('\nPlease enter your phone number (e.g. 601xxxxxxxx): ')
        if phone.isdigit() and (phone[:3] == '601') and (len(phone) >= 10):
            break
        else:
            print('\n----- [System Message]: Please enter a valid phone number')
            print('\n====================================================================================================================')
            log_message('WARNING', 'register', None, 'Invalid phone number entered')

    # Asking address line 1
    while True:
        address_1 = input('\nPlease enter your address line 1: ').upper()
        if address_1 == '' or address_1.isspace():
                log_message('ERROR', 'register', None, 'Invalid address 1 entered')
                invalid_input()
        else:
            break

    address_2 = input('\nPlease enter your address line 2 (leave it blank if not needed): ').upper()

    if address_2 == '' or address_2.isspace():
        address_2 = '-'
    
    # Postal code format checking
    while True:
        postal_code = input('\nPlease enter your postal code: ')
        if len(postal_code) == 5 and postal_code.isdigit():
            break

        else:
            print('\n----- [System Message]: Please enter a valid postal code')
            print('\n====================================================================================================================')
            log_message('WARNING', 'register', None, 'Invalid postal code entered')
    
    # Asking for city
    while True:
        city = input('\nPlease enter your city: ').upper()
        if city == '' or city.isspace() or any(char.isdigit() for char in city):
            log_message('ERROR', 'register', None, 'Invalid input received')
            invalid_input()
        else:
            break

    # Asking for state
    while True:
        print('\n1. KUALA LUMPUR, 2. LABUAN, 3. PUTRAJAYA, 4. JOHOR, 5. KEDAH\n6. KELANTAN, 7. MELAKA, 8. NEGERI SEMBILAN, 9. PAHANG, 10. PULAU PINANG\n11. PERAK, 12. PERLIS, 13. SABAH, 14. SARAWAK, 15. SELANGOR, 16. TERENGGANU')
        state = input('Please select your state (e.g. 1): ')
        if state == '1':
            state = 'KUALA LUMPUR'
            break
        elif state == '2':
            state = 'LABUAN'
            break
        elif state == '3':
            state = 'PUTRAJAYA'
            break
        elif state == '4':
            state = 'JOHOR'
            break
        elif state == '5':
            state = 'KEDAH'
            break
        elif state == '6':
            state = 'KELANTAN'
            break
        elif state == '7':
            state = 'MELAKA'
            break
        elif state == '8':
            state = 'NEGERI SEMBILAN'
            break
        elif state == '9':
            state = 'PAHANG'
            break
        elif state == '10':
            state = 'PULAU PINANG'
            break
        elif state == '11':
            state = 'PERAK'
            break
        elif state == '12':
            state = 'PERLIS'
            break
        elif state == '13':
            state = 'SABAH'
            break
        elif state == '14':
            state = 'SARAWAK'
            break
        elif state == '15':
            state = 'SELANGOR'
            break
        elif state == '16':
            state = 'TERENGGANU'
            break
        else:
            log_message('ERROR', 'register', None, 'Invalid input received')
            invalid_input()

    date = dt.now().strftime('%d %b %y %H:%M:%S')
    # Default status = awaiting admin approval
    status = f'{register_status} (awaiting approval)'

    # Save user details
    new_users.append([email, password, name, ic, phone, address_1, address_2, postal_code, city, state, date, status])
    save_user_details(new_users)

    print(f'\n----- [System Message]: {email} registered successfully')
    print('\n====================================================================================================================')
    
    log_message('INFO', 'register', email, 'User registered successfully')
    main_menu(None)
    return


########################################################    LOGIN   ##############################################################


# Login
def login(email):
    current_user_role = None
    print('\n==================================================   LOGIN   =======================================================')
    print('\nEnter \'x\' to exit')
    email = (input('\nPlease enter your email (e.g. xxx@gmail.com): ')).lower()

    # Loading user data
    user_details = find_user_email(email)

    if email == 'x':
        print('\n====================================================================================================================')
        log_message('INFO', 'login', None, 'User exiting during password entry to main menu')
        main_menu(None)
        return

    # Checking existence of email
    elif email == super_user_email:
        current_user_role = 'super user'
    
    elif user_details is None:
        print(f'\n----- [System Message]: The email \'{email}\' is not yet registered')
        print('\n====================================================================================================================')
        log_message('WARNING', 'login', None, 'Email not registered') # email = None because the email is not exist in this system

        while True:
            selection = input('\nWould you like to proceed to register page? (y/n): ').lower()

            if selection == 'y':
                log_message('INFO', 'register', None, 'User choosing to proceed to register')
                register(None)
                return
                
            elif selection == 'n':
                log_message('INFO', 'login', None, 'User choosing to re-login')
                login(None)
                return
                
            else:
                log_message('ERROR', 'login', None, 'Invalid input received')
                invalid_input()

    # Checking user password
    attempt = 0
    max_attempts = 3

    while attempt < max_attempts:
        provided_password = input('\nPlease enter your password: ')

        # Hashing the password  
        hashed_password = hashing(provided_password)

        if provided_password.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'login', email, 'Exiting to main menu during password entry')
            main_menu(None)
            return

        elif current_user_role == 'super user' and provided_password == super_user_password:
            print('\n----- [System Message]: Access granted!')
            log_message('INFO', 'login', email, 'Super user logged in successfully')
            super_user_menu(super_user_email)
            return

        elif (current_user_role is None and user_details[1] != hashed_password) or (current_user_role == 'super user' and provided_password != super_user_password):
            attempt += 1
            print('\n----- [System Message]: Incorrect password. It is CASE SENSITIVE')
            print(f'----- [System Message]: You have {max_attempts - attempt} more attempt(s)')
            log_message('WARNING', 'login', email, f'Incorrect password attempt {attempt}')

            if attempt == max_attempts:
                print('----- [System Message]: Maximum attempts reached. Access denied')
                print('\n====================================================================================================================')
                log_message('WARNING', 'login', email, 'Maximum login attempts reached. Access denied')
                main_menu(None)
                return
            
            print('\n====================================================================================================================')

        else:
            print('\n----- [System Message]: Access granted!')
            log_message('INFO', 'login', email, f'User: {email}  logged in successfully')
            break

    # Checking user status        
    if '(awaiting approval)' in user_details[11]:
        print('----- [System Message]: Your account is still waiting for admin / super user approval')
        print('\n====================================================================================================================')
        log_message('INFO', 'login', email, 'User awaiting admin / super user approval')
        main_menu(None)

    elif '(disabled)' in user_details[11]:
        print('----- [System Message]: Your account has been disabled by super user')
        print('\n====================================================================================================================')
        log_message('WARNING', 'login', email, 'User trying to login with disabled account')
        main_menu(None)
        
    elif user_details[11] == 'customers':
        log_message('INFO', 'login', email, 'Customer logged in')
        print('\n====================================================================================================================')
        customer_menu(email)
        return        

    elif user_details[11] == 'inventory staff':
        log_message('INFO', 'login', email, 'Inventory staff logged in')
        print('\n====================================================================================================================')
        inventory_management(email)
        return
    
    elif user_details[11] == 'admin':
        log_message('INFO', 'login', email, 'Admin logged in')
        print('\n====================================================================================================================')
        user_management(email)
        return


#############################################################   SUPER USER MENU  #################################################################


# Super User Menu
def super_user_menu(email):
    check_super_user_details(email) # Default adding the user details of super user if haven't exist in user.txt
    print('\n=============================================   SUPER USER MENU   ==================================================')
    print('\n[1. Customer Management (CUSTOMER MENU)]')
    print('[2. User Management (USER MENU)]')
    print('[3. Inventory Management (INVENTORY MENU)]')
    print('[X. Exit]')

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()

        if choice == '1':
            log_message('INFO', 'super_user_menu', email, 'User selected customer menu')
            print('\n====================================================================================================================')
            customer_menu(email)
            return
        
        elif choice == '2':
            log_message('INFO', 'super_user_menu', email, 'User selected user management')
            print('\n====================================================================================================================')
            user_management(email)
            return

        elif choice == '3':
            log_message('INFO', 'super_user_menu', email, 'User selected inventory management')
            print('\n====================================================================================================================')
            inventory_management(email)
            return

        elif choice == 'x':
            log_message('INFO', 'super_user_menu', email, 'User exiting super user menu to main menu')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            main_menu(None)
            return

        else:
            log_message('ERROR', 'super_user_menu', email, 'Invalid input received')
            invalid_input()


###########################################################   CUSTOMER MENU  #################################################################


# Customer Menu
def customer_menu(email):
    print('\n==============================================   CUSTOMER MENU   ===================================================')
    print('\n[1. Purchase Order]')
    print('[2. Service / Repair Order]')
    print('[3. Modify Purchase / Service / Repair Order (CUSTOMER CART)]')
    print('[4. Payment for Orders Placed]')
    print('[5. Inquiry of Order Status]')
    print('[6. Cancel Orders]')
    print('[7. Reports]')
    print('[8. Settings]')
    print('[X. Exit]')

    while True:
        customer_menu_choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if customer_menu_choice == '1':
            log_message('INFO', 'customer_menu', email, 'User selected purchase order')
            purchase_order(email)
            return
        
        elif customer_menu_choice == '2':
            log_message('INFO', 'customer_menu', email, 'User selected service / repair order')
            service_repair_order(email)
            return

        elif customer_menu_choice == '3':
            log_message('INFO', 'customer_menu', email, 'User selected modify purchase / service / repair order')
            modify_purchase_service_repair_order(email)
            return

        elif customer_menu_choice == '4':
            log_message('INFO', 'customer_menu', email, 'User selected payment for orders placed')
            payment_for_orders_placed(email)
            return

        elif customer_menu_choice == '5':
            log_message('INFO', 'customer_menu', email, 'User selected inquiry of order status')
            inquiry_of_order_status(email)
            return

        elif customer_menu_choice == '6':
            log_message('INFO', 'customer_menu', email, 'User selected cancel orders')
            customer_cancel_orders(email)
            return

        elif customer_menu_choice == '7':
            log_message('INFO', 'customer_menu', email, 'User selected reports for customer management')
            reports_for_customer_management(email)
            return
        
        elif customer_menu_choice == '8':
            log_message('INFO', 'customer_menu', email, 'User selected Settings')
            settings(email, 'customers')
            return

        elif customer_menu_choice == 'x':
            if email == super_user_email:
                log_message('INFO', 'customer_menu', email, 'User exiting customer menu to super user menu')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                super_user_menu(email)
                return
            
            else:
                log_message('INFO', 'customer_menu', email, 'User exiting customer menu to main menu')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                main_menu(None)
                return

        else:
            log_message('ERROR', 'customer_menu', email, 'Invalid input received')
            invalid_input()


## Customer Purchase Order
def purchase_order(email):
    print('\n=============================================   PURCHASE ORDER   ===================================================')
    print('\n[1. List Out All Items]')
    print('[2. Search for an Product by Product ID]')
    print('[3. Search for an Product by Product Name]')
    print('[4. Search for an Product by Category]')
    print('[X. Exit]')

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if choice == '1':
            log_message('INFO', 'purchase_order', email, 'User selected to list out all items')
            display_product_details('listing all', 'product', 'customers', email)
            return

        elif choice == '2':
            log_message('INFO', 'purchase_order', email, 'User selected to search for a product by product id')
            search_by_id(email)
            return
        
        elif choice == '3':
            log_message('INFO', 'purchase_order', email, 'User selected to search for a product by product name')
            search_by_name(email)
            return
        
        elif choice == '4':
            log_message('INFO', 'purchase_order', email, 'User selected to search for a product by category')
            search_by_category(email)
            return
        
        elif choice == 'x':
            log_message('INFO', 'purchase_order', email, 'User exiting purchase order to customer menu')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            customer_menu(email)
            return
        
        else:
            log_message('ERROR', 'purchase_order', email, 'Invalid input received')
            invalid_input()


### Search for an Product by Product ID
def search_by_id(email):
    print('\n===============================================   SEARCH BY ID   ===================================================')

    while True:
        print('\nEnter \'x\' to exit')
        productId = input('\nPlease enter the product ID that you would wish to search for: ').lower()

        if productId == 'x':
            log_message('INFO', 'search_by_id', email, 'User exiting search by id to purchase order')
            purchase_order(email)
            return
        
        if not productId:
            log_message('ERROR', 'search_by_id', email, 'Invalid input received')
            invalid_input()
        
        else:
            log_message('INFO', 'search_by_id', email, f'Searching for product ID: {productId}')
            display_product_details('product id', productId, 'customers', email)
            return


### Search for an Product by Product Name
def search_by_name(email):
    print('\n==============================================   SEARCH BY NAME   ==================================================')

    while True:
        print('\nEnter \'x\' to exit')
        productName = input('\nPlease enter the name of the product that you would wish to search for: ').lower()

        if productName == 'x':
            log_message('INFO', 'search_by_name', email, 'User exiting search by name to purchase order')
            purchase_order(email)
            return
        
        if not productName:
            log_message('ERROR', 'search_by_name', email, 'Invalid input received')
            invalid_input()
        
        else:
            log_message('INFO', 'search_by_name', email, f'Searching for product name: {productName}')
            display_product_details('product name', productName, 'customers', email)
            return


### Search for an Product by Category
def search_by_category(email):
    print('\n============================================   SEARCH BY CATEGORY   ================================================')

    while True:
        print('\nEnter \'x\' to exit')
        productCategory = input('\nPlease enter the category of the product that you would wish to search for: ').lower()

        if productCategory == 'x':
            log_message('INFO', 'search_by_category', email, 'User exiting search by category to purchase order')
            purchase_order(email)
            return
        
        if not productCategory:
            log_message('ERROR', 'search_by_category', email, 'Invalid input received')
            invalid_input()
        
        else:
            log_message('INFO', 'search_by_category', email, f'Searching for product category: {productCategory}')
            display_product_details('category', productCategory, 'customers', email)
            return


#### Add to Cart
def add_to_cart(email, role):
    print('\n===============================================   ADD TO CART   ====================================================')
    current_cart = find_cart(email, 'simple')
    print('\nShopping Cart:')

    try:
        print('\n'+current_cart)
        print('----------------------------------------------------------------')
        log_message('INFO', 'add_to_cart', email, 'Displayed current cart')        

    except TypeError:
        print('\nThere is nothing in your shopping cart')
        print('\n----------------------------------------------------------------')
        log_message('INFO', 'add_to_cart', email, 'Cart is empty')

    # Ask for Product ID
    while True:
        print('\nEnter \'x\' to exit')
        product_id = input('\nPlease enter the product ID that you would like to add into your shopping cart: ').lower()

        if product_id == 'x':
            if role == 'customers':
                log_message('INFO', 'add_to_cart', email, 'User exiting add to cart to purchase order')
                purchase_order(email)
                return
            
            elif role == 'customers from service':
                log_message('INFO', 'add_to_cart', email, 'User exiting add to cart to service / repair order')
                service_repair_order(email)
                return
                    
        if not product_id:
            log_message('ERROR', 'add_to_cart', email, 'Invalid input received')
            invalid_input()

        else:
            # Check if the product being added already exists in the cart
            product_exist_in_cart = find_cart(email, 'detail')
            if product_exist_in_cart is None:
                pass

            else:
                product_id_lines = product_exist_in_cart.split('\n')
                for line in product_id_lines:
                    if line.startswith('Product ID: '):
                        actual_product_id = line.split(': ')[1].strip()

                        if product_id == actual_product_id:
                            print(f'\n----- [System Message]: Product ID: {product_id} already exists in your cart')
                            print('\n====================================================================================================================')
                            log_message('WARNING', 'add_to_cart', email, f'Product ID: {product_id} already exists in cart')

                            while True:
                                choice = input('\nWould you like to update / remove the products? (y/n): ').lower()

                                if choice == 'y':
                                    log_message('INFO', 'add_to_cart', email, 'User opted to update / remove products in cart')
                                    modify_purchase_service_repair_order(email)
                                    return
                                
                                elif choice == 'n':
                                    log_message('INFO', 'add_to_cart', email, 'User opted to continue adding products')
                                    print('\n====================================================================================================================')
                                    add_to_cart(email, role)
                                    return
                                
                                else:
                                    log_message('ERROR', 'add_to_cart', email, 'Invalid input received')
                                    invalid_input()                        
                        else:
                            pass

            product_details = find_inventory('product id', product_id, None)
                
            if product_details:
                log_message('INFO', 'add_to_cart', email, f'Product ID: {product_id} found in inventory')
                break

            else:
                print(f'\n----- [System Message]: Product ID: {product_id} does not exist')
                print('\n====================================================================================================================')
                log_message('WARNING', 'add_to_cart', email, f'Product ID: {product_id} does not exist')

    # Ask for Purchase Quantity
    while True:
        purchase_quantity = input('\nHow many do you need: ')

        if purchase_quantity.lower() == 'x':
            if role == 'customers':
                log_message('INFO', 'add_to_cart', email, 'User exiting add to cart to purcahse order')
                purchase_order(email)
                return
            
            elif role == 'customers from service':
                log_message('INFO', 'add_to_cart', email, 'User exiting add to cart to service / repair order')
                service_repair_order(email)
                return
        
        try:
            purchase_quantity = int(purchase_quantity)

            if purchase_quantity <= 0:
                print('\n----- [System Message]: Please enter a quantity greater than zero')
                print('\n====================================================================================================================')
                log_message('WARNING', 'add_to_cart', email, 'Entered quantity is not greater than zero')
                continue

            # Check if the entered quantity >/< the available quantity of the product
            for product_detail in product_details:
                name = product_detail[1]
                price = product_detail[4]
                stock_available = int(product_detail[5])

                if purchase_quantity <= stock_available:
                    save_cart(purchase_quantity, name, product_id, price, email)
                    print(f'\n----- [System Message]: You have added {purchase_quantity}x {name} with price RM {price} each into your shopping cart')
                    print('\n====================================================================================================================')
                    log_message('INFO', 'add_to_cart', email, f'Added {purchase_quantity}x {name} to cart')
                    break

                else:
                    print(f'\n----- [System Message]: We have only {stock_available} unit(s) available in stock. Please enter a smaller quantity')
                    print('\n====================================================================================================================')
                    log_message('WARNING', 'add_to_cart', email, f'Insufficient stock for {name}. Requested {purchase_quantity}, available {stock_available}')
            else:
                continue

            break

        except ValueError:
            print('\n----- [System Message]: Please enter a valid number')
            print('\n====================================================================================================================')
            log_message('WARNING', 'add_to_cart', email, 'Entered value is not a valid number')
            continue

    # Continue Adding Product into Cart or Checkout
    while True:
        continue_purchase = input('\nWould you like to continue adding new product into your shopping cart? (y/n): ').lower()
        print('\n====================================================================================================================')

        if continue_purchase == 'y':
            log_message('INFO', 'add_to_cart', email, 'User opted to continue adding products')
            add_to_cart(email, role)
            return
        
        elif continue_purchase == 'n':
            log_message('INFO', 'add_to_cart', email, 'User opted to finish and modify cart')
            modify_purchase_service_repair_order(email)
            return
        
        else:
            log_message('ERROR', 'add_to_cart', email, 'Invalid input received')
            invalid_input()


## Service / Repair Order
def service_repair_order(email):
    print('\n=========================================   SERVICE / REPAIR ORDER   ===============================================')
    print('\n[1. Mobile Phone Reformat Service]')
    print('[2. Computer Reformat Service]')
    print('[3. Data Backup & Restore Service]')
    print('[4. Motherboard Repair]')
    print('[5. Mobile Phone Internal Cleaning Service]')
    print('[6. Computer Internal Cleaning Service]')
    print('[7. Mobile Phone / Laptop Battery Repair]')
    print('[8. Desktop Power Supply Repair]')
    print('[X. Exit]')

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()

        if choice == '1':
            log_message('INFO', 'service_repair_order', email, 'User selected mobile phone reformat service')
            print('\n====================================================================================================================')
            display_product_details('product name', 'mobile phone reformat service', 'customers from service', email)
            return

        elif choice == '2':
            log_message('INFO', 'service_repair_order', email, 'User selected computer reformat service')
            print('\n====================================================================================================================')
            display_product_details('product name', 'computer reformat service', 'customers from service', email)
            return
        
        elif choice == '3':
            log_message('INFO', 'service_repair_order', email, 'User selected data bBackup & restore service')
            print('\n====================================================================================================================')
            display_product_details('product name', 'data backup & restore service', 'customers from service', email)
            return
        
        elif choice == '4':
            log_message('INFO', 'service_repair_order', email, 'User selected motherboard repair')
            print('\n====================================================================================================================')
            display_product_details('product name', 'motherboard repair', 'customers from service', email)
            return
        
        elif choice == '5':
            log_message('INFO', 'service_repair_order', email, 'User selected mobile phone internal cleaning service')
            print('\n====================================================================================================================')
            display_product_details('product name', 'mobile phone internal cleaning service', 'customers from service', email)
            return
        
        elif choice == '6':
            log_message('INFO', 'service_repair_order', email, 'User selected computer internal cleaning service')
            print('\n===================================================================================================================')
            display_product_details('product name', 'computer internal cleaning service', 'customers from service', email)
            return
        
        elif choice == '7':
            log_message('INFO', 'service_repair_order', email, 'User selected mobile phone / laptop battery repair')
            print('\n====================================================================================================================')
            display_product_details('product name', 'mobile phone / laptop battery repair', 'customers from service', email)
            return
        
        elif choice == '8':
            log_message('INFO', 'service_repair_order', email, 'User selected desktop power supply repair')
            print('\n====================================================================================================================')
            display_product_details('product name', 'desktop power supply repair', 'customers from service', email)
            return
        
        elif choice == 'x':
            log_message('INFO', 'service_repair_order', email, 'User exiting service / repair order to customer menu')
            print('\n====================================================================================================================')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            customer_menu(email)
            return
        
        else:
            log_message('ERROR', 'service_repair_order', email, 'Invalid input received')
            invalid_input()


## Modify Purchase / Service / Repair Order
def modify_purchase_service_repair_order(email):
    print('\n================================   MODIFY PURCHASE / SERVICE / REPAIR ORDER   ======================================')
    # Get the customer's current cart details
    cart_details = find_cart(email, 'detail')

    # Print the cart details
    print('\nShopping Cart:')    
    try:
        print('\n' + cart_details)
        print('\n[1. Checkout]')
        print('[2. Update Quantity of a Product in Cart]')
        print('[3. Remove all Product in Cart]')
        print('[4. Remove a Product in Cart]')
        print('[X. Exit]')
        log_message('INFO', 'modify_purchase_service_repair_order', email, 'Displayed cart details and options')

    except TypeError: # Nothing in the cart / Empty cart
        print('\nThere is nothing in your shopping cart')
        log_message('WARNING', 'modify_purchase_service_repair_order', email, 'Cart is empty')
        customer_menu(email)
        return

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if choice == '1':
            log_message('INFO', 'modify_purchase_service_repair_order', email, 'Initiating checkout')
            payment_for_orders_placed(email)
            return
        
        elif choice == '2':
            while True:
                print('\nEnter \'x\' to exit')
                product_id = input('\nPlease enter the product ID that you wish to edit: ').lower()
                if product_id and product_id != 'x':
                    # Make sure user input's product ID is valid fully. Exp: only proceed if user enter TP001, won't proceed is user enter TP000
                    product_id_lines = cart_details.split('\n')
                    for line in product_id_lines:
                        if line.startswith('Product ID: '):
                            actual_product_id = line.split(': ')[1].strip()                            
                            if product_id == actual_product_id:
                                log_message('INFO', 'modify_purchase_service_repair_order', email, f'Editing quantity for Product ID: {product_id}')
                                remove_product_from_cart(email, product_id, 'update')
                                print('\n----- [System Message]: Action Successful')
                                print('\n====================================================================================================================')
                                modify_purchase_service_repair_order(email)
                                return
                    
                    else:
                        log_message('WARNING', 'modify_purchase_service_repair_order', email, f'Product ID: {product_id} is not in cart')
                        print(f'\n----- [System Message]: Product ID: {product_id} is not in your cart')
                        print('\n====================================================================================================================')

                if product_id == 'x':
                    log_message('INFO', 'modify_purchase_service_repair_order', email, 'Exiting to modify purchase / service / repair order')
                    modify_purchase_service_repair_order(email)
                    return

                elif not product_id:
                    log_message('ERROR', 'modify_purchase_service_repair_order', email, 'Invalid input received')
                    invalid_input() 

        elif choice == '3':
            while True:
                selection = input('\nAre you sure you want to remove all product(s) in your cart? (y/n): ').lower()
                if selection == 'y':
                    log_message('INFO', 'modify_purchase_service_repair_order', email, 'Removing all products from cart')
                    remove_product_from_cart(email, None, 'all')
                    print('\n----- [System Message]: Action Successful')
                    print('\n====================================================================================================================')
                    modify_purchase_service_repair_order(email)
                    return

                elif selection == 'n':
                    log_message('INFO', 'modify_purchase_service_repair_order', email, 'Cancelled removal of all products from cart')
                    modify_purchase_service_repair_order(email)
                    return
                
                else:
                    log_message('ERROR', 'modify_purchase_service_repair_order', email, 'Invalid input received')
                    invalid_input()
        
        elif choice == '4':
            while True:
                print('\nEnter \'x\' to exit')
                product_id = input('\nPlease enter the product ID that you wish to remove: ').lower()
                    
                if product_id and product_id != 'x':
                    # Make sure user input's product ID is valid fully. Exp: only proceed if user enter TP001, won't proceed is user enter TP00
                    product_id_lines = cart_details.split('\n')
                    for line in product_id_lines:
                        if line.startswith('Product ID: '):
                            actual_product_id = line.split(': ')[1].strip()

                            if product_id == actual_product_id:
                                log_message('INFO', 'modify_purchase_service_repair_order', email, f'Removing Product ID: {product_id} from cart')
                                remove_product_from_cart(email, product_id, 'single')
                                print('\n----- [System Message]: Action Successful')
                                print('\n====================================================================================================================')
                                modify_purchase_service_repair_order(email)
                                return
                            
                    else:
                        log_message('WARNING', 'modify_purchase_service_repair_order', email, f'Product ID: {product_id} is not in cart')
                        print(f'\n----- [System Message]: Product ID: {product_id} is not in your cart ')
                        print('\n====================================================================================================================')

                if product_id == 'x':
                    log_message('INFO', 'modify_purchase_service_repair_order', email, 'Exiting to modify purchase / service / repair order')
                    modify_purchase_service_repair_order(email)
                    return

                elif not product_id:
                    log_message('ERROR', 'modify_purchase_service_repair_order', email, 'Invalid input received')
                    invalid_input()            
        
        elif choice == 'x':
            log_message('INFO', 'modify_purchase_service_repair_order', email, 'Exiting modify purchase / service / repair order')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            customer_menu(email)
            return
        
        else:
            log_message('ERROR', 'modify_purchase_service_repair_order', email, 'Invalid input received')
            invalid_input()
 

## Payment for Orders Placed
def payment_for_orders_placed(email):
    print('\n========================================   PAYMENT FOR ORDERS PLACED   =============================================')
    # Get current user's items and total price in cart
    cart_details = find_cart(email, 'detail')
    if cart_details:
        log_message('INFO', 'payment_for_orders_placed', email, 'Displayed cart details for payment')
        pass

    else:
        print('\nThere is nothing in your shopping cart')
        log_message('WARNING', 'payment_for_orders_placed', email, 'Cart is empty during payment process')
        customer_menu(email)
        return
    
    # Ask for user's payment card details
    while True:
        print('\nEnter \'x\' to exit')
        card_num = input('\nPlease enter your card number without spacing: ')

        if card_num.lower() == 'x':
            log_message('INFO', 'payment_for_orders_placed', email, 'User exiting payement for order placed to customer menu')
            customer_menu(email)
            return 
        
        # Check if card number is in correct format       
        if not is_valid_card_number(card_num):
            log_message('WARNING', 'payment_for_orders_placed', email, 'Invalid card number entered')
            print('\n----- [System Message]: Invalid card number. Please check again')
            print('\n====================================================================================================================')
            continue

        else:
            log_message('INFO', 'payment_for_orders_placed', email, 'Valid card number entered')
            break
    
    while True:
        expiry_date = input('\nPlease enter the expiry date (e.g. MM/YY): ')
        # Check if expiry date is in MM/YY format and valid
        if not is_valid_expiry_date(expiry_date):
            log_message('WARNING', 'payment_for_orders_placed', email, 'Invalid expiry date entered')
            print('\n====================================================================================================================')
            continue

        else:
            log_message('INFO', 'payment_for_orders_placed', email, 'Valid expiry date entered')
            break
    
    while True:
        cvv = input('\nPlease enter the CVV: ')
        # Check if CVV is numeric and either 3 or 4 digits long
        if not is_valid_cvv(cvv):
            log_message('WARNING', 'payment_for_orders_placed', email, 'Invalid CVV entered')
            print('\n----- [System Message]: Invalid CVV. Please check again')
            print('\n====================================================================================================================')
            continue

        else:
            log_message('INFO', 'payment_for_orders_placed', email, 'Valid CVV entered')
            break

    # Retrieve back user's name, phone number and address for shipping purpose
    address = display_user_details(email, 'for payment')
    
    # Display all the information
    print('\n====================================================================================================================')
    print('\nCheckout Product(s):')
    print(f'\n{cart_details}')
    print('\n----------------------------------------------------------------')
    print('\nShipping Details:')
    print(f'\n{address}')
    print('\n----------------------------------------------------------------')
    print('\nPayment Details:')
    print(f'\nCard Number: {card_num}\nExpiry Date: {expiry_date}\nCVV: {cvv}')
    print('\n----------------------------------------------------------------')
    print('\n====================================================================================================================')

    while True:
        choice = input('\nWould you like continue checkout with this details? (y/n): ').lower()

        if choice == 'y':
            date = dt.now().strftime('%d %b %y %H:%M:%S')
            save_order(email, address, date)
            return
        
        elif choice == 'n':
            log_message('INFO', 'payment_for_orders_placed', email, 'User cancelled the checkout process')
            customer_menu(email)
            return
        
        else:
            log_message('ERROR', 'payment_for_orders_placed', email, 'Invalid input received')
            invalid_input()
  

## Inquiry of Order Status
def inquiry_of_order_status(email):
    print('\n=========================================   INQUIRY OF ORDER STATUS   ==============================================')
    print('\n[1. List all Order History]')
    print('[2. Search Order Status by Order ID]')
    print('[3. Cancel Order]')
    print('[X. Exit]')

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if choice == '1':
            log_message('INFO', 'inquiry_of_order_status', email, 'User selected to list all order history')
            find_order(email, None, email, 'customer management')
            return
        
        elif choice == '2':
            log_message('INFO', 'inquiry_of_order_status', email, 'User selected to search order status by order id')
            while True:
                print('\nEnter \'x\' to exit')
                order_id = input('\nPlease enter the order ID: ').lower()
                print('\n====================================================================================================================')
                if order_id == 'x':
                    log_message('INFO', 'inquiry_of_order_status', email, 'User cancelled the action')
                    inquiry_of_order_status(email)
                    return
                
                else:
                    log_message('INFO', 'inquiry_of_order_status', email, f'User searched for order ID: {order_id}')
                    find_order(email, order_id, email, 'customer management')
                    return
                
        elif choice == '3':
            log_message('INFO', 'inquiry_of_order_status', email, 'User directing to cancel orders')
            customer_cancel_orders(email)
            return

        elif choice == 'x':
            log_message('INFO', 'inquiry_of_order_status', email, 'User exiting inquiry of order status to customer menu')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            customer_menu(email)
            return

        else:
            log_message('ERROR', 'inquiry_of_order_status', email, 'Invalid input received')
            invalid_input()


## Cancel Orders
def customer_cancel_orders(email):
    print('\n==============================================   CANCEL ORDERS   ===================================================')

    while True:
        print('\nEnter \'x\' to exit')
        orderID = input('\nPlease enter the order ID that you would wish to cancel for: ').lower()

        if orderID == 'x':
            log_message('INFO', 'cancel_orders', email, 'User exiting cancel orders to customer menu')
            customer_menu(email)
            return
        
        elif not orderID or orderID.isspace() or not orderID.isdigit():
            log_message('INFO', 'cancel_orders', email, 'Invalid input received')
            invalid_input()
        
        else:
            while True:
                choice = input("\nBy cancelling order after payment, you WON'T GET ANY REFUND. Are you sure? (y/n): ").lower()

                if choice == 'y':
                    log_message('INFO', 'cancel_orders', email, f'Cancelling order: {orderID}')

                    if not update_order(email, orderID, 'cancelled', 'customer management'):
                        log_message('INFO', 'cancel_orders', email, f'Order id: {orderID} cancel unsuccessful')
                        print(f'\n----- [System Message]: No order with order ID: {orderID} found for {email}')
                        print('\n====================================================================================================================')
                        customer_cancel_orders(email)

                    else:
                        log_message('INFO', 'cancel_orders', email, f'Order id: {orderID} cancel successful')
                        print(f"\n----- [System Message]: Order with order ID: {orderID} cancelled successful")
                        print('\n====================================================================================================================')
                        customer_menu(email)
                        return

                elif choice == 'n':
                    log_message('INFO', 'cancel_orders', email, 'User exiting cancel orders to customer menu')
                    customer_menu(email)
                    return
                
                else:
                    log_message('INFO', 'cancel_orders', email, 'Invalid input received')
                    invalid_input()


## Reports for Customer Management
def reports_for_customer_management(email):
    print('\n=================================================   REPORTS   ======================================================')
    print('\nEnter \'x\' to exit')
    level = input("\nPlease enter log level (INFO, WARNING, ERROR) or leave blank for all: ").strip() or None
    
    if level:
        if level.lower() == 'x':
            log_message('INFO', 'reports_for_customer_management', email, 'User exiting reports for customer management to customer menu')
            customer_menu(email)
            return
    
    page = input("\nPlease enter page name (e.g. customer menu) or leave blank for all: ").strip() or None
    start_time_str = input("\nPlease enter start date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:04:07) or leave blank for no start time: ").strip()
    end_time_str = input("\nPlease enter end date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:05:07) or leave blank for no end time: ").strip()
    keyword = input("\nPlease enter keyword to search in messages or leave blank for no keyword: ").strip() or None
    print('\n====================================================================================================================')

    try:
        start_time = dt.strptime(start_time_str, "%d %b %y %H:%M:%S") if start_time_str else None
        end_time = dt.strptime(end_time_str, "%d %b %y %H:%M:%S") if end_time_str else None

    except ValueError or UnboundLocalError:
        log_message('ERROR', 'reports_for_customer_management', email, 'Invalid date format entered')
        print('\n----- [System Message]: Invalid date format entered')
        reports_for_customer_management(email)
        return

    except Exception as e:
        print(e)
        print('\n----- [System Message]: Please check again your date format entered')
        reports_for_customer_management(email)
        return

    # Parse the log data
    parsed_logs = find_log_message(email)

    # Apply filters
    filtered_logs = filtering_log(parsed_logs, level, page, start_time, end_time, keyword)

    if not filtered_logs:
        log_message('ERROR', 'reports_for_customer_management', email, 'No matched result')
        print('\n----- [System Message]: No matched result. Please double check the data you entered')
        reports_for_customer_management(email)
        return

    else:
        # Generate report
        log_message('INFO', 'reports_for_customer_management', email, 'Report generated successful')
        report = generate_user_report(filtered_logs, email)

    # Print the report
    print(report)
    customer_menu(email)
    return


####################################################################    USER MANAGEMENT     ############################################################


# User Mangement
def user_management(email):
    print('\n=============================================   USER MANAGEMENT   ==================================================')
    print('\n[1. Add Users (SUPER USER ONLY)]')
    print('[2. Verifying Customers (USER STATUS CHANGING)]')
    print('[3. Modify User Personal Details (SUPER USER ONLY)]')
    print('[4. Disable User Access (SUPER USER ONLY)]')
    print('[5. Inquiry of User\'s System Usage (SUPER USER ONLY)]')
    print('[6. Check Customer and Inventory Staff Order Status]')
    print('[7. Modify Customer and Inventory Staff Order Status]')
    print('[8. Reports]')
    print('[X. Exit]')

    while True:
        user_menu_choice = input('\nPlease enter your choice (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if user_menu_choice == '1':
            # Log the action
            log_message('INFO', 'user_management', email, 'User selected add users function')
            add_user(email)
            return

        elif user_menu_choice == '2':
            log_message('INFO', 'user_management', email, 'User selected verifying user function')
            verifying_user(email)
            return
        
        elif user_menu_choice == '3':
            # Log the action
            log_message('INFO', 'user_management', email, 'User selected modify user function')           
            modify_user(email)
            return
        
        elif user_menu_choice == '4':
            # Log the action
            log_message('INFO', 'user_management', email, 'User selected disable user function')          
            disable_user_access(email)
            return

        elif user_menu_choice == '5':
            # Log the action
            log_message('INFO', 'user_management', email, 'User selected inquiry user system usage function')           
            inquiry_user_system_usage(email)
            return

        elif user_menu_choice == '6':
            # Log the action
            log_message('INFO', 'user_management', email, 'User selected order checker function')
            order_checker(email)
            return
        
        elif user_menu_choice == '7':
            # Log the action
            log_message('INFO', 'user_management', email, 'User selected modify order status function')
            modify_order_status(email)
            return
        
        elif user_menu_choice == '8':
            # Log the action
            log_message('INFO', 'user_management', email, 'User selected reports for user management function')              
            reports_for_user_management(email)
            return
        
        elif user_menu_choice == 'x':
            if email == super_user_email:
                log_message('INFO', 'user_management', email, 'User exiting user management to super user menu')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                super_user_menu(email)
                return
            
            else:
                log_message('INFO', 'user_management', email, 'User exiting user management to main menu')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                main_menu(None)
                return            
        
        else:
            log_message('ERROR', 'user_management', email, 'Invalid input received')
            invalid_input()


## Function for adding new user (Managed by Super User)
def add_user(email):
    if email != super_user_email:
        print('\n----- [System Message]: You do not have permission to use the function')
        log_message('WANING', 'add_user', email, 'User tried to access super user only\'s function')
        print('\n====================================================================================================================')
        user_management(email)
        return

    print('\n=================================================   ADD USER   =====================================================')
    print('\nEnter \'x\' to exit')
    # Define valid status
    valid_status = ['customers', 'admin', 'inventory staff']
    new_users = []

    while True:
        new_email = (input('\nPlease enter the new user email (e.g. xxx@gmail.com): ')).lower()
        log_message('INFO', 'add_user', email, f'New user account\'s email [{new_email}] entered')

        if new_email == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'add_user', email, 'User exiting add user function to user management function')
            user_management(email) 
            return
        
        elif new_email == super_user_email:
            print(f'\n----- [System Message]: There can only be 1 super user in this system')
            print('\n====================================================================================================================')
            log_message('WARNING', 'add_user', email, 'Attempted to register as super user')
            user_management(email)
            return
        
        else:        
            if check_email_validity(new_email):
                # Checking existence of email
                if find_user_email(new_email):
                    print(f'\n----- [System Message]: A user with email \'{new_email}\' is already registered')
                    print('\n====================================================================================================================')
                    log_message('INFO', 'add_user', email, 'User already registered with email')

                    while True:
                        selection = input('\nWould you like to proceed to modify user\'s details page? (y/n): ').lower()

                        if selection == 'y':
                            log_message('INFO', 'add_user', email, 'User choosing to proceed to modify user\' details page')
                            modify_user(email)
                            return
                            
                        elif selection == 'n':
                            log_message('INFO', 'add_user', email, 'User choosing to re-adding new user')
                            add_user(email)
                            return
                            
                        else:
                            log_message('ERROR', 'add_user', email, 'Invalid input received')
                            invalid_input()
                else:
                    break
            else:
                continue

    while True:
        password = input('\nPlease enter the password\nMinimum 8 characters long, contain special character, number and upper lower case): ')
        log_message('INFO', 'add_user', email, f'New user account\'s password [{password}] entered')


        if password.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'add_user', email, 'User exiting during password entry to user management')
            user_management(email)
            return

        elif not check_password_strength(password): # If the check_password_strength function return FALSE, it will loops again
            log_message('WARNING', 'add_user', email, 'Password does not meet strength requirements')
            continue

        else:
            break

    # Double checking of password
    while True:
        dc_password = input('\nPlease double confirm the password: ')

        if dc_password.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'add_user', email, 'User exiting during password confirmation to user management')
            user_management(email)
            return
        
        elif password != dc_password:
            print('\n----- [System Message]: Please check again your password. It is CASE SENSITIVE')
            print('\n====================================================================================================================')
            log_message('WARNING', 'add_user', email, 'Double confirm password doesn\'t match with initial password')
        
        else:
            password = hashing(password)
            break

    while True:
        name = input('\nPlease enter the name: ')
        log_message('INFO', 'add_user', email, f'New user name [{name}] entered')

        if name == '' or name.isspace() or any(is_symbol(char) for char in name):
            log_message('ERROR', 'add_user', email, 'Invalid input received')
            invalid_input()

        else:
            break

    while True:
        ic = input('\nPlease enter the 12 digit IC number (without hyphens \'-\'): ')
        log_message('INFO', 'add_user', email, f'New user\'s IC [{ic}] entered')

        if len(ic) == 12 and ic.isdigit():
            break

        else:
            print('\n----- [System Message]: Please enter a valid IC number')
            print('\n===================================================================================================================')
            log_message('WARNING', 'add_user', email, 'Invalid IC number entered')

    while True:
        phone = input('\nPlease enter the phone number (e.g. 601xxxxxxxx): ')
        log_message('INFO', 'add_user', email, f'New user\'s phone number [{phone}] entered')

        if phone.isdigit() and (phone[:3] == '601') and (len(phone) >= 10):
            break
        else:
            print('\n----- [System Message]: Please enter a valid phone number')
            print('\n====================================================================================================================')
            log_message('WARNING', 'add_user', email, 'Invalid phone number entered')

    while True:
        address_1 = input("\nPlease enter the address 1: ").upper()
        # Log the action
        log_message('INFO', 'add_user', email, f'New user\'s address 1 [{address_1}] entered')
        if address_1 == '' or address_1.isspace():
            print("\n----- [System Message]: Please enter a valid address 1.")
            print('\n====================================================================================================================')
            # Log the action
            log_message('ERROR', 'add_user', email, 'Invalid address 1 input')  
        else:
            break

    address_2 = input('\nPlease enter the address line 2 (leave it blank if not needed): ').upper()

    if address_2 == '' or address_2.isspace():
        address_2 = '-'
        log_message('INFO', 'add_user', email, f'New user\'s address 2 [{address_2}] entered')

    while True:
            postal_code = input('\nPlease enter the postal code: ')
            if len(postal_code) == 5 and postal_code.isdigit():
                break
            else:
                print('\n----- [System Message]: Please enter a valid postal code')
                print('\n====================================================================================================================')
                log_message('WARNING', 'add_user', email, 'Invalid postal code entered')

    while True:
        city = input("\nPlease enter the city: ").upper()
        # Log the action
        log_message('INFO', 'add_user', email, f'New user\'s city [{city}] entered')
        if city == '' or city.isspace() or any(char.isdigit() for char in city):
            print("\n----- [System Message]: Please enter a valid city.")
            print('\n====================================================================================================================')
            # Log the action
            log_message('ERROR', 'add_user', email, 'Invalid city input')
        else:
            break

    # Asking for state
    while True:
        print('\n1. KUALA LUMPUR, 2. LABUAN, 3. PUTRAJAYA, 4. JOHOR, 5. KEDAH\n6. KELANTAN, 7. MELAKA, 8. NEGERI SEMBILAN, 9. PAHANG, 10. PULAU PINANG\n11. PERAK, 12. PERLIS, 13. SABAH, 14. SARAWAK, 15. SELANGOR, 16. TERENGGANU')
        state = input('Please select the state (e.g. 1): ')
        if state == '1':
            state = 'KUALA LUMPUR'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '2':
            state = 'LABUAN'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '3':
            state = 'PUTRAJAYA'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '4':
            state = 'JOHOR'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '5':
            state = 'KEDAH'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '6':
            state = 'KELANTAN'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '7':
            state = 'MELAKA'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '8':
            state = 'NEGERI SEMBILAN'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '9':
            state = 'PAHANG'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '10':
            state = 'PULAU PINANG'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '11':
            state = 'PERAK'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '12':
            state = 'PERLIS'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '13':
            state = 'SABAH'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '14':
            state = 'SARAWAK'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '15':
            state = 'SELANGOR'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        elif state == '16':
            state = 'TERENGGANU'
            log_message('INFO', 'add_user', email, f'New user\'s state [{state}] selected')
            break
        else:
            log_message('ERROR', 'add_user', email, 'Invalid input received')
            invalid_input()
    
    registered_date = dt.now().strftime('%d %b %y')
    print(f"\n----- [System Message]: Registered date is: {registered_date}")
    # Log the action
    log_message('INFO', 'add_user', email, f'Registered date [{registered_date}] displayed')

    while True:
        status = input("\nPlease enter new user's status (customers / admin / inventory staff): ").strip().lower()
        # Log the action
        log_message('INFO', 'add_user', email, f'New user\'s status [{status}] selected')
        if status in valid_status:
            break

        else:
            print("\n----- [System Message]: The status selected by you is not available in the list. Please try again.")
            print('\n====================================================================================================================')
            # Log the action
            log_message('ERROR', 'add_user', email, 'Invalid status input')

    print("\n----- [System Message]: Status selected is:", status)
    # Log the action
    log_message('INFO', 'add_user', email, 'Selected status displayed')

    new_users.append([new_email, password, name, ic, phone, address_1, address_2, postal_code, city, state, registered_date, status])
    save_user_details(new_users)

    print(f'\n----- [System Message]: {new_email} registered successfully')
    print('\n====================================================================================================================')
    log_message('INFO', 'add_user', email, 'User registered successfully')
    user_management(email)
    return


## Function for verifying new customers (Managed by admin and super user)
def verifying_user(email):
    print('\n==============================================   VERIFYING USER   ==================================================')
    new_data = []
    print('\nEnter \'x\' to exit')
    # Define valid status
    valid_status = ['customers', 'admin', 'inventory staff']

    while True:
        email_to_verify = input("\nPlease enter the user account's email to verify / change status: ").lower()
        # Log the action
        log_message('INFO', 'verifying_user', email, 'Account\'s email filled')
        if email_to_verify.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'verifying_user', email, 'User exiting verifying user function to user management function')
            user_management(email)
            return
        
        elif email_to_verify == super_user_email:
            print(f'\n----- [System Message]: You are not allowed to change the status of super user')
            print('\n====================================================================================================================')
            log_message('WARNING', 'modify_user', email, 'Attempted to modify status of super user')
            continue
        
        else:        
            if check_email_validity(email_to_verify):
                break

            else:
                print("\n----- [System Message]: Invalid email format. Please try again.")
                print('\n====================================================================================================================')
                log_message('ERROR', 'verifying_user', email, 'Invalid email format')
    
    try:
        user_details = find_user_email(email_to_verify)
        old_status = user_details[-1]
        print(f'\n----- [System Message]: User current status: {old_status}')
        log_message('INFO', 'verifying_user', email, 'Account\'s current status displayed')

    except TypeError:
        print(f'\n----- [System Message]: The email \'{email_to_verify}\' is not exist')
        print('\n====================================================================================================================')
        log_message('WARNING', 'verifying_user', email, 'Email not exist')

        while True:
            selection = input('\nWould you like to proceed to add user function? (y/n): ').lower()

            if selection == 'y':
                log_message('INFO', 'verifying_user', email, 'User choosing to proceed to add user function')
                add_user(email)
                return
                
            elif selection == 'n':
                log_message('INFO', 'verifying_user', email, 'User choosing to re-verify')
                verifying_user(email)
                return
                
            else:
                log_message('ERROR', 'verifying_user', email, 'Invalid input received')
                invalid_input()

    if 'admin' in old_status and email != super_user_email:
        log_message('WARNING', 'verifying_user', email, 'User trying to verify admin\'s account')
        print("\n----- [System Message]: Your are not allowed to verify admin's account")
        user_management(email)
        return

    # Check if user input status is valid or not
    while True:
        new_status = input("\nPlease enter new status (customers / admin / inventory staff): ").strip().lower()
        log_message('INFO', 'verifying_user', email, f'Account\'s new status {new_status} has been choosen')
        if new_status not in valid_status:
            print("\n----- [System Message]: Invalid status. Please enter a valid status.")
            log_message('ERROR', 'verifying_user', email, 'Invalid status')
    
        else:
            # If valid, replace the old status with new status and save it
            if new_status == 'admin' and email != super_user_email:
                log_message('WARNING', 'verifying_user', email, 'User trying to verify admin\'s account')
                print("\n----- [System Message]: Your are not allowed to verify admin's account")
                user_management(email)
                return
            
            else:
                user_details[-1] = new_status
                new_data.append(user_details)
                update_user_details(email_to_verify, new_data)
                print(f"\n----- [System Message]: Status for {email_to_verify} updated to {new_status}")
                # Log the action
                log_message('INFO', 'verifying_user', email, 'Status done changed')
                log_message('INFO', 'verifying_user', email, f"{email_to_verify} has been changed from [{old_status}] to [{new_status}]")
                user_management(email)
                return


## Function for modifying user details (Managed by Super User)
def modify_user(email):
    if email != super_user_email:
        print('\n----- [System Message]: You do not have permission to use the function')
        log_message('WANING', 'modify_user', email, 'User tried to access super user only\'s function')
        print('\n====================================================================================================================')
        user_management(email)
        return
    print('\n==============================================     MODIFY USER   ===================================================')
    print('\nEnter \'x\' to exit')

    while True:
        email_to_modify = input("\nPlease enter the user account's email to modify user personal details: ")
        # Log the action
        log_message('INFO', 'modify_user', email, f'Account\'s email [{email_to_modify}] filled')
        if email_to_modify.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'modify_user', email, 'User exiting modify user function to user management function')
            user_management(email)
            return
        
        else:        
            if check_email_validity(email_to_modify):
                break

            else:
                print("\n----- [System Message]: Invalid email format. Please try again.")
                print('\n====================================================================================================================')
                log_message('ERROR', 'modify_user', email, 'Invalid email format')
    
    if find_user_email(email_to_modify):
        modifying_user(email, email_to_modify)
        return

    else:
        print(f'\n----- [System Message]: The email \'{email_to_modify}\' is not exist')
        print('\n====================================================================================================================')
        log_message('WARNING', 'modify_user', email, 'Email not exist')

        while True:
            selection = input('\nWould you like to proceed to add user function? (y/n): ').lower()

            if selection == 'y':
                log_message('INFO', 'modify_user', email, 'User choosing to proceed to add user function')
                add_user(email)
                return
                
            elif selection == 'n':
                log_message('INFO', 'modify_user', email, 'User choosing to re-modify')
                modify_user(email)
                return
                
            else:
                log_message('ERROR', 'modify_user', email, 'Invalid input received')
                invalid_input()


#### Second Part of Modify User                
def modifying_user(email, email_to_modify):
    new_details = []
    new_data = []
    old_data = find_user_email(email_to_modify)
    definder = ['Email: ', 'Password (Hashed): ', 'Name: ', 'IC Number: ', 'Phone number: ', 'Address Line 1: ', 'Address Line 2: ', 'Postal Code: ', 'City: ', 'State: ', 'Register Date: ', 'Status: ']
    print('\n====================================================================================================================')
    # Display current personal details
    print('\nCurrent personal details:\n') 
    for datum, element in zip(old_data, definder):
        new_details.append(datum)
        print(element + datum)

    print('\n----------------------------------------------------------------')
    print('\n[1. Change Email]')
    print('[2. Change Password]')
    print('[3. Change Name]')
    print('[4. Change IC Number]')
    print('[5. Change Phone Number]')
    print('[6. Change Address Line 1]')
    print('[7. Change Address Line 2]')
    print('[8. Change Postal Code]')
    print('[9. Change City]')
    print('[10. Change State]')
    print('[X. Exit]')

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').strip().lower()
        print('\n====================================================================================================================')
        print('\nEnter \'x\' to exit')

        if choice == '1':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing email')
                new_email = input('\nPlease enter new email (e.g. xxx@gmail.com): ').strip().lower()
                if new_email.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                
                elif new_email == super_user_email:
                    print(f'\n----- [System Message]: There can only be 1 super user in this system')
                    print('\n====================================================================================================================')
                    log_message('WARNING', 'modifying_user', email, 'Attempted to modify email as super user')
                    continue

                else:        
                    if check_email_validity(new_email):
                        user_details = find_user_email(new_email)
                        if find_user_email(new_email):
                            print(f"\n----- [System Message]: The {new_email} already belongs to {user_details[2]}")
                            print('\n====================================================================================================================')
                            log_message('ERROR', 'modifying_user', email, 'Email already exist in the system')

                        else:
                            new_details[0] = new_email
                            new_data.append(new_details)
                            update_user_details(email_to_modify, new_data)
                            print('\n----- [System Message]: Email updated successfully')
                            log_message('INFO', 'modifying_user', email, f'Email updated successfully from [{old_data[0]}] to [{new_details[0]}]')
                            modifying_user(email, email_to_modify=new_email)
                            return
                        
                    else:
                        print("\n----- [System Message]: Invalid email format. Please try again.")
                        print('\n====================================================================================================================')
                        log_message('ERROR', 'modifying_user', email, 'Invalid email format')             

        elif choice == '2':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing password')
                password = input('\nPlease enter new password\nMinimum 8 characters long, contain special character, number and upper lower case): ')
                if password.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif not check_password_strength(password):
                    log_message('WARNING', 'modifying_user', email, 'Password does not meet strength requirements')
                    continue
                else:
                    dc_password = input('\nPlease double confirm your password: ')
                    if dc_password.lower() == 'x':
                        log_message('INFO', 'modifying_user', email, 'User reselect option')
                        modifying_user(email, email_to_modify)
                        return
                    elif password != dc_password:
                        print('\n----- [System Message]: Please check again your password. It is CASE SENSITIVE')
                        print('\n====================================================================================================================')
                        log_message('WARNING', 'modifying_user', email, 'Double confirm password doesn\'t match with initial password')
                    else:
                        password = hashing(password)
                        new_details[1] = password
                        new_data.append(new_details)
                        update_user_details(email_to_modify, new_data)
                        print('\n----- [System Message]: Password updated successfully')
                        log_message('INFO', 'modifying_user', email, f'Password updated successfully from [{old_data[1]}] to [{new_details[1]}]')
                        modifying_user(email, email_to_modify)
                        return
            
        elif choice == '3':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing name')
                name = input('\nPlease enter new name: ')
                if name.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif name == '' or name.isspace() or any(is_symbol(char) for char in name):
                    log_message('ERROR', 'modifying_user', email, 'Invalid input received')
                    invalid_input()
                else:
                    new_details[2] = name
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: Name updated successfully')
                    log_message('INFO', 'modifying_user', email, f'Name updated successfully from [{old_data[2]}] to [{new_details[2]}]')
                    modifying_user(email, email_to_modify)
                    return
            
        elif choice == '4':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing IC number')
                ic = input('\nPlease enter new 12 digit IC number (without hyphens \'-\'): ')
                if ic.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif len(ic) == 12 and ic.isdigit():
                    new_details[3] = ic
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: IC number updated successfully')
                    log_message('INFO', 'modifying_user', email, f'IC number updated successfully from [{old_data[3]}] to [{new_details[3]}]')
                    modifying_user(email, email_to_modify)
                    return
                else:
                    log_message('ERROR', 'modifying_user', email, 'Invalid input received')
                    invalid_input()            
            
        elif choice == '5':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing phone number')
                phone_num = input('\nEnter new phone number (e.g. 601xxxxxxxx): ')
                if phone_num.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif phone_num.isdigit() and (phone_num[:3] == '601') and (len(phone_num) >= 10):
                    new_details[4] = phone_num
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: Phone number updated successfully')
                    log_message('INFO', 'modifying_user', email, f'Phone number updated successfully from [{old_data[4]}] to [{new_details[4]}]')
                    modifying_user(email, email_to_modify)
                    return
                else:
                    log_message('ERROR', 'modifying_user', email, 'Invalid input received')
                    invalid_input()
                
        elif choice == '6':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing address line 1')
                address_1 = input('\nEnter new address line 1: ').upper()
                if address_1.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif address_1 == '' or address_1.isspace():
                    log_message('ERROR', 'modifying_user', email, 'Invalid input received')
                    invalid_input()
                else:
                    new_details[5] = address_1
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: Address line 1 updated successfully')
                    log_message('INFO', 'modifying_user', email, f'Address line 1 updated successfully from [{old_data[5]}] to [{new_details[5]}]')
                    modifying_user(email, email_to_modify)
                    return
            
        elif choice == '7':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing address line 2')
                address_2 = input('\nEnter new address line 2 (leave it blank if not needed): ').upper()
                if address_2.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif address_2 == '' or address_2.isspace():
                    address_2 = '-'
                    new_details[6] = address_2
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: Address line 2 updated successfully')
                    log_message('INFO', 'modifying_user', email, f'Address line 2 updated successfully from [{old_data[6]}] to [{new_details[6]}]')
                    modifying_user(email, email_to_modify)
                    return
                else:
                    new_details[6] = address_2
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: Address line 2 updated successfully')
                    log_message('INFO', 'modifying_user', email, f'Address line 2 updated successfully from [{old_data[6]}] to [{new_details[6]}]')
                    modifying_user(email, email_to_modify)
                    return
            
        elif choice == '8':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing postal code')
                postal_code = input('\nEnter new postal code: ')
                if postal_code.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif len(postal_code) == 5 and postal_code.isdigit():
                    new_details[7] = postal_code
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: Postal code updated successfully')
                    log_message('INFO', 'modifying_user', email, f'Postal code updated successfully from [{old_data[7]}] to [{new_details[7]}]')
                    modifying_user(email, email_to_modify)
                    return
                else:
                    log_message('ERROR', 'modifying_user', email, 'Invalid input received')
                    invalid_input()
            
        elif choice == '9':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing city')
                city = input('\nPlease enter new city: ').upper()
                if city.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif city == '' or city.isspace() or any(char.isdigit() for char in city):
                    log_message('ERROR', 'modifying_user', email, 'Invalid input received')
                    invalid_input()
                else:
                    new_details[8] = city
                    new_data.append(new_details)
                    update_user_details(email_to_modify, new_data)
                    print('\n----- [System Message]: City updated successfully')
                    log_message('INFO', 'modifying_user', email, f'City updated successfully from [{old_data[8]}] to [{new_details[8]}]')
                    modifying_user(email, email_to_modify)
                    return
            
        elif choice == '10':
            while True:
                log_message('INFO', 'modifying_user', email, 'User changing state')
                print('\n1. KUALA LUMPUR, 2. LABUAN, 3. PUTRAJAYA, 4. JOHOR, 5. KEDAH\n6. KELANTAN, 7. MELAKA, 8. NEGERI SEMBILAN, 9. PAHANG, 10. PULAU PINANG\n11. PERAK, 12. PERLIS, 13. SABAH, 14. SARAWAK, 15. SELANGOR, 16. TERENGGANU')
                state = input('\nPlease select new state (e.g. 1): ')
                if state.lower() == 'x':
                    log_message('INFO', 'modifying_user', email, 'User reselect option')
                    modifying_user(email, email_to_modify)
                    return
                elif state == '1':
                    new_details[9] = 'KUALA LUMPUR'
                    break
                elif state == '2':
                    new_details[9] = 'LABUAN'
                    break
                elif state == '3':
                    new_details[9] = 'PUTRAJAYA'
                    break
                elif state == '4':
                    new_details[9] = 'JOHOR'
                    break
                elif state == '5':
                    new_details[9] = 'KEDAH'
                    break
                elif state == '6':
                    new_details[9] = 'KELANTAN'
                    break
                elif state == '7':
                    new_details[9] = 'MELAKA'
                    break
                elif state == '8':
                    new_details[9] = 'NEGERI SEMBILAN'
                    break
                elif state == '9':
                    new_details[9] = 'PAHANG'
                    break
                elif state == '10':
                    new_details[9] = 'PULAU PINANG'
                    break
                elif state == '11':
                    new_details[9] = 'PERAK'
                    break
                elif state == '12':
                    new_details[9] = 'PERLIS'
                    break
                elif state == '13':
                    new_details[9] = 'SABAH'
                    break
                elif state == '14':
                    new_details[9] = 'SARAWAK'
                    break
                elif state == '15':
                    new_details[9] = 'SELANGOR'
                    break
                elif state == '16':
                    new_details[9] = 'TERENGGANU'
                    break
                else:
                    log_message('ERROR', 'modifying_user', email, 'Invalid input received')
                    invalid_input()

            new_data.append(new_details)
            update_user_details(email_to_modify, new_data)
            print('\n----- [System Message]: State updated successfully')
            log_message('INFO', 'modifying_user', email, f'State updated successfully from [{old_data[9]}] to [{new_details[9]}]')
            modifying_user(email, email_to_modify)
            return
            
        elif choice == 'x':
            log_message('INFO', 'modifying_user', email, 'User exiting modifying user funtion to user management function')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            user_management(email)
            return
        
        else:
            log_message('ERROR', 'modifying_user', email, 'Invalid input received')
            invalid_input()


# Function for disabling user access (Super User Only)
def disable_user_access(email):
    if email != super_user_email:
        print('\n----- [System Message]: You do not have permission to use the function')
        log_message('WANING', 'disable_user_access', email, 'User tried to access super user only\'s function')
        print('\n====================================================================================================================')
        user_management(email)
        return
    
    print('\n==========================================     DISABLE USER ACCESS   ===============================================')
    new_data = []
    print('\nEnter \'x\' to exit')

    while True:
        email_to_disable_user = input("\nPlease enter the user account's email to disable user access: ")
        # Log the action
        log_message('INFO', 'disable_user_access', email, f'Account\'s email [{email_to_disable_user}] filled')
        if email_to_disable_user.lower() == 'x':
            print('\n====================================================================================================================')
            log_message('INFO', 'disable_user_access', email, 'User exiting disable user access function to user management function')
            user_management(email)
            return
        
        elif email_to_disable_user == super_user_email:
            print(f'\n----- [System Message]: You are not allowed to disable super user account')
            print('\n====================================================================================================================')
            log_message('WARNING', 'disable_user_access', email, 'Attempted to disable super user account')
            continue
        
        else:        
            if check_email_validity(email_to_disable_user):
                break

            else:
                print("\n----- [System Message]: Invalid email format. Please try again.")
                print('\n====================================================================================================================')
                log_message('ERROR', 'disable_user_access', email, 'Invalid email format')
    
    try:
        user_details = find_user_email(email_to_disable_user)
        old_status = user_details[-1]
        if 'disabled' in old_status:
            print("\n----- [System Message]: User is already disabled.")
            # Log the action
            log_message('ERROR', 'disable_user_access', email, 'User is already disabled')
            disable_user_access(email)
        else:
            print(f'\n----- [System Message]: User current status: {old_status}')
            log_message('INFO', 'disable_user_access', email, 'Account\'s current status displayed')

    except TypeError:
        print(f'\n----- [System Message]: The email \'{email_to_disable_user}\' is not exist')
        print('\n====================================================================================================================')
        log_message('WARNING', 'disable_user_access', email, 'Email not exist')

        while True:
            selection = input('\nWould you like to proceed to add user function? (y/n): ').lower()

            if selection == 'y':
                log_message('INFO', 'disable_user_access', email, 'User choosing to proceed to add user function')
                add_user(email)
                return
                
            elif selection == 'n':
                log_message('INFO', 'disable_user_access', email, 'User choosing to re-disable')
                disable_user_access(email)
                return
                
            else:
                log_message('ERROR', 'disable_user_access', email, 'Invalid input received')
                invalid_input()

    while True:
        selection = input(f'\nAre you sure to disable this account -> {email_to_disable_user}? (y/n): ').lower()
        if selection == 'y':
            user_details[-1] = f'{old_status} (disabled)'
            new_data.append(user_details)
            update_user_details(email_to_disable_user, new_data)
            print(f"\n----- [System Message]: Status for {email_to_disable_user} updated to {user_details[-1]}")
            # Log the action
            log_message('INFO', 'disable_user_access', email, 'User has been disabled')
            log_message('INFO', 'disable_user_access', email, f"{email_to_disable_user} has been changed from [{old_status}] to [{user_details[-1]}]")
            user_management(email)
            return
            
        elif selection == 'n':
            log_message('INFO', 'disable_user_access', email, 'User choosing to re-disable')
            disable_user_access(email)
            return
            
        else:
            log_message('ERROR', 'disable_user_access', email, 'Invalid input received')
            invalid_input()


# Function for inquiring about user's system usage (Super User Only)
def inquiry_user_system_usage(email):
    if email != super_user_email:
        print('\n----- [System Message]: You do not have permission to use the function')
        log_message('WANING', 'inquiry_user_system_usage', email, 'User tried to access super user only\'s function')
        print('\n====================================================================================================================')
        user_management(email)
        return
    print('\n=======================================     INQUIRY USER SYSTEM USAGE   ============================================')
    print('\nEnter \'x\' to exit')

    while True:
        needed_email = input('\nPlease enter the email that you would like the logs belongs to or leave blank for all: ').strip().lower() or 'all user'

        if needed_email:
            if needed_email.lower() == 'x':
                log_message('INFO', 'inquiry_user_system_usage', email, 'User exiting reports for inquiry user system usage to user management')
                user_management(email)
                return
            
            else:
                user_list = display_user_details(None, None)
                if (needed_email in user_list) or needed_email == 'all user':
                    break
                else:
                    print(f'\n----- [System Message]: Email: {needed_email} is not exist')
                    print('\n====================================================================================================================')
                    log_message('ERROR', 'inquiry_user_system_usage', email, 'Invalid email entered')
                    continue
        
    level = input("\nPlease enter log level (INFO, WARNING, ERROR) or leave blank for all: ").strip() or None
    page = input("\nPlease enter page name (e.g. login) or leave blank for all: ").strip() or None
    start_time_str = input("\nPlease enter start date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:04:07) or leave blank for no start time: ").strip()
    end_time_str = input("\nPlease enter end date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:05:07) or leave blank for no end time: ").strip()
    keyword = input("\nPlease enter keyword to search in messages or leave blank for no keyword: ").strip() or None
    print('\n====================================================================================================================')
    
    try:
        start_time = dt.strptime(start_time_str, "%d %b %y %H:%M:%S") if start_time_str else None
        end_time = dt.strptime(end_time_str, "%d %b %y %H:%M:%S") if end_time_str else None

    except ValueError or UnboundLocalError:
        log_message('ERROR', 'inquiry_user_system_usage', email, 'Invalid date format entered')
        print('\n----- [System Message]: Invalid date format entered')
        inquiry_user_system_usage(email)
        return

    except Exception as e:
        print(e)
        print('\n----- [System Message]: Please check again your date format entered')
        inquiry_user_system_usage(email)
        return
    
    # Parse the log data
    parsed_logs = find_log_message(needed_email)

    # Apply filters
    filtered_logs = filtering_log(parsed_logs, level, page, start_time, end_time, keyword)

    if not filtered_logs:
        log_message('ERROR', 'inquiry_user_system_usage', email, 'No matched result')
        print('\n----- [System Message]: No matched result. Please double check the data you entered')
        inquiry_user_system_usage(email)
        return

    else:
        # Generate report
        log_message('INFO', 'inquiry_user_system_usage', email, 'Report generated successful')
        report = generate_user_report(filtered_logs, needed_email)

    # Print the report
    print(report)
    user_management(email)
    return


# Function for checking customer or staff order status (Managed by admin and super user)
def order_checker(email):
    print('\n============================================     ORDER CHECKER     =================================================')
    print('\n[1. Customer Order Checker]')
    print('[2. Inventory Staff Order Checker]')
    print('[3. Modify Order Status]')
    print('[X. Exit]')

    while True:
        checker_choice = input('\nPlease enter your choice for order checker (e.g. 1): ')
        print('\n====================================================================================================================')

        if checker_choice == '1':
            # Log the action
            log_message('INFO', 'order_checker', email, 'User selected customer order checker')
            while True:
                print('\nEnter \'x\' to exit')
                order_id = input('\nPlease enter the order ID: ').lower()
                print('\n====================================================================================================================')
                if order_id == 'x':
                    log_message('INFO', 'order_checker', email, 'User cancelled the action')
                    order_checker(email)
                    return
                
                else:
                    log_message('INFO', 'order_checker', email, f'User searched for order ID: {order_id}')
                    find_order(None, order_id, email, 'user management')
                    return
        
        elif checker_choice == '2':
            # Log the action
            log_message('INFO', 'order_checker', email, 'User selected inventory staff order checker')
            while True:
                print('\nEnter \'x\' to exit')
                order_id = input('\nPlease enter the order ID: ').lower()
                print('\n====================================================================================================================')
                if order_id == 'x':
                    log_message('INFO', 'order_checker', email, 'User cancelled the action')
                    order_checker(email)
                    return
                
                else:
                    log_message('INFO', 'order_checker', email, f'User searched for order ID: {order_id}')
                    find_inventory_staff_order(email, order_id, None, 'user management')
                    return
        
        elif checker_choice == '3':
            log_message('INFO', 'order_checker', email, 'User selected modify order status')
            modify_order_status(email)
            return
        
        elif checker_choice == 'x':
            log_message('INFO', 'order_checker', email, 'User exiting order checker to user management')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            user_management(email)
            return

        else:
            log_message('ERROR', 'order_checker', email, 'Invalid input received')
            invalid_input()


# Function for modifying customer or staff order status (Managed by admin and super user)
def modify_order_status(email):
    print('\n=========================================     MODIFY ORDER STATUS     ==============================================')
    print('\n[1. Modify Customer Order Status]')
    print('[2. Modify Inventory Staff Order Status]')
    print('[X. Exit]')

    while True:
        modify_choice = input('\nPlease enter your choice (e.g. 1): ')
        print('\n====================================================================================================================')
        order_status_list = ['pending', 'processing and shipping', 'completed', 'cancelled']

        if modify_choice == '1':
            # Log the action
            log_message('INFO', 'modify_order_status', email, 'User selected modify customer order status')
            while True:
                print('\nEnter \'x\' to exit')
                order_id = input('\nPlease enter the order ID: ').lower()
                print('\n====================================================================================================================')
                if order_id == 'x':
                    log_message('INFO', 'modify_order_status', email, 'User cancelled the action')
                    modify_order_status(email)
                    return
                
                elif not order_id or order_id.isspace() or not order_id.isdigit():
                    log_message('INFO', 'modify_order_status', email, 'Invalid input received')
                    invalid_input()
                
                else:
                    while True:
                        new_status = input('\nWhat status would you like to change it to? (pending / processing and shipping / completed / cancelled): ').lower()
                        if new_status in order_status_list:
                            if not update_order(email, order_id, new_status, 'user management'):
                                log_message('INFO', 'modify_order_status', email, f'Order id: {order_id} update unsuccessful')
                                print(f'\n----- [System Message]: No order with order ID: {order_id} found')
                                print('\n====================================================================================================================')
                                modify_order_status(email)
                                return

                            else:
                                log_message('INFO', 'modify_order_status', email, f'Order id: {order_id} update successful')
                                print(f"\n----- [System Message]: Order with order ID: {order_id} updated successful")
                                print('\n====================================================================================================================')
                                user_management(email)
                                return
                        else:
                            log_message('ERROR', 'modify_order_status', email, 'Invalid input received')
                            invalid_input()
                
        elif modify_choice == '2':
            # Log the action
            log_message('INFO', 'modify_order_status', email, 'User selected modify inventory staff order status')
            while True:
                print('\nEnter \'x\' to exit')
                order_id = input('\nPlease enter the order ID: ').lower()
                print('\n====================================================================================================================')
                if order_id == 'x':
                    log_message('INFO', 'modify_order_status', email, 'User cancelled the action')
                    modify_order_status(email)
                    return
                
                elif not order_id or order_id.isspace() or not order_id.isdigit():
                    log_message('INFO', 'modify_order_status', email, 'Invalid input received')
                    invalid_input()
                
                else:
                    while True:
                        new_status = input('\nWhat status would you like to change it to? (pending / processing and shipping / completed / cancelled): ').lower()
                        if new_status in order_status_list:
                            if not update_inventory_staff_order(email, order_id, new_status, 'user management'):
                                log_message('INFO', 'modify_order_status', email, f'Order id: {order_id} update unsuccessful')
                                print(f'\n----- [System Message]: No order with order ID: {order_id} found')
                                print('\n====================================================================================================================')
                                modify_order_status(email)
                                return

                            else:
                                log_message('INFO', 'modify_order_status', email, f'Order id: {order_id} update successful')
                                print(f"\n----- [System Message]: Order with order ID: {order_id} updated successful")
                                print('\n====================================================================================================================')
                                user_management(email)
                                return
                        else:
                            log_message('ERROR', 'modify_order_status', email, 'Invalid input received')
                            invalid_input()                    
        
        elif modify_choice == 'x':
            log_message('INFO', 'modify_order_status', email, 'User exiting modify order status function to user management fucntion')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            user_management(email)
            return

        else:
            log_message('ERROR', 'modify_order_status', email, 'Invalid input received')
            invalid_input()


## Reports for User Management
def reports_for_user_management(email):
    print('\n===============================================     REPORTS     ====================================================')
    print('\nEnter \'x\' to exit')
    level = input("\nPlease enter log level (INFO, WARNING, ERROR) or leave blank for all: ").strip() or None
    
    if level:
        if level.lower() == 'x':
            log_message('INFO', 'reports_for_user_management', email, 'User exiting reports for user management to user management')
            user_management(email)
            return
    
    page = input("\nPlease enter page name (e.g. customer menu) or leave blank for all: ").strip() or None
    start_time_str = input("\nPlease enter start date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:04:07) or leave blank for no start time: ").strip()
    end_time_str = input("\nPlease enter end date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:05:07) or leave blank for no end time: ").strip()
    keyword = input("\nPlease enter keyword to search in messages or leave blank for no keyword: ").strip() or None
    print('\n====================================================================================================================')

    try:
        start_time = dt.strptime(start_time_str, "%d %b %y %H:%M:%S") if start_time_str else None
        end_time = dt.strptime(end_time_str, "%d %b %y %H:%M:%S") if end_time_str else None

    except ValueError or UnboundLocalError:
        log_message('ERROR', 'reports_for_user_management', email, 'Invalid date format entered')
        print('\n----- [System Message]: Invalid date format entered')
        reports_for_user_management(email)
        return

    except Exception as e:
        print(e)
        print('\n----- [System Message]: Please check again your date format entered')
        reports_for_user_management(email)
        return

    # Parse the log data
    parsed_logs = find_log_message(email)

    # Apply filters
    filtered_logs = filtering_log(parsed_logs, level, page, start_time, end_time, keyword)

    if not filtered_logs:
        log_message('ERROR', 'reports_for_user_management', email, 'No matched result')
        print('\n----- [System Message]: No matched result. Please double check the data you entered')
        reports_for_user_management(email)
        return

    else:
        # Generate report
        log_message('INFO', 'reports_for_user_management', email, 'Report generated successful')
        report = generate_user_report(filtered_logs, email)

    # Print the report
    print(report)
    user_management(email)
    return


###############################################################     INVENTORY MANAGEMENT    ################################################################


# Inventory Management
def inventory_management(email):
    print('\n===========================================   INVENTORY MANAGEMENT   ===============================================')
    print('\n[1. Stock Check / Adjustments]')
    print('[2. Purchase Order for New Computers / Spare Parts]')
    print('[3. Modify Purchase Order]')
    print('[4. Submit Order]')
    print('[5. Check Purchase Order Status]')
    print('[6. Cancel Purchase Order]')
    print('[7. Reports]')
    print('[8. Settings]')
    print('[X. Exit]')

    while True:
        inventory_management_choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if inventory_management_choice == '1':
            log_message('INFO', 'inventory_management', email, 'User selected stock check / adjustments')
            stock_check_adjustments(email)
            return
        
        elif inventory_management_choice == '2':        
            log_message('INFO', 'inventory_management', email, 'User selected purchase order for new computers / spare parts')
            purchase_order_for_new_computers_spare_parts(email)
            return
        
        elif inventory_management_choice == '3':       
            log_message('INFO', 'inventory_management', email, 'User selected modify purchase order')
            modify_purchase_order(email)
            return
        
        elif inventory_management_choice == '4':
            log_message('INFO', 'inventory_management', email, 'User selected submit order')
            submit_order(email)
            return
        
        elif inventory_management_choice == '5':
            log_message('INFO', 'inventory_management', email, 'User selected check purchase order status')
            check_purchase_order_status(email)
            return
        
        elif inventory_management_choice == '6':
            log_message('INFO', 'inventory_management', email, 'User selected cancel purchase order')
            cancel_purchase_order(email)
            return
        
        elif inventory_management_choice == '7':
            log_message('INFO', 'inventory_management', email, 'User selected reports for inventory management')
            reports_for_inventory_management(email)
            return
        
        elif inventory_management_choice == '8':
            log_message('INFO', 'inventory_management', email, 'User selected settings for inventory management')
            settings(email, 'inventory staff')
            return
        
        elif inventory_management_choice == 'x':
            if email == super_user_email:
                log_message('INFO', 'inventory_management', email, 'User exiting inventory management to super user menu')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                super_user_menu(email)
                return
            
            else:
                log_message('INFO', 'inventory_management', email, 'User exiting inventory management to main menu')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                main_menu(None)
                return
        
        else:
            log_message('ERROR', 'customer_menu', email, 'Invalid input received')
            invalid_input()


## Stock Check / Adjustments
def stock_check_adjustments(email):
    print('\n========================================   STOCK CHECK / ADJUSTMENTS   =============================================')
    print('\n[1. List Out all Items]')
    print('[2. Product Checking]')
    print('[3. Product Updating]')
    print('[4. Product Adding]')
    print('[X. Exit]')

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if choice == '1':
            log_message('INFO', 'stock_check_adjustments', email, 'User selected list out all items')
            display_product_details('listing all', 'product', 'inventory staff', email)
            return

        elif choice == '2':
            log_message('INFO', 'stock_check_adjustments', email, 'User selected product checking')
            product_checking(email)
            return
        
        elif choice == '3':
            log_message('INFO', 'stock_check_adjustments', email, 'User selected product updating')
            product_updating(email)
            return
        
        elif choice == '4':
            log_message('INFO', 'stock_check_adjustments', email, 'User selected product adding')
            product_adding(email)
            return
        
        elif choice == 'x':
            log_message('INFO', 'stock_check_adjustments', email, 'User exiting stock check adjustment to inventory management')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            inventory_management(email)
            return
        
        else:
            log_message('ERROR', 'stock_check_adjustments', email, 'Invalid input received')
            invalid_input()


### Check the Exisiting Product with Product ID
def product_checking(email):
    print('\n=============================================   PRODUCT CHECKING   =================================================')

    while True:
        print('\nEnter \'x\' to exit')
        productId = input('\nPlease enter the product ID that you would wish to search for: ').lower()

        if productId == 'x':
            log_message('INFO', 'product_checking', email, 'User exiting product checking to stock check / adjustment')
            stock_check_adjustments(email)
            return
        
        if not productId:
            log_message('ERROR', 'product_checking', email, 'Invalid input received')
            invalid_input()
        
        else:
            log_message('INFO', 'product_checking', email, f'Checking for product ID: {productId}')
            display_product_details('product id', productId, 'inventory staff', email)
            return
  

### Update the Product Details
def product_updating(email):
    new_details = []
    print('\n=============================================   PRODUCT UPDATING   =================================================')
    while True:
        print('\nEnter \'x\' to exit')
        productId = input('\nPlease enter the product ID that you would wish to edit (e.g. tp001): ').lower()
        if productId == 'x':
            log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
            stock_check_adjustments(email)
            return
            
        details = display_product_details('product id', productId, 'inventory staff from product updating', email)
        old_productID = details[0]
        old_productName = details[1]
        old_productDesc = details[2]
        old_productCategory = details[3]
        old_productPrice = details[4]
        old_stockStatus = details[5]
        old_manufacturer = details[6]
        break
            
    while True:
        print('\n[1. Change Product ID]')
        print('[2. Change Product Name]')
        print('[3. Change Description]')
        print('[4. Change Category]')
        print('[5. Change Price]')
        print('[6. Change Stock Status]')
        print('[7. Change Manufacturer]')
        print('[X. Exit]')
        choice = input('\nPlease select an option (e.g. 1): ').strip().lower()
        print('\n====================================================================================================================')

        if choice == '1':
            log_message('INFO', 'product_updating', email, 'Changing product ID')
            print('\nEnter \'x\' to exit')
            new_productId = (input('\nEnter new product id: ')).lower().strip()

            if new_productId == 'x':
                log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
                stock_check_adjustments(email)
                return            
            if not new_productId or new_productId.isspace() or not ((new_productId.startswith('tp') or new_productId.startswith('sr')) and new_productId[2:].isdigit() and len(new_productId) == 5):
                log_message('ERROR', 'product_updating', email, 'Invalid input received')
                print('\n----- [System Message]: Invalid product ID entered')
                print('\n====================================================================================================================')
                continue
            else:
                product_details = find_inventory('product id', new_productId, None)
                if product_details:
                    for product_detail in product_details:
                        log_message('WARNING', 'product_updating', email, f'The product ID: {new_productId} already exists and belongs to {product_detail[1]}')
                        print(f'\n----- [System Message]: The product ID: {new_productId} already exists and belongs to {product_detail[1]}')
                        print('\n====================================================================================================================')
                        continue
                else:
                    definder = 'product id'
                    new_details.append([productId, new_productId, definder])
                    update_inventory(new_details)
                    print("\n----- [System Message]: Product ID updated successfully")
                    log_message('INFO', 'product_updating', email, f'Changed product ID from {old_productID} to {new_productId}')
                    display_product_details('product id', new_productId, 'inventory staff from product updating', email)
                    print('\n====================================================================================================================')
                    productId = new_productId # Update the product ID to the latest product ID in case staff decided to change the name of the product also
                    continue
                
        elif choice == '2':
            log_message('INFO', 'product_updating', email, 'Changing product name')
            print('\nEnter \'x\' to exit')
            new_productName = input('\nEnter new product name: ')

            if new_productName.lower() == 'x':
                log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
                stock_check_adjustments(email)
                return
            if not new_productName or new_productName.isspace():
                log_message('ERROR', 'product_updating', email, 'Invalid input received')
                print('\n----- [System Message]: The product name cannot be empty')
                print('\n====================================================================================================================')
                continue
            else:               
                definder='product name'
                new_details.append([productId, new_productName, definder])
                update_inventory(new_details)
                print("\n----- [System Message]: Product name updated successfully")
                log_message('INFO', 'product_updating', email, f'Changed product name from {old_productName} to {new_productName}')
                display_product_details('product id', productId, 'inventory staff from product updating', email)
                print('\n====================================================================================================================')
                continue
            
        elif choice == '3':
            log_message('INFO', 'product_updating', email, 'Changing description')
            print('\nEnter \'x\' to exit')
            new_productDesc = input('\nEnter new description: ')

            if new_productDesc.lower() == 'x':
                log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
                stock_check_adjustments(email)
                return            
            if not new_productDesc or new_productDesc.isspace():
                new_productDesc = '-'

            definder='description'
            new_details.append([productId, new_productDesc, definder])
            update_inventory(new_details)
            print("\n----- [System Message]: Description updated successfully")
            log_message('INFO', 'product_updating', email, f'Changed description from {old_productDesc} to {new_productDesc}')
            display_product_details('product id', productId, 'inventory staff from product updating', email)
            print('\n====================================================================================================================')
            continue
            
        elif choice == '4':
            log_message('INFO', 'product_updating', email, 'Changing category')
            print('\nEnter \'x\' to exit')
            new_productCategory = input('\nEnter new category: ')

            if new_productCategory.lower() == 'x':
                log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
                stock_check_adjustments(email)
                return
            if not new_productCategory or new_productCategory.isspace() or any(is_symbol(char) for char in new_productCategory):
                log_message('ERROR', 'product_updating', email, 'Invalid input received')
                print("\n----- [System Message]: Invalid input received")
                print('\n====================================================================================================================')
                continue
            else:
                definder='category'
                new_details.append([productId, new_productCategory, definder])
                update_inventory(new_details)
                print("\n----- [System Message]: Category updated successfully")
                log_message('INFO', 'product_updating', email, f'Changed category from {old_productCategory} to {new_productCategory}')
                display_product_details('product id', productId, 'inventory staff from product updating', email)
                print('\n====================================================================================================================')
                continue
            
        elif choice == '5':
            log_message('INFO', 'product_updating', email, 'Changing price')
            print('\nEnter \'x\' to exit')
            new_productPrice = input('\nEnter new price: ')

            if new_productPrice.lower() == 'x':
                log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
                stock_check_adjustments(email)
                return
            if not new_productPrice or new_productPrice.isspace():
                log_message('ERROR', 'product_updating', email, 'Invalid input received')
                print('\n----- [System Message]: The price cannot be empty')
                print('\n====================================================================================================================')        
                continue    
            else:
                try:
                    new_productPrice  = round(float(new_productPrice), 2)
                    definder='price'
                    new_details.append([productId, f'{new_productPrice:.2f}', definder])
                    update_inventory(new_details)
                    print("\n----- [System Message]: Price updated successfully")
                    log_message('INFO', 'product_updating', email, f'Changed price from RM {old_productPrice} to RM {new_productPrice}')
                    display_product_details('product id', productId, 'inventory staff from product updating', email)
                    print('\n====================================================================================================================')

                except ValueError:
                    log_message('ERROR', 'product_updating', email, 'Invalid input received')
                    print('\n----- [System Message]: Please enter a valid integer price. Without \'RM\'')
                    print('\n====================================================================================================================')
                    continue
            
        elif choice == '6':
            log_message('INFO', 'product_updating', email, 'Changing stock status')
            print('\nEnter \'x\' to exit')
            new_stockStatus = input('\nEnter new stock status: ')

            if new_stockStatus.lower() == 'x':
                log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
                stock_check_adjustments(email)
                return
            if not new_stockStatus or new_stockStatus.isspace():
                log_message('ERROR', 'product_updating', email, 'Invalid input received')
                print('\n----- [System Message]: The stock number cannot be empty')
                print('\n====================================================================================================================')
                continue
            else:
                try:
                    new_stockStatus = int(new_stockStatus)
                    definder='real-time stock status'
                    new_details.append([productId, new_stockStatus, definder])
                    update_inventory(new_details)
                    print("\n----- [System Message]: Stock status updated successfully")
                    log_message('INFO', 'product_updating', email, f'Changed stock status from {old_stockStatus} unit(s) to {new_stockStatus} unit(s)')
                    display_product_details('product id', productId, 'inventory staff from product updating', email)
                    print('\n====================================================================================================================')

                except ValueError:
                    log_message('ERROR', 'product_updating', email, 'Invalid input received')
                    print('\n----- [System Message]: Please enter a valid stock number')
                    print('\n====================================================================================================================')
                    continue
            
        elif choice == '7':
            log_message('INFO', 'product_updating', email, 'Changing manufacturer')
            print('\nEnter \'x\' to exit')
            new_Manufacturer = input('\nEnter new manufacturer: ')

            if new_Manufacturer.lower() == 'x':
                log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
                stock_check_adjustments(email)
                return
            if not new_Manufacturer or new_Manufacturer.isspace():
                log_message('ERROR', 'product_updating', email, 'Invalid input received')
                print('\n----- [System Message]: The manufacturer cannot be empty')
                print('\n====================================================================================================================')
                continue
            else:
                definder='manufacturer'
                new_details.append([productId, new_Manufacturer, definder])
                update_inventory(new_details)
                print("\n----- [System Message]: Manufacturer updated successfully")
                log_message('INFO', 'product_updating', email, f'Changed manufacturer from {old_manufacturer} to {new_Manufacturer}')
                display_product_details('product id', productId, 'inventory staff from product updating', email)
                print('\n====================================================================================================================')
            
        elif choice == 'x':
            log_message('INFO', 'product_updating', email, 'User exiting product updating to stock check / adjustment')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            stock_check_adjustments(email)
            return
            
        else:
            log_message('ERROR', 'product_updating', email, 'Invalid input received')
            invalid_input()            


### Add New Product Into the Inventory (Log)
def product_adding(email):
    new_product = []
    print('\n==============================================   PRODUCT ADDING   ==================================================')
    
    # Ask for product id
    while True:
        print('\nEnter \'x\' to exit')
        productId = (input('\nPlease enter the product ID (e.g. tp001 or sr001): ')).lower()

        if productId == 'x':
            log_message('INFO', 'product_adding', email, 'User exiting product adding to stock check / adjustment')
            stock_check_adjustments(email)
            return
        
        if not productId or productId.isspace() or not ((productId.startswith('tp') or productId.startswith('sr')) and productId[2:].isdigit() and len(productId) == 5):
            log_message('WARNING', 'product_adding', email, 'Invalid product id entered')
            print('\n----- [System Message]: Invalid product ID entered')
            print('\n====================================================================================================================')

        else:
            break

    # Checking existance of product id
    product_details = find_inventory('product id', productId, None)

        
    if product_details:
        for product_detail in product_details:
            log_message('WARNING', 'product_adding', email, f'The product ID: {productId} already exists and belongs to {product_detail[1]}')
            print(f'\n----- [System Message]: The product ID: {productId} already exists and belongs to {product_detail[1]}')
            print('\n====================================================================================================================')

        while True:
            choice = input('\nWould you like to proceed to product updating page? (y/n): ').lower()

            if choice == 'y':
                log_message('INFO', 'product_adding', email, 'User choosing to proceed to product updating')
                product_updating(email)
                return
                
            elif choice == 'n':
                log_message('INFO', 'product_adding', email, 'User choosing to continue with product adding')
                product_adding(email)
                return
                
            else:
                log_message('ERROR', 'product_adding', email, 'Invalid input received')
                invalid_input()

    # Ask for product name
    while True:
        productName = input('\nPlease enter the name of this product: ')

        if productName:
            break

        else:
            log_message('WARNING', 'product_adding', email, 'Empty product name entered')
            print('\n----- [System Message]: The product name cannot be empty')
            print('\n====================================================================================================================')

    # Ask for description
    description = input('\nPlease enter the description of this product: ')

    if not description or description.isspace():
        description = '-'
    
    # Ask for category
    while True:
        category = input('\nWhat is the category of this product: ')

        if any(is_symbol(char) for char in category) or category.isspace() or category == '':
            log_message('WARNING', 'product_adding', email, 'Empty product category entered')
            print('\n----- [System Message]: Invalid input received')
            print('\n====================================================================================================================')

        else:
            break

    # Ask for price
    while True:
        price = input('\nWhat is the price of this product? (e.g. 100): ')

        if price:
            try:
                price = round(float(price), 2)
                break

            except ValueError:
                log_message('ERROR', 'product_adding', email, 'Invalid integer entered')
                print('\n----- [System Message]: Please enter a valid integer price. Without \'RM\'')
                print('\n====================================================================================================================')
        
        else:
            log_message('WARNING', 'product_adding', email, 'Empty price entered')
            print('\n----- [System Message]: The price cannot be empty')
            print('\n====================================================================================================================')

    # Ask for stock number
    while True:
        stock_num = input('\nWhat is the current stock number of this product: ')

        if stock_num:
            try:
                stock_num = int(stock_num)
                break

            except ValueError:
                log_message('ERROR', 'product_adding', email, 'Invalid integer entered')
                print('\n----- [System Message]: Please enter a valid stock number')
                print('\n====================================================================================================================')

        else:
            log_message('WARNING', 'product_adding', email, 'Empty stock number entered')
            print('\n----- [System Message]: The stock number cannot be empty')
            print('\n====================================================================================================================')

    # Ask for manufacturer
    while True:
        manufacturer = input('\nWho is the manufacturer of this product: ')

        if manufacturer:
            break

        else:
            log_message('WARNING', 'product_adding', email, 'Empty manufacturer entered')
            print('\n----- [System Message]: The manufacturer cannot be empty')
            print('\n====================================================================================================================')

    sales_history = 0
    date = dt.now().strftime('%d %b %y %H:%M:%S')

    new_product.append([productId, productName, description, category, f'{price:.2f}', stock_num, manufacturer, sales_history, date])
    save_inventory(email, new_product, productId, productName)
    return


## Get Input from Inventory Staff to Restock / Purchase New Product to Maintain / Update the Inventory
def purchase_order_for_new_computers_spare_parts(email):
    print('\n=============================      PURCHASE ORDER FOR NEW COMPUTERS / SPARE PARTS   ================================')
    current_cart = find_inventory_staff_cart(email, 'simple')
    print('\nShopping Cart:')

    try:
        print('\n'+current_cart)
        print('----------------------------------------------------------------')
        log_message('INFO', 'inventory_staff_add_to_cart', email, 'Displayed current cart')        

    except TypeError:
        print('\nThere is nothing in your shopping cart')
        print('\n----------------------------------------------------------------')
        log_message('INFO', 'inventory_staff_add_to_cart', email, 'Cart is empty')


    # Ask for product sku
    while True:        
        print('\nEnter \'x\' to exit')
        product_sku = input("\nPlease enter product SKU: ").lower()
        if product_sku == 'x':
            log_message('INFO', 'purchase_order_for_new_computers_spare_parts', email, 'User exiting inventory staff add to cart to inventory management')
            inventory_management(email)
            return
        elif product_sku == '' or product_sku.isspace():
            log_message('ERROR', 'purchase_order_for_new_computers_spare_parts', email, 'Invalid input received')
            invalid_input()
        else:
            product_exist_in_cart = find_inventory_staff_cart(email, 'detail')
            if product_exist_in_cart is None:
                break

            else:
                product_sku_lines = product_exist_in_cart.split('\n')
                for line in product_sku_lines:
                    if line.startswith('Product SKU: '):
                        actual_product_sku = line.split(': ')[1].strip()

                        if product_sku == actual_product_sku:
                            print(f'\n----- [System Message]: Product SKU: {product_sku} already exists in your cart')
                            print('\n====================================================================================================================')
                            log_message('WARNING', 'purchase_order_for_new_computers_spare_parts', email, f'Product ID: {product_sku} already exists in cart')

                            while True:
                                choice = input('\nWould you like to update / remove the products? (y/n): ').lower()

                                if choice == 'y':
                                    log_message('INFO', 'purchase_order_for_new_computers_spare_parts', email, 'User opted to update / remove products in cart')
                                    modify_purchase_order(email)
                                    return
                                
                                elif choice == 'n':
                                    log_message('INFO', 'purchase_order_for_new_computers_spare_parts', email, 'User opted to continue adding products')
                                    print('\n====================================================================================================================')
                                    purchase_order_for_new_computers_spare_parts(email)
                                    return
                                
                                else:
                                    log_message('ERROR', 'purchase_order_for_new_computers_spare_parts', email, 'Invalid input received')
                                    invalid_input()
                else:
                    break

    # Ask for product name
    while True:
        product_name = input("\nPlease enter product name: ")
        if product_name.lower() == 'x':
            log_message('INFO', 'purchase_order_for_new_computers_spare_parts', email, 'User exiting inventory staff add to cart to inventory management')
            inventory_management(email)
            return
        elif product_name == '' or product_name.isspace():
            log_message('ERROR', 'purchase_order_for_new_computers_spare_parts', email, 'Invalid input received')
            invalid_input()
        else:
            break
    
    # Ask for supplier name
    while True:
        supplier_name = input("\nPlease enter supplier name (e. g. Nvidia): ").upper()
        if supplier_name.lower() == 'x':
            log_message('INFO', 'purchase_order_for_new_computers_spare_parts', email, 'User exiting purchase order for new computers / spare parts to inventory management')
            inventory_management(email)
            return
        elif supplier_name == '' or supplier_name.isspace():
            log_message('ERROR', 'purchase_order_for_new_computers_spare_parts', email, 'Invalid input received')
            invalid_input()
        else:
            break
    
    # Ask for supplier contact number
    while True:
        supplier_phone = input("\nPlease enter supplier phone number (e.g. 601xxxxxxxx): ")
        if supplier_phone.lower() == 'x':
            log_message('INFO', 'purchase_order_for_new_computers_spare_parts', email, 'User exiting purchase order for new computers / spare parts to inventory management')
            inventory_management(email)
            return
        elif supplier_phone.isdigit() and (supplier_phone[:3] == '601') and (len(supplier_phone) >= 10):
            log_message('INFO', 'purchase_order_for_new_computers_spare_parts', email, 'User directing to inventory staff add to cart')
            break
        else:
            print('\n----- [System Message]: Please enter a valid phone number')
            print('\n====================================================================================================================')
            log_message('WARNING', 'purchase_order_for_new_computers_spare_parts', email, 'Invalid phone number entered')

    # Ask for desired product price
    while True:
        price = input("\nPlease enter the desired product price (e.g. 100): ")
        try:
            price = round(float(price),2)
            if price <= 0:
                print('\n----- [System Message]: Please enter a quantity greater than zero')
                print('\n====================================================================================================================')
                log_message('WARNING', 'purchase_order_for_new_computers_spare_parts', email, 'Entered quantity is not greater than zero')
                continue
            else:
                break
        except:
            print("\n----- [System Message]: Please enter a valid integer price. Without 'RM'")
            print('\n====================================================================================================================')
            log_message('ERROR', 'purchase_order_for_new_computers_spare_parts', email, 'Invalid input received')

    # Ask for product quantity
    while True:
        quantity = input("\nPlease enter requested product quantity: ")

        if quantity.isdigit():
            quantity = int(quantity)
            if quantity <= 0:
                print('\n----- [System Message]: Please enter a quantity greater than zero')
                print('\n====================================================================================================================')
                log_message('WARNING', 'purchase_order_for_new_computers_spare_parts', email, 'Entered quantity is not greater than zero')
                continue
            else:
                break
        else:
            print('\n----- [System Message]: Please enter a valid number')
            print('\n====================================================================================================================')
            log_message('ERROR', 'purchase_order_for_new_computers_spare_parts', email, 'Invalid input received')

    save_inventory_staff_cart(email, supplier_name, supplier_phone, product_name, product_sku, price, quantity) # Record into file

    while True: # Ask if user would like to add more products
        continue_adding = input('\nWould you like to continue adding product into your cart? (y/n): ').lower()
        print('\n====================================================================================================================')

        if continue_adding == 'y':
            log_message('INFO', 'inventory_staff_add_to_cart', email, 'User opted to continue adding products')
            purchase_order_for_new_computers_spare_parts(email)
            return
        
        elif continue_adding == 'n':
            log_message('INFO', 'inventory_staff_add_to_cart', email, 'User opted to finish and modify cart')
            modify_purchase_order(email)
            return
        
        else:
            log_message('ERROR', 'inventory_staff_add_to_cart', email, 'Invalid input received')
            invalid_input()


## Modify the cart
def modify_purchase_order(email):
    print('\n==========================================   MODIFY PURCHASE ORDER   ===============================================')
    # Get inventory staff's current cart details
    cart_details = find_inventory_staff_cart(email, 'detail')

    # Print the cart details
    print('\nInventory Staff\'s Cart:')    
    try:
        print('\n'+ cart_details)
        print('\n[1. Save Order]')
        print('[2. Update Quantity of a Product in Cart]')
        print('[3. Remove all Product in Cart]')
        print('[4. Remove a Product in Cart]')
        print('[X. Exit]')
        log_message('INFO', 'modify_purchase_order', email, 'Displayed cart details and options')

    except TypeError: # Nothing in the cart / Empty cart
        print('\nThere is nothing in your cart')
        log_message('WARNING', 'modify_purchase_order', email, 'Cart is empty')
        inventory_management(email)
        return
    
    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if choice == '1':
            log_message('INFO', 'modify_purchase_order', email, 'Submitting order')
            submit_order(email)
            return
        
        elif choice == '2':
            while True:
                print('\nEnter \'x\' to exit')
                product_sku = input('\nPlease enter the product SKU that you wish to edit: ').lower()
                if product_sku and product_sku != 'x':
                    # Make sure user input's product SKU is valid fully. Exp: only proceed if user enter TP001, won't proceed is user enter TP00
                    product_sku_lines = cart_details.split('\n')
                    for line in product_sku_lines:
                        if line.startswith('Product SKU: '):
                            actual_product_sku = line.split(': ')[1].strip()                            
                            if product_sku == actual_product_sku:
                                log_message('INFO', 'modify_purchase_order', email, f'Editing requested quantity for Product SKU: {product_sku}')
                                update_inventory_staff_cart(email, product_sku, 'update')
                                print('\n----- [System Message]: Action Successful')
                                print('\n====================================================================================================================')
                                modify_purchase_order(email)
                                return
                            
                    else:
                        log_message('WARNING', 'modify_purchase_order', email, f'Product SKU: {product_sku} is not in cart')
                        print(f'\n----- [System Message]: Product SKU: {product_sku} is not in your cart')
                        print('\n====================================================================================================================')

                if product_sku == 'x':
                    log_message('INFO', 'modify_purchase_order', email, 'Exiting to modify purchase order')
                    modify_purchase_order(email)
                    return
                
                elif not product_sku:                    
                    log_message('ERROR', 'modify_purchase_order', email, 'Invalid input received')
                    invalid_input() 

        elif choice == '3':
            while True:
                selection = input('\nAre you sure you want to remove all product(s) in your cart? (y/n): ').lower()
                if selection == 'y':
                    log_message('INFO', 'modify_purchase_order', email, 'Removing all products from cart')
                    update_inventory_staff_cart(email, None, 'all')
                    print('\n----- [System Message]: Action Successful')
                    print('\n====================================================================================================================')
                    modify_purchase_order(email)
                    return

                elif selection == 'n':
                    log_message('INFO', 'modify_purchase_order', email, 'Cancelled removal of all products from cart')
                    modify_purchase_order(email)
                    return
                
                else:
                    log_message('ERROR', 'modify_purchase_order', email, 'Invalid input received')
                    invalid_input()

        elif choice == '4':
            while True:
                print('\nEnter \'x\' to exit')
                product_sku = input('\nPlease enter the product SKU that you wish to remove: ').lower()
                    
                if product_sku and product_sku != 'x':
                    # Make sure user input's SKU is valid fully. Exp: only proceed if user enter TP001, won't proceed is user enter TP00
                    product_sku_lines = cart_details.split('\n')
                    for line in product_sku_lines:
                        if line.startswith('Product SKU: '):
                            actual_product_sku = line.split(': ')[1].strip()

                            if product_sku == actual_product_sku:
                                log_message('INFO', 'modify_purchase_order', email, f'Removing Product SKU: {product_sku} from cart')
                                update_inventory_staff_cart(email, product_sku, 'single')
                                print('\n----- [System Message]: Action Successful')
                                print('\n====================================================================================================================')
                                modify_purchase_order(email)
                                return
                            
                    else:
                        log_message('WARNING', 'modify_purchase_order', email, f'Product SKU: {product_sku} is not in cart')
                        print(f'\n----- [System Message]: Product SKU: {product_sku} is not in your cart ')
                        print('\n====================================================================================================================')

                if product_sku == 'x':
                    log_message('INFO', 'modify_purchase_order', email, 'Exiting to modify purchase order')
                    modify_purchase_order(email)
                    return

                elif not product_sku:
                    log_message('ERROR', 'modify_purchase_order', email, 'Invalid input received')
                    invalid_input()            
        
        elif choice == 'x':
            log_message('INFO', 'modify_purchase_order', email, 'Exiting modify order')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            inventory_management(email)
            return
        
        else:
            log_message('ERROR', 'modify_purchase_order', email, 'Invalid input received')
            invalid_input()
 

## Submit Restock or Add New Product's Order
def submit_order(email):    
    print('\n===============================================   SUBMIT ORDER   ===================================================')
    cart_details = find_inventory_staff_cart(email, 'detail')
    if cart_details:
        log_message('INFO', 'submit_order', email, 'Displayed cart details for submitting order')
        pass

    else:
        print('\nThere is nothing in your shopping cart')
        log_message('WARNING', 'submit_order', email, 'Cart is empty during submitting order process')
        inventory_management(email)
        return
    
    # Retrieve back user's name, phone number and address for shipping purpose
    address = display_user_details(email, 'for payment')

    # Display all the information
    print('\n====================================================================================================================')
    print('\nCheckout Product(s):')
    print(f'\n{cart_details}')
    print('\n----------------------------------------------------------------')
    print('\nShipping Details:')
    print(f'\n{address}')
    print('\n----------------------------------------------------------------')
    print('\nPayment Method (Default):')
    print(f'\nOnline Banking')
    print('\n----------------------------------------------------------------')
    print('\n====================================================================================================================')

    while True:
        choice = input('\nWould you like continue with this details? (y/n): ').lower()

        if choice == 'y':
            date = dt.now().strftime('%d %b %y %H:%M:%S')
            log_message('INFO', 'submit_order', email, 'Order submitted successfully')
            save_inventory_staff_order(email, address, date)
            return
        
        elif choice == 'n':
            log_message('INFO', 'submit_order', email, 'User cancelled the order submission process')
            inventory_management(email)
            return
        
        else:
            log_message('ERROR', 'submit_order', email, 'Invalid input received')
            invalid_input()   


## Check the Purchased Order Status
def check_purchase_order_status(email):
    print('\n====================================      CHECK PURCHASED ORDER STATUS      ========================================')
    print('\n[1. List all Order History]')
    print('[2. Search Order Status by Order ID]')
    print('[3. Cancel Order]')
    print('[X. Exit]')

    while True:
        choice = input('\nPlease select an option (e.g. 1): ').lower()
        print('\n====================================================================================================================')

        if choice == '1':
            log_message('INFO', 'check_purchase_order_status', email, 'User selected to list all order history')
            email_to_check = input('\nPlease enter the email that you would like to check the order belongs to or leave blank for all: ').lower() or None
            print('\n====================================================================================================================')
            find_inventory_staff_order(email, None, email_to_check, 'inventory management')
            return
        
        elif choice == '2':
            log_message('INFO', 'check_purchase_order_status', email, 'User selected to search order status by order id')
            while True:
                print('\nEnter \'x\' to exit')
                order_id = input('\nPlease enter the order ID: ').lower()
                print('\n====================================================================================================================')
                if order_id == 'x':
                    log_message('INFO', 'check_purchase_order_status', email, 'User cancelled the action')
                    check_purchase_order_status(email)
                    return
                
                else:
                    log_message('INFO', 'check_purchase_order_status', email, f'User searched for order ID: {order_id}')
                    find_inventory_staff_order(email, order_id, None, 'inventory management')
                    return
                
        elif choice == '3':
            log_message('INFO', 'check_purchase_order_status', email, 'User directing to cancel orders')
            cancel_purchase_order(email)
            return
        
        elif choice == 'x':
            log_message('INFO', 'check_purchase_order_status', email, 'User exiting inquiry of order status to inventory management')
            print('\nDirecting to previous page...')
            print('\n====================================================================================================================')
            inventory_management(email)
            return

        else:
            log_message('ERROR', 'check_purchase_order_status', email, 'Invalid input received')
            invalid_input()


## Cancel Orders
def cancel_purchase_order(email):
    print('\n==============================================   CANCEL ORDERS   ===================================================')

    while True:
        print('\nEnter \'x\' to exit')
        orderID = input('\nPlease enter the order ID that you would wish to cancel for: ').lower()

        if orderID == 'x':
            log_message('INFO', 'cancel_purchase_order', email, 'User exiting cancel purchase orders to inventory management')
            inventory_management(email)
            return
        
        elif not orderID or orderID.isspace() or not orderID.isdigit():
            log_message('INFO', 'cancel_purchase_order', email, 'Invalid input received')
            invalid_input()

        else:
            while True:
                choice = input("\nUnless the product is not available, all paid orders are non-refundable. Are you sure to cancel? (y/n): ").lower()

                if choice == 'y':
                    log_message('INFO', 'cancel_purchase_order', email, f'Cancelling order: {orderID}')

                    if not update_inventory_staff_order(email, orderID, 'cancelled', 'inventory management'):
                        log_message('INFO', 'cancel_purchase_order', email, f'Order id: {orderID} cancel unsuccessful')
                        print(f'\n----- [System Message]: No order with order ID: {orderID} found')
                        print('\n====================================================================================================================')
                        cancel_purchase_order(email)
                        return

                    else:
                        log_message('INFO', 'cancel_purchase_order', email, f'Order id: {orderID} cancel successful')
                        print(f"\n----- [System Message]: Order with order ID: {orderID} cancelled successful")
                        print('\n====================================================================================================================')
                        inventory_management(email)
                        return

                elif choice == 'n':
                    log_message('INFO', 'cancel_purchase_order', email, 'User exiting cancel purchase orders to inventory management')
                    inventory_management(email)
                    return
                
                else:
                    log_message('INFO', 'cancel_purchase_order', email, 'Invalid input received')
                    invalid_input()


## Reports for Inventory Management
def reports_for_inventory_management(email):
    print('\n=================================================   REPORTS   ======================================================')
    while True:
        print('\nEnter \'x\' to exit')
        needed_email = input('\nPlease enter the email that you would like the logs belongs to or leave blank for all: ').strip() or 'all inventory staff'

        if needed_email:
            if needed_email.lower() == 'x':
                log_message('INFO', 'reports_for_inventory_management', email, 'User exiting reports for inventory management to inventory management')
                inventory_management(email)
                return
            
            else:
                inventory_staff_list = display_user_details('inventory staff', 'for log')
                if (needed_email in inventory_staff_list) or needed_email == 'all inventory staff':
                    break
                else:
                    print(f'\n----- [System Message]: Email: {needed_email} is not exist or it is not belongs to inventory staff')
                    print('\n====================================================================================================================')
                    log_message('ERROR', 'reports_for_inventory_management', email, 'Invalid email entered')
                    continue
        
    level = input("\nPlease enter log level (INFO, WARNING, ERROR) or leave blank for all: ").strip() or None
    page = input("\nPlease enter page name (e.g. product adding) or leave blank for all: ").strip() or None
    start_time_str = input("\nPlease enter start date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:04:07) or leave blank for no start time: ").strip()
    end_time_str = input("\nPlease enter end date and time (DD MMM YY HH:MM:SS) (e.g. 04 AUG 24 14:05:07) or leave blank for no end time: ").strip()
    keyword = input("\nPlease enter keyword to search in messages or leave blank for no keyword: ").strip() or None
    print('\n====================================================================================================================')
    
    try:
        start_time = dt.strptime(start_time_str, "%d %b %y %H:%M:%S") if start_time_str else None
        end_time = dt.strptime(end_time_str, "%d %b %y %H:%M:%S") if end_time_str else None

    except ValueError or UnboundLocalError:
        log_message('ERROR', 'reports_for_inventory_management', email, 'Invalid date format entered')
        print('\n----- [System Message]: Invalid date format entered')
        reports_for_inventory_management(email)
        return

    except Exception as e:
        print(e)
        print('\n----- [System Message]: Please check again your date format entered')
        reports_for_inventory_management(email)
        return
    
    # Parse the log data
    parsed_logs = find_log_message(needed_email)

    # Apply filters
    filtered_logs = filtering_log(parsed_logs, level, page, start_time, end_time, keyword)

    if not filtered_logs:
        log_message('ERROR', 'reports_for_inventory_management', email, 'No matched result')
        print('\n----- [System Message]: No matched result. Please double check the data you entered')
        reports_for_inventory_management(email)
        return

    else:
        # Generate report
        log_message('INFO', 'reports_for_inventory_management', email, 'Report generated successful')
        report = generate_user_report(filtered_logs, needed_email)

    # Print the report
    print(report)
    inventory_management(email)
    return


####################################################################    DATA DISPLAY     ############################################################


#### Display Product Details
def display_product_details(definder, data, role, email):

    products = find_inventory(definder, data, role)

    if products:
        log_message('INFO', 'display_product_details', email, f'Found products for {definder}: {data}')
        print(f'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~   [{definder}: {data}]   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for i, product in enumerate(products):
            # Add the model of the devices for customer who request for service / repair at the end of the product name
            product_id = product[0]
            product_name = product[1]
            description = product[2]
            category = product[3]
            price = product[4]
            stock_status = product[5]
            manufacturer = product[6]
            total_amount_sold = product[7]
            date = product[8]

            print(f'\nProduct {i+1}:')
            print(f'\nProduct ID: {product_id}')
            print(f'Product Name: {product_name}')
            print(f'Description: {description}')
            print(f'Category: {category}')
            print(f'Price: RM {price}')
            print(f'Real-time Stock Status: {stock_status} unit(s)')
            print(f'Manufacturer: {manufacturer}')
            print(f'Total Amount Sold: {total_amount_sold} unit(s)')
            print(f'Last Update: {date}')
            print('\n====================================================================================================================')
        
        if role == 'customers' or role == 'customers from service':
            log_message('INFO', 'display_product_details', email, 'Navigating to add to cart')
            add_to_cart(email, role)
            return

        elif role == 'inventory staff':
            log_message('INFO', 'display_product_details', email, 'Navigating to stock check/adjustments')
            stock_check_adjustments(email)
            return
        
        elif role == 'inventory staff from product updating':
            log_message('INFO', 'display_product_details', email, 'Navigating to product updating')
            return [product_id, product_name, description, category, price, stock_status, manufacturer, total_amount_sold]
    
    else:
        if definder == 'listing all' and role == 'customers':
            log_message('INFO', 'display_product_details', email, 'No products in inventory')
            print('\n----- [System Message]: There is nothing in inventory')
            print('\n====================================================================================================================') 
            customer_menu(email)
            return
        
        elif definder == 'listing all' and role == 'inventory staff':
            log_message('INFO', 'display_product_details', email, 'No products in inventory')
            print('\n----- [System Message]: There is nothing in inventory')
            print('\n====================================================================================================================') 
            stock_check_adjustments(email)
            return
        
        else:
            log_message('WARNING', 'display_product_details', email, f'No products found for {definder}: {data}')
            print(f'\n----- [System Message]: {definder}: {data} is not exist')
            print('\n====================================================================================================================')  
            
            if role == 'customers' and definder == 'product id':
                log_message('INFO', 'display_product_details', email, 'Redirecting to search by ID')
                search_by_id(email)
                return
            
            elif role == 'customers' and definder == 'product name':
                log_message('INFO', 'display_product_details', email, 'Redirecting to search by name')
                search_by_name(email)
                return
            
            elif role == 'customers' and definder == 'category':
                log_message('INFO', 'display_product_details', email, 'Redirecting to search by category')
                search_by_category(email)
                return
            
            elif role == 'customers from service' and definder == 'product name':
                log_message('INFO', 'display_product_details', email, 'Redirecting to customer menu')
                customer_menu(email)
                return

            elif role == 'inventory staff':
                log_message('INFO', 'display_product_details', email, 'Redirecting to product checking')
                product_checking(email)
                return
            
            elif role == 'inventory staff from product updating':
                log_message('INFO', 'display_product_details', email, 'Redirecting to product updating')
                product_updating(email)
                return None


### Display order details
def display_order_details(order):
    order_id = order['order id']
    order_date = order['order date']
    order_email = order['order email']
    order_status = order['order status']
    
    print(f'\nOrder ID: {order_id}')
    print(f'Order Date: {order_date}')
    print(f'Order Email: {order_email}')
    print(f'Order Status: {order_status}')
    print('\n----------------------------------------------------------------')

    print('\nPurchased Products:')
    for product in order['purchased product(s)']:
        product_id = product['product id']
        product_name = product['product name']
        price = product['price']
        quantity = product['quantity']

        print(f'\n    Product ID: {product_id}')
        print(f'    Product Name: {product_name}')
        print(f'    Price: {price}')
        print(f'    Quantity: {quantity}')
        print('\n----------------------------------------------------------------')
        

    shipping_details = order['shipping details']
    receiver = shipping_details['receiver']
    contact_number = shipping_details['contact number']
    address_line_1 = shipping_details['address line 1']
    address_line_2 = shipping_details.get('address line 2', '')  # Handle missing optional field
    postal_code = shipping_details['postal code']
    city = shipping_details['city']
    state = shipping_details['state']

    print('\nShipping Details:')
    print(f'Receiver: {receiver}')
    print(f'Contact Number: {contact_number}')
    print(f'Address Line 1: {address_line_1}')
    print(f'Address Line 2: {address_line_2}')
    print(f'Postal Code: {postal_code}')
    print(f'City: {city}')
    print(f'State: {state}')
    print('\n====================================================================================================================')


# Display user's details
def display_user_details(identifier, requirement):
    with open(user_file, 'r') as file:
        if requirement == 'for payment':
            for line in file:
                if identifier in line:
                    elements = line.split(':::')
                    for element in elements:
                        key, value = element.split(': ')
                        if key == 'name':
                            name = value
                        elif key == 'phone':
                            phone = value
                        elif key == 'address 1':
                            address_1 = value
                        elif key == 'address 2':
                            address_2 = value
                        elif key == 'postal code':
                            postal_code = value
                        elif key == 'city':
                            city = value
                        elif key == 'state':
                            state = value

            complete_address = f'{name}\n{phone}\n{address_1}\n{address_2}\n{postal_code}\n{city}\n{state}'
            return complete_address
    
        elif requirement == 'for log':
            email_list = []
            for line in file:
                if identifier in line:
                    elements = line.split(':::')
                    for element in elements:
                        key, value = element.split(': ')
                        if key == 'email':
                            email = value
                            email_list.append(email)
            
            return email_list
        
        elif requirement is None:
            email_list = []
            for line in file:
                elements = line.split(':::')
                for element in elements:
                    key, value = element.split(': ')
                    if key == 'email':
                        email = value
                        email_list.append(email)
            
            return email_list
        
        elif requirement == 'status only':
            for line in file:
                if identifier in line:
                    elements = line.split(':::')
                    for element in elements:
                        key, value = element.split(': ')
                        if key == 'status':
                            status = value

            return status


### Display Inventory Staff's order details
def display_inventory_staff_order_details(order):
    order_id = order['order id']
    order_date = order['order date']
    order_email = order['order email']
    order_status = order['order status']
    payment_method = order['payment method']
    
    print(f'\nOrder ID: {order_id}')
    print(f'Order Date: {order_date}')
    print(f'Order Email: {order_email}')
    print(f'Order Status: {order_status}')
    print(f'Payment Method: {payment_method}')
    print('\n----------------------------------------------------------------')

    print('\nPurchased Products:')
    for product in order['purchased product(s)']:
        product_sku = product['product sku']
        product_name = product['product name']
        desired_price = product['desired price']
        requested_quantity = product['requested quantity']
        supplier_name = product['supplier name']
        supplier_contact = product['supplier contact number']

        print(f'\n    Product SKU: {product_sku}')
        print(f'    Product Name: {product_name}')
        print(f'    Desired Price: {desired_price}')
        print(f'    Requested Quantity: {requested_quantity}')
        print(f'    Supplier Name: {supplier_name}')
        print(f'    Supplier Contact Number: {supplier_contact}')
        print('\n----------------------------------------------------------------')
        

    shipping_details = order['shipping details']
    receiver = shipping_details['receiver']
    contact_number = shipping_details['contact number']
    address_line_1 = shipping_details['address line 1']
    address_line_2 = shipping_details.get('address line 2', '')  # Handle missing optional field
    postal_code = shipping_details['postal code']
    city = shipping_details['city']
    state = shipping_details['state']

    print('\nShipping Details:')
    print(f'Receiver: {receiver}')
    print(f'Contact Number: {contact_number}')
    print(f'Address Line 1: {address_line_1}')
    print(f'Address Line 2: {address_line_2}')
    print(f'Postal Code: {postal_code}')
    print(f'City: {city}')
    print(f'State: {state}')
    print('\n====================================================================================================================')


#####################################################################    VALIDATION / CHECKING     #############################################################


# Check the email vaidity
def check_email_validity(email):
    # Basic checks for '@' and '.' presence
    if '@' not in email or '.' not in email or ' ' in email:
        print('\n----- [System Message]: Invalid email format: missing \'@\' or \'.\' or your email contain spacing')
        return False
    
    # Splitting the email into two parts: local part and domain part
    local_part, domain_part = email.split('@', 1)

    # Check if local part and domain part are not empty
    if not local_part or not domain_part:
        print('\n----- [System Message]: Local part or domain part is empty')
        return False
    
    # Check if domain part contains a dot and is not at the start or end
    if '.' not in domain_part or domain_part.startswith('.') or domain_part.endswith('.'):
        print('\n----- [System Message]: Incorrect domain structure')
        return False

    # Ensure that domain part has characters before and after the dot
    domain_name, domain_extension = domain_part.rsplit('.', 1)
    if not domain_name or not domain_extension:
        print('\n----- [System Message]: Missing domain name or extension')
        return False
    
    # Validation passed
    return True


# Check the password strength
def check_password_strength(password):
    # Check if password is at least 8 characters long
    if len(password) < 8:
        print("\n----- [System Message]: Password must be at least 8 characters long")
        print('\n====================================================================================================================')
        return False

    # Check if password contains both uppercase and lowercase characters
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "@#$%^&+="

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        print("\n----- [System Message]: Password must contain at least one uppercase letter")
        print('\n====================================================================================================================')
        return False
    if not has_lower:
        print("\n----- [System Message]: Password must contain at least one lowercase letter")
        print('\n====================================================================================================================')
        return False
    if not has_digit:
        print("\n----- [System Message]: Password must contain at least one number")
        print('\n====================================================================================================================')
        return False
    if not has_special:
        print("\n----- [System Message]: Password must contain at least one special character (@, #, $, %, ^, &, +, =)")
        print('\n====================================================================================================================')
        return False

    return True


# Check the validity of the card number
def is_valid_card_number(card_num):
    # Implementing the Luhn Algorithm to validate the card number
    def luhn_check(num):
        total = 0
        reverse_digits = num[::-1]
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:  # Every second digit from the right
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0

    # Card number must be 16 digits and pass the Luhn check
    return card_num.isdigit() and len(card_num) == 16 and luhn_check(card_num)


# Check the validity of the card expiry date
def is_valid_expiry_date(expiry_date):
    if len(expiry_date) != 5 or expiry_date[2] != '/':
        print('\n----- [System Message]: Invalid expiry date format. Please use MM/YY')
        return False
    
    month, year = expiry_date.split('/')
    if not (month.isdigit() and year.isdigit()):
        print('\n----- [System Message]: Invalid expiry date format. Please use MM/YY')
        return False
    
    month = int(month)
    year = int(year) + 2000  # Assuming the year is provided as two digits (YY), for 20YY.
    if not 1 <= month <= 12:
        print('\n----- [System Message]: Invalid expiry date format. Please use MM/YY')
        return False

    # Get the current date
    current_date = dt.now()
    current_year = current_date.year
    current_month = current_date.month

    # Check if the expiry date is in the future
    if year < current_year or (year == current_year and month < current_month):
        print('\n----- [System Message]: The card has expired')
        return False

    return True


# Check the validity of the card cvv
def is_valid_cvv(cvv):
    return cvv.isdigit() and len(cvv) in [3, 4]


# Check if there is symbol or number exist in user input
def is_symbol(char):
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")
    return char not in allowed_characters # Return true if user input contain symbol


#####################################################################    FILE HANDLING     #############################################################


# Check if super user data in user.txt, if not, will save it
def check_super_user_details(super_user_email):
    super_user_password_after_hashing = hashing(super_user_password)
    super_user_details_found = False
    try:
        with open(user_file, 'r') as file:
            for line in file:
                if super_user_email in line:
                    super_user_details_found = True
                    break # If there is already the details fo super user exist in user.txt, quit this fuction
                else:
                    super_user_details_found = False
            
            if super_user_details_found:
                return
            else:
                # If there is no details of super user in user.txt, quit this loop and append the details
                with open(user_file, 'a') as file:
                    super_user_details = ':::'.join(f'{key}: {value}' for key, value in zip(
                        ['email', 'password', 'name', 'ic', 'phone', 'address 1', 'address 2', 'postal code', 'city', 'state', 'register date', 'status'],
                        [super_user_email, super_user_password_after_hashing, 'Super User', '100182766537', '0136728271', 'ASIA PACIFIC UNIVERSITY', 'JALAN TEKNOLOGI 5, TAMAN TEKNOLOGI MALAYSIA', '57000', 'KUALA LUMPUR', 'KUALA LUMPUR', '01 Aug 24 00:00:00', 'super user']))
                    file.write(super_user_details + '\n')



    except FileNotFoundError: # If there is no details of super user in user.txt append the details
        with open(user_file, 'a') as file:
            super_user_details = ':::'.join(f'{key}: {value}' for key, value in zip(
                ['email', 'password', 'name', 'ic', 'phone', 'address 1', 'address 2', 'postal code', 'city', 'state', 'register date', 'status'],
                [super_user_email, super_user_password_after_hashing, 'Super User', '100182766537', '0136728271', 'ASIA PACIFIC UNIVERSITY', 'JALAN TEKNOLOGI 5, TAMAN TEKNOLOGI MALAYSIA', '57000', 'KUALA LUMPUR', 'KUALA LUMPUR', '01 Aug 24 00:00:00', 'super user']))
            file.write(super_user_details + '\n')


# Saving Data into user.txt
def save_user_details(new_users):
    with open(user_file, 'a') as file:
        for user in new_users:
            user_details = ':::'.join(f'{key}: {value}' for key, value in zip(
                ['email', 'password', 'name', 'ic', 'phone', 'address 1', 'address 2', 'postal code', 'city', 'state', 'register date', 'status'], user
                ))
            file.write(user_details + '\n')


# Finding Data in user.txt
def find_user_email(email):
    users = []
    found_email = False
    try:
        with open(user_file, 'r') as file:
            for line in file:
                elements = line.strip().split(':::')

                for element in elements:
                    key, value = element.split(': ')
                    if key == 'email' and value == email:
                        found_email = True
                        break

                if found_email:
                    for element in elements:
                        key, value = element.split(': ')
                        users.append(value.strip())
                    return users
                
    except FileNotFoundError:
        pass

    return None


# Updating Data in user.txt
def update_user_details(email, new_data):
    with open(user_file, 'r') as file:
        needed_line = []
        for lines in file:
            elements = lines.strip().split(':::')
            for element in elements:
                key, value = element.strip().split(': ')
                if key == 'email':
                    if value != email:
                        needed_line.append(lines)

    with open(user_file, 'w') as file:
        file.writelines(needed_line)
        
    with open(user_file, 'a') as file:
        for data in new_data:
            user_details = ':::'.join(f'{key}: {value}' for key, value in zip(
                ['email', 'password', 'name', 'ic', 'phone', 'address 1', 'address 2', 'postal code', 'city', 'state', 'register date', 'status'], data
                ))
            file.write(user_details + '\n')


# Saving Data into customer_cart.txt
def save_cart(purchase_quantity, product, product_id, price, email):

    # Get current date
    date = dt.now().strftime('%d %b %y %H:%M:%S')
    
    with open(customer_cart_file, 'a') as file:
        cart_details = ':::'.join(f'{key}: {value}' for key, value in zip(
            ['email', 'product', 'product id', 'price', 'purchase quantity', 'last update'], [email, product, product_id, price, purchase_quantity, date]
        ))        
        file.write(cart_details+'\n')


# Finding Data in customer_cart.txt
def find_cart(email, requirement):
    total_price = 0
    total_quantity = 0
    cart_lines = []

    try:
        with open(customer_cart_file, 'r') as file:
            for line in file:
                elements = line.strip().split(':::')
                customer_email = None
                price = 0
                quantity = 0
                product_name = None

                for element in elements:
                    key, value = element.split(': ')
                    if key == 'email':
                        customer_email = value
                    elif key == 'product id':
                        product_id = value
                    elif key == 'product':
                        product_name = value
                    elif key == 'price':
                        price = float(value.strip())
                    elif key == 'purchase quantity':
                        quantity = int(value.strip())
                    elif key == 'last update':
                        last_update = value

                if customer_email == email:
                    total_price += price * quantity
                    total_quantity += quantity

                    if requirement == 'detail':
                        cart_lines.append(f'Product ID: {product_id}\nProduct Name: {product_name}\nPrice: RM {price:.2f} each\nQuantity: {quantity}\nLast Update: {last_update}\n')

                    elif requirement == 'one by one':
                        cart_lines.append([product_id, product_name, f'{price:.2f}', str(quantity)])

            if total_quantity == 0:
                return None

            if requirement == 'simple':
                return f'Total products in cart: {total_quantity}\nTotal price: RM {total_price:.2f}'
            
            elif requirement == 'detail':
                cart_summary = '\n'.join(cart_lines)
                cart_summary += f'\n----------------------------------------------------------------\n\nTotal products in cart: {total_quantity}'
                cart_summary += f'\nTotal price: RM {total_price:.2f}'
                return cart_summary
            
            elif requirement == 'one by one':
                return cart_lines

    except FileNotFoundError:
        pass

    return None


# Updating Data in customer_cart.txt
def remove_product_from_cart(email, product_id, requirement):
    try:
        with open(customer_cart_file, 'r') as file:
            lines = file.readlines()

        if requirement == 'all':
            # Remove all lines containing the customer's email
            needed_lines = [line for line in lines if email not in line]

        elif requirement == 'single':
            # Remove the line containing both email and product_id
            needed_lines = [line for line in lines if not (email in line and product_id in line)]

        if requirement != 'update':
            with open(customer_cart_file, 'w') as file:
                file.writelines(needed_lines)

        elif requirement == 'update':
            while True:
                quantity = input('\nWhat quantity would you like to set: ')

                if quantity.lower() == 'x':
                    modify_purchase_service_repair_order(email)
                    return
                
                else:
                    try:
                        quantity = int(quantity)
                        product_details = find_inventory('product id', product_id, None)
                        for product_detail in product_details:
                            stock_available = int(product_detail[5])
                            break

                        if quantity <= 0:
                            log_message('WARNING', 'remove_product_from_cart', email, 'Entered quantity is not greater than zero')
                            print('\n----- [System Message]: Please enter a quantity greater than zero')
                            print('\n====================================================================================================================')
                            continue

                        elif quantity > stock_available:
                            log_message('WARNING', 'remove_product_from_cart', email, 'Entered quantity is greater than quantity available in inventory')
                            print(f'\n----- [System Message]: We have only {stock_available} unit(s) available in stock. Please enter a smaller quantity')
                            print('\n====================================================================================================================')
                            continue

                        else:
                            break

                    except ValueError:
                        log_message('WARNING', 'remove_product_from_cart', email, 'Entered quantity is not a valid number')
                        print('\n----- [System Message]: Please enter a valid number')
                        print('\n====================================================================================================================')

            # Remove the line containing the specific email and product_id for update
            needed_lines = [line for line in lines if not (email in line and product_id in line)]

            # Write the updated lines back to the file
            with open(customer_cart_file, 'w') as file:
                file.writelines(needed_lines)

            # Update the specific line with new quantity and timestamp
            for line in lines:
                if email in line and product_id in line:
                    elements = line.strip().split(':::')
                    date = dt.now().strftime('%d %b %y %H:%M:%S')
                    elements[4] = f'purchase quantity: {quantity}'
                    elements[5] = f'last update: {date}'
                    updated_line = ':::'.join(elements)
                    
                    with open(customer_cart_file, 'a') as file:
                        file.write(updated_line + '\n')
        
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
    
    return None


# Saving Data into order.json
def save_order(email, address, date):
    # Initialize the items list
    items = [] # Used to store the product(s) that purchased by customer
    product_id_list = [] # Used to update the product in inventory after customer purchased the product

    # Get customer cart items
    cart = find_cart(email, 'one by one')
    definder = 'update after purchase'
    for line in cart:
        product_id = line[0]
        product_name = line[1]
        price = line[2]
        quantity = line[3]

        product_id_list.append([product_id, quantity, definder])

        item = {
            'product id': product_id,
            'product name': product_name,
            'price': price,
            'quantity': quantity
        }

        # Append the dictionary of the first item in the cart
        items.append(item)

    # Get customer address
    address_parts = str(address).split('\n')
    name = address_parts[0]
    phone_num = address_parts[1]
    address_1 = address_parts[2]
    address_2 = address_parts[3]
    postal = address_parts[4]
    city = address_parts[5]
    state = address_parts[6]

    shipping_details = {
        'receiver': name,
        'contact number': phone_num,
        'address line 1': address_1,
        'address line 2': address_2,
        'postal code': postal,
        'city': city,
        'state': state
    }

    # Load existing orders from the file or create a new file if the file doesn't exist
    try:
        with open(customer_order_file, 'r') as file:
            existing_orders = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        existing_orders = []

    # Determine the new order ID
    if existing_orders:
        last_order_id = existing_orders[-1]
        order_id = last_order_id['order id'] + 1

    else:
        order_id = 1

    status = 'pending'

    order = {
        'order id': order_id,
        'order date': date,
        'order email': email,
        'order status': status,
        'purchased product(s)': items,
        'shipping details': shipping_details
    }

    # Add the new order to the list of existing orders
    existing_orders.append(order)

    # Write the updated orders to the JSON file
    with open(customer_order_file, 'w') as file:
        json.dump(existing_orders, file, indent=4)

    remove_product_from_cart(email, None, 'all') # Remove all product from cart after checking out all the product in cart
    update_inventory(product_id_list) # Update the quantity of the product in inventory after user has complete the payment
    log_message('INFO', 'save_order', email, f'Order placed successfully. Order ID: {order_id}')
    print(f'\n----- [System Message]: Order Placed. Order ID: {order_id}')
    print('\n====================================================================================================================')
    inquiry_of_order_status(email)
    return


# Finding Data in order.json
def find_order(searching_email, order_id, email, from_page):
    try:
        with open(customer_order_file, 'r') as file:
            orders = json.load(file)

            found = False  # To track if any matching orders are found

            for order in orders:
                if searching_email is not None:
                    # Skip orders that don't match the provided email
                    if order['order email'] != searching_email:
                        continue
                    
                    # If order_id is None, list all orders / otherwise, match specific order ID
                    if order_id is None or str(order['order id']) == order_id:
                        found = True                    
                        log_message('INFO', 'find_order', email, 'Order found')
                        display_order_details(order)

                elif searching_email is None and str(order['order id']) == order_id:
                    found = True                    
                    log_message('INFO', 'find_order', email, f'Order ID: {order_id} found')
                    display_order_details(order)
            
            # Handle cases where no matching orders were found
            if not found:
                if order_id is None or searching_email is None:
                    log_message('WARNING', 'find_order', email, 'Order not found')
                    print(f'\n----- [System Message]: No orders found')
                else:
                    log_message('WARNING', 'find_order', email, 'Order not found')
                    print(f'\n----- [System Message]: No order with order ID: {order_id} found for {searching_email}')
                print('\n====================================================================================================================')

    except FileNotFoundError:
        print(f'\n----- [System Message]: No orders found for {searching_email}')
    except json.JSONDecodeError:
        print(f'\n----- [System Message]: No orders found')
    except KeyError as e:
        print(f'\nError: Missing expected data field: {e}')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
    
    # Return bacnk to the page where the user from
    if from_page == 'user management':
        order_checker(email)
        return
    else: # If from_page == 'customer management'
        inquiry_of_order_status(email)
        return


# Update Data in order.json
def update_order(email, order_id, status, from_page):
    try:
        with open(customer_order_file, 'r') as file:
            orders = json.load(file)
        
        # Initialize a flag to check if order is found
        order_found = False
        
        # Iterate through the orders and update the status of the matching order
        for order in orders:
            if from_page == 'user management':
                if order['order id'] == int(order_id):
                    order['order status'] = status
                    order_found = True
                    break

            else: # If from_page != user management
                if order['order id'] == int(order_id) and order['order email'] == email and order['order status'] == 'pending':
                    order['order status'] = status
                    order_found = True
                    break
                elif order['order id'] == int(order_id) and order['order email'] == email and order['order status'] != 'pending':
                    log_message('INFO', 'cancel_orders', email, f'Order id: {order_id} cancel unsuccessful')
                    print(f"\n----- [System Message]: You are unable to cancel this order as it might already have been cancelled or shipped out")
                    customer_cancel_orders(email)
                    return
        
        if order_found:
            # Write the updated list back to the JSON file
            with open(customer_order_file, 'w') as file:
                json.dump(orders, file, indent=4)
            return True
        else:
            return False        

    except FileNotFoundError:
        print(f'\n----- [System Message]: No orders found for {email}')
    
    except json.JSONDecodeError:
        print(f'\n----- [System Message]: No orders found')
        
    except KeyError as e:
        print(f'Error: Missing expected data field: {e}')
        
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        

    if from_page == 'user management':
        modify_order_status(email)
        return
    else: # if from_page == 'inventory management
        customer_menu(email)
        return


# Saving Data into inventory.txt
def save_inventory(email, new_product, productID, productName):
    with open(inventory_file, 'a') as file:
        for product in new_product:
            product_details = ':::'.join(f'{key}: {value}' for key, value in zip(
                ['product id', 'product name', 'description', 'category', 'price', 'real-time stock status', 'manufacturer', 'total amount sold', 'last update'], product
                ))
            file.write(product_details + '\n')
    
    print(f'\n----- [System Message]: {productName} with ID: {productID} registered successfully')
    print('\n====================================================================================================================')

    while True:
        continue_add_new_product = input('\nWould you like to cotinue adding new product? (y/n): ').lower()
        if continue_add_new_product == 'y':
            product_adding(email)
            return
        
        elif continue_add_new_product == 'n':
            stock_check_adjustments(email)
            return
        
        else:
            invalid_input()


# Finding Data in inventory.txt
def find_inventory(definer, data, role):
    inventories = []

    try:
        with open(inventory_file, 'r') as file:
            for lines in file:
                elements = lines.strip().split(':::')
                matched = False
                inventory = []

                for element in elements:
                    key, value = element.split(': ')

                    if role == 'customers': # If user is customer from product searching, will show result of inventory product only
                        if definer in ['product id', 'category']:
                            if (data in ['service', 'repair']) or str(data).startswith('sr'): # To Prevent search result of product finding showing repair and services
                                return None
                            else:
                                if key == definer and value.lower() == data:
                                    matched = True    

                        elif definer == 'listing all':
                            if key == 'product id' and 'tp' in value:
                                matched = True

                        else: # If definer is 'Product Name'
                            if key == definer and (('service' not in value.lower()) and ('repair' not in value.lower())) and data in value.lower(): # To Prevent search result of product finding showing repair and services
                                matched = True
                                
                        inventory.append(value.strip())
                    
                    elif role == 'customers from service': # If user is customer from service / repair, will show result of service / reapair only
                        if key == definer and value.lower() == data:
                            matched = True

                        inventory.append(value.strip())

                    elif role == 'inventory staff from product updating':
                        if key == definer and value.lower() == data:
                            matched = True

                        inventory.append(value.strip())

                    else: # If user is inventory staff, will show result of product and service / repair from inventory
                        if definer == 'product id':
                            if key == definer and value.lower() == data:
                                matched = True    

                        elif definer == 'listing all':
                            if key == 'product id' and 'tp' or 'sr' in value:
                                matched = True

                        inventory.append(value.strip())
                
                if matched:
                    inventories.append(inventory)

    except FileNotFoundError:
        pass

    return inventories if inventories else None


# Updating Data in inventory.txt
def update_inventory(product_id_list):
    for item in product_id_list:
        product_id = item[0]
        data = item[1]
        definder = item[2]

        try:
            # Read the existing inventory file
            with open(inventory_file, 'r') as file:
                lines = file.readlines()
                # Filter out the lines that do not contain the product ID
                needed_lines = [line for line in lines if product_id not in line]

                # Process each line to find and update the product information
                for line in lines:
                    if product_id in line:
                        date = dt.now().strftime('%d %b %y %H:%M:%S')
                        if definder == 'update after purchase':
                            stock_status = None # Initialize stock status
                            total_amount_sold = None # Initialize total amount sold

                            # Extract information from the line
                            elements = line.strip().split(':::')
                            for element in elements:
                                key, value = element.split(': ')
                                if key == 'real-time stock status':
                                    quantity = int(data)
                                    stock_status = int(value)
                                elif key == 'total amount sold':
                                    quantity = int(data)
                                    total_amount_sold = int(value)

                            # Update stock status and total amount sold
                            elements[5] = f'real-time stock status: {stock_status - quantity}'
                            elements[7] = f'total amount sold: {total_amount_sold + quantity}'
                            elements[8] = f'last update: {date}'
                            updated_line = ':::'.join(elements)

                            # Write the remaining lines without the updated product
                            with open(inventory_file, 'w') as file:
                                file.writelines(needed_lines)                       
                            
                            # Append the updated product information
                            with open(inventory_file, 'a') as file:
                                file.write(updated_line + '\n')

                        else:
                            elements = line.strip().split(':::')
                            for index, element in enumerate(elements):
                                key, value = element.split(': ')
                                if key == definder:
                                    elements[index] = f'{key}: {data}'
                                    elements[8] = f'last update: {date}'

                            # Update data of an product
                            updated_line = ':::'.join(elements)

                            # Write the remaining lines without the updated product
                            with open(inventory_file, 'w') as file:
                                file.writelines(needed_lines)                       
                            
                            # Append the updated product information
                            with open(inventory_file, 'a') as file:
                                file.write(updated_line + '\n')

                    else:
                        pass

        except FileNotFoundError:
            # Handle case where inventory file is not found
            print(f"Error: The file '{inventory_file}' was not found.")


# Saving Data into inventory_staff_cart.txt
def save_inventory_staff_cart(email, supplier_name, supplier_phone, product_name, product_sku, price, quantity):

    # Get current date
    date = dt.now().strftime('%d %b %y %H:%M:%S')
        
    with open(inventory_staff_cart_file, 'a') as file:
        cart_details = ':::'.join(f'{key}: {value}' for key, value in zip(
            ['email', 'supplier name', 'supplier phone', 'product name', 'product sku', 'desired price', 'requested quantity', 'last update'], [email, supplier_name, supplier_phone, product_name, product_sku, f'{price:.2f}', quantity, date]
        ))
        file.write(cart_details+'\n')


# Finding Data in inventory_staff_cart.txt
def find_inventory_staff_cart(email, requirement):
    total_price = 0
    total_quantity = 0
    cart_lines = []

    try:
        with open(inventory_staff_cart_file, 'r') as file:
            for line in file:
                elements = line.strip().split(':::')
                staff_email = None
                price = 0
                quantity = 0


                for element in elements:
                    key, value = element.split(': ')
                    if key == 'email':
                        staff_email = value
                    elif key == 'supplier name':
                        supplier_name = value
                    elif key == 'supplier phone':
                        supplier_phone = value
                    elif key == 'product name':
                        product_name = value
                    elif key == 'product sku':
                        product_sku = value
                    elif key == 'desired price':
                        price = float(value.strip()) # Changed to float because math operation needed to calculate total
                    elif key == 'requested quantity':
                        quantity = int(value.strip()) # Changed to float because math operation needed to calculate total
                    elif key == 'last update':
                        last_update = value
                
                if staff_email == email:
                    total_price += price * quantity
                    total_quantity += quantity

                    if requirement == 'detail':
                        cart_lines.append(f'Supplier Name: {supplier_name}\nSupplier Contact Number: {supplier_phone}\nProduct SKU: {product_sku}\nProduct Name: {product_name}\nDesired Price: RM {price:.2f} each\nRequested Quantity: {quantity}\nLast Update: {last_update}\n')
                    
                    elif requirement == 'one by one':
                        cart_lines.append([supplier_name, supplier_phone, product_name, product_sku,f'{price:.2f}', str(quantity)])

            if total_quantity == 0:
                return None
            
            if requirement == 'simple':
                return f'Total products in cart: {total_quantity}\nTotal price: RM {total_price:.2f}'
            
            elif requirement == 'detail':
                cart_summary = '\n'.join(cart_lines)
                cart_summary += f'\n----------------------------------------------------------------\n\nTotal products in cart: {total_quantity}'
                cart_summary += f'\nTotal price: RM {total_price:.2f}'
                return cart_summary
            
            elif requirement == 'one by one':
                return cart_lines

    except FileNotFoundError:
        pass

    return None


# Updating Data in inventory_staff_cart.txt
def update_inventory_staff_cart(email, product_sku, requirement):
    try:
        with open(inventory_staff_cart_file, 'r') as file:
            lines = file.readlines()

        if requirement == 'all':
            # Remove all lines containing the customer's email
            needed_lines = [line for line in lines if email not in line]

        elif requirement == 'single':
            # Remove the line containing both email and product_id
            needed_lines = [line for line in lines if not (email in line and product_sku in line)]

        if requirement != 'update':
            with open(inventory_staff_cart_file, 'w') as file:
                file.writelines(needed_lines)

        elif requirement == 'update':
            while True:
                quantity = input('\nWhat quantity would you like to set: ')

                if quantity.lower() == 'x':
                    modify_purchase_order(email)
                    return
                
                else:
                    try:
                        quantity = int(quantity)
                        if quantity <= 0:
                            log_message('WARNING', 'update_inventory_staff_cart', email, 'Entered quantity is not greater than zero')
                            print('\n----- [System Message]: Please enter a quantity greater than zero')
                            print('\n====================================================================================================================')
                            continue

                        else:
                            break

                    except ValueError:
                        log_message('WARNING', 'update_inventory_staff_cart', email, 'Entered quantity is not a valid number')
                        print('\n----- [System Message]: Please enter a valid number')
                        print('\n====================================================================================================================')

            # Remove the line containing the specific email and product_id for update
            needed_lines = [line for line in lines if not (email in line and product_sku in line)]

            # Write the updated lines back to the file
            with open(inventory_staff_cart_file, 'w') as file:
                file.writelines(needed_lines)

            # Update the specific line with new quantity and timestamp
            for line in lines:
                if email in line and product_sku in line:
                    elements = line.strip().split(':::')
                    date = dt.now().strftime('%d %b %y %H:%M:%S')
                    elements[-2] = f'requested quantity: {quantity}'
                    elements[-1] = f'last update: {date}'
                    updated_line = ':::'.join(elements)
                    
                    with open(inventory_staff_cart_file, 'a') as file:
                        file.write(updated_line + '\n')

    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
    
    return None


# Saving Data in inventory_staff_order.json
def save_inventory_staff_order(email, address, date):
    # Initialize the items list
    items = [] # Used to store the product(s) that purchased by inventory staff

    cart = find_inventory_staff_cart(email, 'one by one')
    for line in cart:
        product_sku = line[3]
        product_name = line[2]
        price = line[4]
        quantity = line[5]
        supplier_name = line[0]
        supplier_contact = line[1]

        item = {
            'product sku':product_sku,
            'product name': product_name,
            'desired price':price,
            'requested quantity': quantity,
            'supplier name': supplier_name,
            'supplier contact number': supplier_contact
        }

        items.append(item)

    address_parts = str(address).split('\n')
    name = address_parts[0]
    phone_num = address_parts[1]
    address_1 = address_parts[2]
    address_2 = address_parts[3]
    postal = address_parts[4]
    city = address_parts[5]
    state = address_parts[6]

    shipping_details = {
    'receiver': name,
    'contact number': phone_num,
    'address line 1': address_1,
    'address line 2': address_2,
    'postal code': postal,
    'city': city,
    'state': state
    }

    # Load existing orders from the file or create a new file if the file doesn't exist
    try:
        with open(inventory_staff_order_file, 'r') as file:
            existing_orders = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        existing_orders = []

    # Determine the new order ID
    if existing_orders:
        last_order_id = existing_orders[-1]
        order_id = last_order_id['order id'] + 1

    else:
        order_id = 1
    
    status = 'pending'

    order = {
        'order id': order_id,
        'order date': date,
        'order email': email,
        'order status': status,
        'payment method': 'Online Banking',
        'purchased product(s)': items,
        'shipping details': shipping_details
    }

    # Add the new order to the list of existing orders
    existing_orders.append(order)

    # Write the updated orders to the JSON file
    with open(inventory_staff_order_file, 'w') as file:
        json.dump(existing_orders, file, indent=4)

    update_inventory_staff_cart(email, None, 'all') # Remove all product from cart after checking out all the product in cart
    log_message('INFO', 'save_inventory_staff_order', email, f'Order placed successfully. Order ID: {order_id}')
    print(f'\n----- [System Message]: Order Placed. Order ID: {order_id}')
    print('\n====================================================================================================================')
    check_purchase_order_status(email)
    return


# Finding Data in inventory_staff_order.json
def find_inventory_staff_order(email, order_id, email_to_check, from_page):
    try:
        with open(inventory_staff_order_file, 'r') as file:
            orders = json.load(file)

            found = False  # To track if any matching orders are found

            for order in orders:

                if email_to_check is not None:
                    # If order_id is None, list all orders / otherwise, match specific order ID
                    if order['order email'] == email_to_check and order_id is None: # List all order for specific email
                        found = True                    
                        log_message('INFO', 'find_inventory_staff_order', email, f'Order found for {email_to_check}')
                        display_inventory_staff_order_details(order)
                    
                    # Skip orders that don't match the provided email
                    else:
                        continue

                if email_to_check is None and order_id is None: # List all order
                    found = True                    
                    log_message('INFO', 'find_inventory_staff_order', email, f'Order found for all inventory staff')
                    display_inventory_staff_order_details(order)

                if email_to_check is None and str(order['order id']) == order_id: # Display the order related to the order id
                    found = True                    
                    log_message('INFO', 'find_inventory_staff_order', email, f'Order ID: {order_id} found')
                    display_inventory_staff_order_details(order)
        
            # Handle cases where no matching orders were found
            if not found:
                if order_id is None:
                    log_message('WARNING', 'find_inventory_staff_order', email, f'Order not found')
                    print(f'\n----- [System Message]: No orders found for {email_to_check}')
                else:
                    log_message('WARNING', 'find_inventory_staff_order', email, f'Order not found for {email_to_check}')
                    print(f'\n----- [System Message]: No order with order ID: {order_id} found')
                print('\n====================================================================================================================')

    except FileNotFoundError:
        print(f'\n----- [System Message]: No orders found for {email_to_check}')
        
    except json.JSONDecodeError:
        print(f'\n----- [System Message]: No orders found')
        
    except KeyError as e:
        print(f'\nError: Missing expected data field: {e}')
        
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')

    # Return bacnk to the page where the user from
    if from_page == 'user management':
        order_checker(email)
        return
    else: # if from_page == 'inventory management
        check_purchase_order_status(email)
        return


# Update Data in inventory_staff_order.json
def update_inventory_staff_order(email, order_id, status, from_page):
    try:
        with open(inventory_staff_order_file, 'r') as file:
            orders = json.load(file)
        
        # Initialize a flag to check if order is found
        order_found = False
        
        # Iterate through the orders and update the status of the matching order
        for order in orders:
            if from_page == 'user management':
                if order['order id'] == int(order_id):
                    order['order status'] = status
                    order_found = True
                    break

            else: # If from_page != 'user management'
                if order['order id'] == int(order_id) and order['order status'] == 'pending':
                    order['order status'] = status
                    order_found = True
                    break

                elif order['order id'] == int(order_id) and order['order status'] != 'pending':
                    log_message('INFO', 'cancel_purchase_order', email, f'Order id: {order_id} cancel unsuccessful')
                    print(f"\n----- [System Message]: You are unable to cancel this order as it might already have been cancelled or shipped out")
                    cancel_purchase_order(email)
                    return
            
        if order_found:
            # Write the updated list back to the JSON file
            with open(inventory_staff_order_file, 'w') as file:
                json.dump(orders, file, indent=4)
            return True
        else:
            return False        

    except FileNotFoundError:
        print(f'\n----- [System Message]: No orders found')

    except json.JSONDecodeError:
        print(f'\n----- [System Message]: No orders found')

    except KeyError as e:
        print(f'Error: Missing expected data field: {e}')

    except Exception as e:
        print(f'An unexpected error occurred: {e}')
       

    if from_page == 'user management':
        modify_order_status(email)
        return
    else: # if from_page == 'inventory management
        inventory_management(email)
        return


# Saving Data into log.txt
def log_message(level, page, email, message):
    date = dt.now().strftime('%d %b %y %H:%M:%S')
    with open(log_file, 'a') as file:
        file.write(f'{date} | {level} | {page} | {email} | {message}\n')


# Finding Data in log.txt
def find_log_message(email):
    parsed_log = []

    with open(log_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            element = line.strip().split(' | ')
            
            # Parse the date and time
            date = element[0]
            timestamp = dt.strptime(date, "%d %b %y %H:%M:%S")

            # Parse the log level, page, user and message
            level = element[1]
            page = element[2]
            user = element[3]
            message = element[4]

            if email == 'all inventory staff':
                inventory_staff_list = display_user_details('inventory staff', 'for log')

                if user in inventory_staff_list:
                    parsed_log.append({
                            'timestamp': timestamp,
                            'level': level,
                            'page': page,
                            'user': user,
                            'message': message
                        })
                    
            elif email == 'all user':
                user_list = display_user_details(None, None)

                if user in user_list:
                    parsed_log.append({
                            'timestamp': timestamp,
                            'level': level,
                            'page': page,
                            'user': user,
                            'message': message
                        })

            else: # Used for customer reports
                if user == email:
                    parsed_log.append({
                        'timestamp': timestamp,
                        'level': level,
                        'page': page,
                        'user': user,
                        'message': message
                    })            

        return parsed_log


########################################################    GENERAL SHARING FUNCTIONS      ##############################################################


# Invalid Input Display
def invalid_input():
    print('\n----- [System Message]: Invalid input')
    print('\n====================================================================================================================')


# Hashing the Password for Security Purpose
def hashing(password):
    hash_value = len(password)
    for char in password:
        hash_value += ord(char) # The ord() function returns the number representing the unicode code of a specified character
        hash_value = (hash_value * ord(char)) % 982451653 # The 982451653 is a number to be modulus. The greater the number, the more the stronger hashing
    return str(hash_value)


### Filter Out the Related Log Lines
def filtering_log(parsed_logs, level, page, start_time, end_time, keyword):
    filtered_logs = parsed_logs

    if level:
        filtered_logs = [log for log in filtered_logs if log['level'] == level.upper()]

    if page:
        filtered_logs = [log for log in filtered_logs if log['page'] == page.replace(' ', '_').lower()]
    
    if start_time:
        filtered_logs = [log for log in filtered_logs if log['timestamp'] >= start_time]
    
    if end_time:
        filtered_logs = [log for log in filtered_logs if log['timestamp'] <= end_time]
    
    if keyword:
        filtered_logs = [log for log in filtered_logs if keyword.lower() in log['message'].lower()]
    
    if not filtered_logs:
        return False    
    return filtered_logs


### Adjusting the Logs in Readable Form
def generate_user_report(parsed_logs, email):
    report = "\n================================================   LOG REPORT   ====================================================\n\n"
    report += f"Report Generated: {dt.now().strftime('%d %b %y %H:%M:%S')}\n"
    report += f"Title: User Activity Report for [{email}]\n\n"

    report += "----------------------------------------------------------------------------------------------------------------------------------\n"
    report += "Timestamp            | Level    | Page                                          | Message\n"
    report += "----------------------------------------------------------------------------------------------------------------------------------\n"

    for log in parsed_logs:
        report += f"{log['timestamp'].strftime('%d %b %y %H:%M:%S'): <20} | {log['level']: <8} | {log['page']: <45} | {log['message']}\n"

    report += "----------------------------------------------------------------------------------------------------------------------------------\n"

    total_logs = len(parsed_logs)
    total_warnings = sum(1 for log in parsed_logs if log['level'] == 'WARNING')
    total_errors = sum(1 for log in parsed_logs if log['level'] == 'ERROR')
    total_infos = sum(1 for log in parsed_logs if log['level'] == 'INFO')

    report += f"\nSummary:\n"
    report += f"Total Logs: {total_logs}\n"
    report += f"Total Warnings: {total_warnings}\n"
    report += f"Total Errors: {total_errors}\n"
    report += f"Total Infos: {total_infos}\n\n"

    report += "----------------------------------------------------------------------------------------------------------------------------------\n"
    report += "\nEnd of Report"

    return report


## Settings
def settings(email, user_is):
    print('\n==================================================   SETTINGS   ====================================================')
    new_data = []
    new_details = []
    # Retrieve user data based on email
    old_data = find_user_email(email)
    definder = ['Email: ', 'Password (Hashed): ', 'Name: ', 'IC Number: ', 'Phone number: ', 'Address Line 1: ', 'Address Line 2: ', 'Postal Code: ', 'City: ', 'State: ', 'Register Date: ', 'Status: ']

    # Display current personal details
    print('\nCurrent personal details:\n') 
    for datum, element in zip(old_data, definder):
        new_details.append(datum)
        print(element + datum)

    print('\n----------------------------------------------------------------')
    print('\n[1. Change Password]')
    print('[2. Change Name]')
    print('[3. Change IC Number]')
    print('[4. Change Phone Number]')
    print('[5. Change Address Line 1]')
    print('[6. Change Address Line 2]')
    print('[7. Change Postal Code]')
    print('[8. Change City]')
    print('[9. Change State]')
    print('[X. Exit]')
    
    while True:
        choice = input('\nPlease select an option (e.g. 1): ').strip().lower()
        print('\n====================================================================================================================')
        print('\nEnter \'x\' to exit')

        if choice == '1':
            while True:
                log_message('INFO', 'settings', email, 'User changing password')
                password = input('\nPlease enter new password\nMinimum 8 characters long, contain special character, number and upper lower case): ')
                if password.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif not check_password_strength(password):
                    log_message('WARNING', 'settings', email, 'Password does not meet strength requirements')
                    continue
                else:
                    dc_password = input('\nPlease double confirm your password: ')
                    if dc_password.lower() == 'x':
                        log_message('INFO', 'settings', email, 'User reselect option')
                        settings(email, user_is)
                        return
                    elif password != dc_password:
                        print('\n----- [System Message]: Please check again your password. It is CASE SENSITIVE')
                        print('\n====================================================================================================================')
                        log_message('WARNING', 'settings', email, 'Double confirm password doesn\'t match with initial password')
                    else:
                        password = hashing(password)
                        new_details[1] = password
                        new_data.append(new_details)
                        update_user_details(email, new_data)
                        print('\n----- [System Message]: Password updated successfully')
                        log_message('INFO', 'settings', email, f'Password updated successfully from [{old_data[1]}] to [{new_details[1]}]')
                        settings(email, user_is)
                        return
            
        elif choice == '2':
            while True:
                log_message('INFO', 'settings', email, 'User changing name')
                name = input('\nPlease enter new name: ')
                if name.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif name == '' or name.isspace() or any(is_symbol(char) for char in name):
                    log_message('ERROR', 'settings', email, 'Invalid input received')
                    invalid_input()
                else:
                    new_details[2] = name
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: Name updated successfully')
                    log_message('INFO', 'settings', email, f'Name updated successfully from [{old_data[2]}] to [{new_details[2]}]')
                    settings(email, user_is)
                    return
            
        elif choice == '3':
            while True:
                log_message('INFO', 'settings', email, 'User changing IC number')
                ic = input('\nPlease enter new 12 digit IC number (without hyphens \'-\'): ')
                if ic.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif len(ic) == 12 and ic.isdigit():
                    new_details[3] = ic
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: IC number updated successfully')
                    log_message('INFO', 'settings', email, f'IC number updated successfully from [{old_data[3]}] to [{new_details[3]}]')
                    settings(email, user_is)
                    return
                else:
                    log_message('ERROR', 'settings', email, 'Invalid input received')
                    invalid_input()            
            
        elif choice == '4':
            while True:
                log_message('INFO', 'settings', email, 'User changing phone number')
                phone_num = input('\nEnter new phone number (e.g. 601xxxxxxxx): ')
                if phone_num.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif phone_num.isdigit() and (phone_num[:3] == '601') and (len(phone_num) >= 10):
                    new_details[4] = phone_num
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: Phone number updated successfully')
                    log_message('INFO', 'settings', email, f'Phone number updated successfully from [{old_data[4]}] to [{new_details[4]}]')
                    settings(email, user_is)
                    return
                else:
                    log_message('ERROR', 'settings', email, 'Invalid input received')
                    invalid_input()
                
        elif choice == '5':
            while True:
                log_message('INFO', 'settings', email, 'User changing address line 1')
                address_1 = input('\nEnter new address line 1: ').upper()
                if address_1.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif address_1 == '' or address_1.isspace():
                    log_message('ERROR', 'settings', email, 'Invalid input received')
                    invalid_input()
                else:
                    new_details[5] = address_1
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: Address line 1 updated successfully')
                    log_message('INFO', 'settings', email, f'Address line 1 updated successfully from [{old_data[5]}] to [{new_details[5]}]')
                    settings(email, user_is)
                    return
            
        elif choice == '6':
            while True:
                log_message('INFO', 'settings', email, 'User changing address line 2')
                address_2 = input('\nEnter new address line 2 (leave it blank if not needed): ').upper()
                if address_2.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif address_2 == '' or address_2.isspace():
                    address_2 = '-'
                    new_details[6] = address_2
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: Address line 2 updated successfully')
                    log_message('INFO', 'settings', email, f'Address line 2 updated successfully from [{old_data[6]}] to [{new_details[6]}]')
                    settings(email, user_is)
                    return
                else:
                    new_details[6] = address_2
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: Address line 2 updated successfully')
                    log_message('INFO', 'settings', email, f'Address line 2 updated successfully from [{old_data[6]}] to [{new_details[6]}]')
                    settings(email, user_is)
                    return
            
        elif choice == '7':
            while True:
                log_message('INFO', 'settings', email, 'User changing postal code')
                postal_code = input('\nEnter new postal code: ')
                if postal_code.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif len(postal_code) == 5 and postal_code.isdigit():
                    new_details[7] = postal_code
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: Postal code updated successfully')
                    log_message('INFO', 'settings', email, f'Postal code updated successfully from [{old_data[7]}] to [{new_details[7]}]')
                    settings(email, user_is)
                    return
                else:
                    log_message('ERROR', 'settings', email, 'Invalid input received')
                    invalid_input()
            
        elif choice == '8':
            while True:
                log_message('INFO', 'settings', email, 'User changing city')
                city = input('\nPlease enter new city: ').upper()
                if city.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif city == '' or city.isspace() or any(char.isdigit() for char in city):
                    log_message('ERROR', 'settings', email, 'Invalid input received')
                    invalid_input()
                else:
                    new_details[8] = city
                    new_data.append(new_details)
                    update_user_details(email, new_data)
                    print('\n----- [System Message]: City updated successfully')
                    log_message('INFO', 'settings', email, f'City updated successfully from [{old_data[8]}] to [{new_details[8]}]')
                    settings(email, user_is)
                    return
            
        elif choice == '9':
            while True:
                log_message('INFO', 'settings', email, 'User changing state')
                print('\n1. KUALA LUMPUR, 2. LABUAN, 3. PUTRAJAYA, 4. JOHOR, 5. KEDAH\n6. KELANTAN, 7. MELAKA, 8. NEGERI SEMBILAN, 9. PAHANG, 10. PULAU PINANG\n11. PERAK, 12. PERLIS, 13. SABAH, 14. SARAWAK, 15. SELANGOR, 16. TERENGGANU')
                state = input('\nPlease select new state (e.g. 1): ')
                if state.lower() == 'x':
                    log_message('INFO', 'settings', email, 'User reselect option')
                    settings(email, user_is)
                    return
                elif state == '1':
                    new_details[9] = 'KUALA LUMPUR'
                    break
                elif state == '2':
                    new_details[9] = 'LABUAN'
                    break
                elif state == '3':
                    new_details[9] = 'PUTRAJAYA'
                    break
                elif state == '4':
                    new_details[9] = 'JOHOR'
                    break
                elif state == '5':
                    new_details[9] = 'KEDAH'
                    break
                elif state == '6':
                    new_details[9] = 'KELANTAN'
                    break
                elif state == '7':
                    new_details[9] = 'MELAKA'
                    break
                elif state == '8':
                    new_details[9] = 'NEGERI SEMBILAN'
                    break
                elif state == '9':
                    new_details[9] = 'PAHANG'
                    break
                elif state == '10':
                    new_details[9] = 'PULAU PINANG'
                    break
                elif state == '11':
                    new_details[9] = 'PERAK'
                    break
                elif state == '12':
                    new_details[9] = 'PERLIS'
                    break
                elif state == '13':
                    new_details[9] = 'SABAH'
                    break
                elif state == '14':
                    new_details[9] = 'SARAWAK'
                    break
                elif state == '15':
                    new_details[9] = 'SELANGOR'
                    break
                elif state == '16':
                    new_details[9] = 'TERENGGANU'
                    break
                else:
                    log_message('ERROR', 'settings', email, 'Invalid input received')
                    invalid_input()

            new_data.append(new_details)
            update_user_details(email, new_data)
            print('\n----- [System Message]: State updated successfully')
            log_message('INFO', 'settings', email, f'State updated successfully from [{old_data[9]}] to [{new_details[9]}]')
            settings(email, user_is)
            return
            
        elif choice == 'x':
            if user_is == 'customers':
                log_message('INFO', 'settings', email, 'User exiting settings to customer menu')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                customer_menu(email)
                return
        
            elif user_is == 'inventory staff':
                log_message('INFO', 'settings', email, 'User exiting settings to inventory management')
                print('\nDirecting to previous page...')
                print('\n====================================================================================================================')
                inventory_management(email)
                return   
        
        else:
            log_message('ERROR', 'settings', email, 'Invalid input received')
            invalid_input()


main_menu(None)

