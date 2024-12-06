# KLCCC-System

Introduction:
KL Central Computer Company (KLCCC) is a rapidly expanding computer sales and repair business located in Kuala Lumpur. To efficiently manage its growing volume of transactions and streamline its operations, KLCCC has decided to implement a comprehensive automated system. This system, developed in Python, is designed to handle the company's core functions across three distinct areas: Customer Management, User Management, and Inventory Management.

The software solution will facilitate various operations, including customer registration and login, order processing, user management, inventory control as well as data analysing and filtering for reporting purpose. Each functional area of the system will be managed by a separate developer to ensure specialized handling and ease of maintenance. 

Assumptions:
1.	User Types and Approval:
-	Super User: Root-in account in this KLCCC System with the highest level of access and control and no need to be approved by anyone before accessing the system.
-	Customers and Inventory Staff: Must register and be approved by admin or the Super User before accessing the system.
-	Admin: Must register and be approved by the Super User before accessing the system.

2.	Access Control:
-	Different user roles (customers, admin, inventory staff) have specific access rights and functionalities within the system.
-	Super User has overarching control and approval rights across all areas, including user management and inventory oversight.

3.	Functional Areas:
General function for all management:
-	Login function
-	Register function
-	Data analysing and filtering for reporting purpose function
  
Customer Management:
-	Product purchasing function
-	Requesting for service or repair function
-	Modifying customer’s cart function
-	Payment processing function
-	Order cancelling function
-	Settings function

User Management:
-	Adding new users
-	Verification of customers
-	Modification of user details
-	Disabling user access
-	System usage inquiries
-	Checking and modifying customer or inventory staff’s order status
  
Inventory Management:
-	Handles stock management
-	Purchase orders for new computers or spare parts
-	Inventory staff’s cart modification
-	Order submission to supplier
-	Order status checking
- Settings function

