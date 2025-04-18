## Date: 2025-04-15
## Authors: Robot Group 1
## Description:  A program to manage finances at HAB Taxi Service


# Import libraries
import datetime
import os

# Constants
CUR_DATE = datetime.datetime.now()
ALPHA_NUM = ("1234567890 .-'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") # Characters allowed for validation

# Format date to YYYY-MM-DD
def getFormattedDate():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Open or create Defaults.dat 
def openDefaults():
    defaultValues = [143, 1922, 175.00, 60.00, 300.00, 0.15]
    if os.path.exists("Defaults.dat"):                        # Check if Default.dat exists
        try:
            with open("Defaults.dat", "r") as f:              # Open and read if exists
                parts = f.read().strip().split(",")          
                return (
                    int(parts[0].strip()),
                    int(parts[1].strip()),
                    float(parts[2].strip()),
                    float(parts[3].strip()),
                    float(parts[4].strip()),
                    float(parts[5].strip())
                )
        except:
            pass

    # Write default values to Default.dat
    with open("Defaults.dat", "w") as f: 
        f.write(", ".join(map(str, defaultValues)) + "\n")
    return defaultValues

# Open or create Revenue.dat 
def openRevenue():
    if os.path.exists("Revenue.dat"):  
        with open("Revenue.dat", "r") as f:
            lines = f.read().strip().split("\n")
            if lines and lines[-1] != "": 

                # Parse the last record in the file
                parts = lines[-1].split(",")
                if len(parts) == 7:
                    return (
                        int(parts[0].strip()),
                        datetime.datetime.strptime(parts[1].strip(), "%Y-%m-%d").date(),
                        parts[2].strip(),
                        int(parts[3].strip()),
                        float(parts[4].strip()),
                        float(parts[5].strip()),
                        float(parts[6].strip())
                    )

    # If Revenue.dat doesn't exist or is empty, create a default revenue record.
    transactionNum, driverNum, monthlyStandFee, dailyRentalFee, weeklyRentalFee, hstRate = openDefaults()
    transactionDate = CUR_DATE.date()
    revDescription = "Revenue description"
    transactionAmount = monthlyStandFee
    hst = round(hstRate * transactionAmount, 2)
    totalAmount = transactionAmount + hst

    # Write Revenue.dat with default values if file is empty
    with open("Revenue.dat", "w") as f:
        f.write(f"{transactionNum}, {transactionDate}, {revDescription}, {driverNum}, {transactionAmount}, {hst}, {totalAmount}\n")
    
    return transactionNum, transactionDate, revDescription, driverNum, transactionAmount, hst, totalAmount

# Load defaults from Defaults.dat
transactionNum, driverNum, monthlyStandFee, dailyRentalFee, weeklyRentalFee, hstRate = openDefaults()
revenue = openRevenue()

# Record monthly stand fee on 1st of month
if CUR_DATE.day == 1:

    # Get the current stand fee from Defaults.dat
    transactionNum, driverNum, monthlyStandFee, dailyRentalFee, weeklyRentalFee, hstRate = openDefaults()

    # Record the transaction in the revenue table
    transactionDate = CUR_DATE.date()
    revDescription = "Monthly Stand Fee"
    transactionAmount = monthlyStandFee
    hst = round(hstRate * transactionAmount, 2)
    totalAmount = transactionAmount + hst

    # Update Revenue.dat with the new transaction
    with open("Revenue.dat", "a") as f:
        f.write(f"{transactionNum}, {transactionDate}, {revDescription}, {driverNum}, {transactionAmount}, {hst}, {totalAmount}\n")

    # Update Defaults.dat with the new transaction number
    with open("Defaults.dat", "w") as f:
        f.write(f"{transactionNum + 1}, {driverNum}, {monthlyStandFee}, {dailyRentalFee}, {weeklyRentalFee}, {hstRate}\n")


    with open("Employees.dat", "r") as f_read:
        lines = f_read.readlines()

    with open("Employees.dat", "w") as f:
        for line in lines:
            parts = line.strip().split(", ")
            balanceDue = float(parts[9])  # Assuming the balance is the 10th value in the line
            updatedBalance = balanceDue + monthlyStandFee

            # Update the balance and write it back to the file
            parts[9] = str(updatedBalance)  # Update balance
            f.write(", ".join(parts) + "\n")

    # Increment transaction number for the next transaction
    transactionNum += 1
    print(f"\nStand fees successfully charged for {CUR_DATE.month}/{CUR_DATE.year}. Revenue and driver balances updated.")

# Menu Loop
while True:

    # Display menu options
    print("\n" + " " * 10 + "HAB Taxi Services")
    print(" " * 7 + "Company Services System\n")
    print("1. Enter a New Employee (driver).")
    print("2. Enter Company Revenues.")
    print("3. Enter Company Expenses.")
    print("4. Track Car Rentals.")
    print("5. Record Employee Payment.")
    print("6. Print Company Profit Listing.")
    print("7. Print Driver Financial Listing.")
    print("8. Quit Program.\n")

    # Input and validate choice #1-8
    while True:
        choice = input(" " * 12 + "Enter choice (1-8): ")
        if choice.isdigit() and 1 <= int(choice) <= 8:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
    
    # Option 1: Add a New Employee 
    if choice == "1":
        while True:
            # Input and validate driver name
            while True:
                name = input("Enter driver name: ").title()
                if name != "" and set(name).issubset(ALPHA_NUM):
                    break
                else:
                    print("Invalid Name. Please try again.")
            
            # Enter and validate driver address
            while True:
                address = input("Enter driver address: ").title()
                if address != "" and set(address).issubset(ALPHA_NUM):
                    break
                else:
                    print("Invalid Address. Please try again.")
                
            # Input and validate driver phone number
            while True:
                phone = input("Enter driver phone number (##########): ")
                if phone.isdigit() and len(phone) == 10:
                    break
                else:
                    print("Phone number must be 10 digits. Please try again.")

            # Input and validate driver license number
            while True:
                licenseNum = input("Enter driver license number: ")
                if licenseNum.isdigit():
                    break
                else:
                    print("Invalid License Number. Please try again.")
            
            # Input and validate driver license expiry date (YYY-MM-DD)
            while True:
                licenseExpiry = input("Enter license expiry date (YYYY-MM-DD): ")
                try:
                    licenseExpiryDate = datetime.datetime.strptime(licenseExpiry, "%Y-%m-%d").date()
                    if licenseExpiryDate >= CUR_DATE.date():
                        break
                    else:
                        print("License is expired. Please try again.")
                except:
                    print("Date must be in YYYY-MM-DD format. Please try again.")

            # Input and validate name of insurance company used by driver
            while True:
                insuranceCompany = input("Enter insurance company name: ").title()
                if insuranceCompany != "" and set(insuranceCompany).issubset(ALPHA_NUM):
                    break
                else:
                    print("Invalid insurance company. Please try again.")
            
            # Input and validate the insurance policy number
            while True:
                policyNum = input("Enter insurance policy number: ")
                if policyNum.isdigit():
                    break
                else:
                    print("Policy number must be numeric. Please try again.")
            
            # Input if driver uses own car (Y,N) and validate
            while True:
                ownCar = input("Does the driver own a car? (Y/N): ").upper()
                if ownCar in ["Y", "N"]:
                    break
                else:
                    print("Invalid input. Must be Y or N. Please try again.")

            # Increment driverNum for the new employee
            driverNum += 1
            with open("Employees.dat", "a") as f:
                f.write(f"{driverNum}, {name}, {address}, {phone}, {licenseNum}, {licenseExpiry}, {insuranceCompany}, {policyNum}, {ownCar}, 0.0\n")
            with open("Defaults.dat", "w") as f:
                f.write(f"{transactionNum}, {driverNum}, {monthlyStandFee}, {dailyRentalFee}, {weeklyRentalFee}, {hstRate}\n")
            print("\nEmployee successfully added!")
            
            # Break out of the inner loop to return to the menu
            break
        
    # Print message stating choice #2 is not programmed to function
    elif choice == "2":
        print("\nThe logic for choice #2 has yet to be implemented\n")
        continue

    # Print message stating choice #3 is not programmed to function
    elif choice == "3":
        print("\nThe logic for choice #3 has yet to be implemented\n")
        continue
    
    # Enter driver rental information for choice #4
    elif choice == "4":
        print("\n" + "-"*50)
        print("Track Car Rentals")
        print("-"*50)

        # Input Rental ID
        while True:
            rentalID = input("Enter Rental ID: ")
            if rentalID.isdigit():
                rentalID = int(rentalID)
                break
            else:
                print("Invalid Rental ID. Please enter a valid numeric Rental ID.")

        # Validate Driver Number
        while True:
            try:
                driverNumRental = int(input("Enter Driver Number: "))
                with open("Employees.dat", "r") as f:
                    existingDriverNums = [int(line.split(",")[0]) for line in f if line.strip()]
                if driverNumRental in existingDriverNums:
                    break
                else:
                    print("Driver number does not exist. Please try again.")
            except:
                print("Invalid input. Driver number must be numeric.")

        # Input and Validate Car Number
        while True:
            carNumber = input("Enter Car Number: ")
            if carNumber.isdigit() and carNumber != "":
                carNumber = int(carNumber)
                break
            else:
                print("Car number must be a numeric value. Please try again.")

        # Input and Validate Rental Type (Daily or Weekly)
        while True:
            rentalType = input("Enter rental type ('d' for Daily / 'w' for Weekly): ").lower()
            if rentalType in ['d', 'w']:
                break
            else:
                print("Invalid input. Please enter 'd' for Daily or 'w' for Weekly.")

        # Calculate Rental Rate based on Type
        rentalRate = dailyRentalFee if rentalType == 'd' else weeklyRentalFee

        # Input and Validate Rental Duration (days for daily, weeks for weekly)
        while True:
            try:
                if rentalType == 'd':
                    rentalDuration = int(input(f"Enter rental duration in days: "))
                else:
                    rentalDuration = int(input(f"Enter rental duration in weeks: "))
                if rentalDuration > 0:
                    break
                else:
                    print("Duration must be a positive integer. Please try again.")
            except:
                print("Invalid input. Please enter an integer.")

        # Calculate Total Rental Amount and HST (Tax)
        totalRentalAmount = rentalRate * rentalDuration
        totalHST = round(hstRate * totalRentalAmount, 2)
        totalAmount = totalRentalAmount + totalHST

        # Write Rental Details to Rentals.dat
        with open("Rentals.dat", "a") as f:
            f.write(f"{rentalID}, {driverNumRental}, {carNumber}, {getFormattedDate()}, {rentalType}, {rentalDuration}, {totalRentalAmount:.2f}, {totalHST:.2f}, {totalAmount:.2f}\n")

        # Display a confirmation message to the user
        print("\nRental information successfully recorded!")
        print("-"*50)
        print("\n")
        print(f"Rental ID: {rentalID}")
        print(f"Driver Number: {driverNumRental}")
        print(f"Car Number: {carNumber}")
        print(f"Driver Address: {address}")
        print(f"Rental Type: {'Daily' if rentalType == 'd' else 'Weekly'}")
        print(f"Rental Duration: {rentalDuration} {'day(s)' if rentalType == 'd' else 'week(s)'}")
        print("-"*50)
        print(f"Total Rental Amount: ${totalRentalAmount:.2f}")
        print(f"HST (tax): ${totalHST:.2f}")
        print(f"Total Amount Due: ${totalAmount:.2f}")
        print("-"*50)


    # Option 5: Record Employee Payment
    elif choice == "5":
        print("\n" + "-"*50)
        print("Record Employee Payment")
        print("-"*50)

        # Input Driver Number
        while True:
            try:
                driverNumPayment = int(input("Enter Driver Number to record the payment: "))
                with open("Employees.dat", "r") as f:
                    existingDriverNums = [int(line.split(",")[0]) for line in f if line.strip()]
                if driverNumPayment in existingDriverNums:
                    break
                else:
                    print("Driver number does not exist. Please try again.")
            except:
                print("Invalid input. Driver number must be numeric.")

        # Step 2: Input Payment Amount
        while True:
            try:
                paymentAmount = float(input(f"Enter payment amount for driver {driverNumPayment}: $"))
                if paymentAmount > 0:
                    break
                else:
                    print("Payment amount must be positive. Please try again.")
            except:
                print("Invalid input. Payment amount must be numeric.")

        # Adjust Driver's Balance
        updated_lines = []
        with open("Employees.dat", "r") as f:
            for line in f:
                parts = line.strip().split(", ")

                # Check if the current line matches the driver number
                if int(parts[0]) == driverNumPayment:
                    currentBalance = float(parts[9])  # Assuming balance is the 10th element
                    newBalance = currentBalance - paymentAmount  # Subtract payment
                    parts[9] = str(newBalance)  # Update the balance

                updated_lines.append(", ".join(parts))

        # Update the Employees.dat file with new balance
        with open("Employees.dat", "w") as f:
            f.write("\n".join(updated_lines) + "\n")

        # Record the payment in a log file (EmployeePayments.dat)
        paymentDate = getFormattedDate()  # Get the current date
        with open("EmployeePayments.dat", "a") as f:
            f.write(f"{driverNumPayment}, {paymentAmount}, {paymentDate}\n")

        # Display confirmation message
        print("\nPayment successfully recorded!")
        print("==============================")
        print("\n")
        print(f"Driver Number: {driverNumPayment}")
        print(f"Payment Amount: ${paymentAmount:.2f}")
        print(f"New Balance: ${newBalance:.2f}")
        print("-"*50)
        print("\n")

    # Option 6: Print Company Profit Listing
    elif choice == "6":
        print("\n" + "-"*30)
        print("Profit Listing Report \n\nDisplays Information About Company Costs and Expense  \n\nFor HAB TAXI Service")
        print("-"*30 +"\n")
        # Initialize total revenue and total expenses
        totalRevenue = 0
        totalExpenses = 0

        # Read Revenue.dat and calculate total revenue
        try:
            with open("Revenue.dat", "r") as revenue_file:
                for line in revenue_file:
                    parts = line.strip().split(", ")
                    totalRevenue += float(parts[6])  # Total amount is the 7th value (index 6)
        except:
            print("Revenue data file not found.")
        
        # Read Expenses.dat and calculate total expenses
        try:
            with open("Expenses.dat", "r") as expenses_file:
                for line in expenses_file:
                    parts = line.strip().split(", ")
                    totalExpenses += float(parts[3])  # Total amount is the 4th value (index 3)
        except:
            print("Expenses data file not found.")
        
        # Calculate profit
        profit = totalRevenue - totalExpenses
        
        # Display the profit report

        print(f"Total Revenue: ${totalRevenue:,.2f}")
        print(f"Total Expenses: ${totalExpenses:,.2f}")
        print(f"Company Profit: ${profit:,.2f}")
        print("-"*30)
   
   # Option 7: Print Driver Financial Listing
    elif choice == "7":
        print("\n" + "-"*63)
        print(" " * 15 + "Driver Financial Listing Report")
        print("-"*63)

        # Read Employees.dat and initialize financial data for each driver
        driverFinancialReport = {}
        
        try:
            with open("Employees.dat", "r") as empFile:
                for line in empFile:
                    parts = line.strip().split(", ")
                    driverNum = int(parts[0])  # Driver number (1st value)
                    driverName = parts[1]  # Driver name (2nd value)
                    balanceDue = float(parts[9])  # Balance due (10th value)

                    driverFinancialReport[driverNum] = {
                        'name': driverName,
                        'balance_due': balanceDue,
                        'total_payments': 0.0  # Initialize total payments to 0
                    }
        except:
            print("Employees data file not found.")

        # Read EmployeePayments.dat and calculate total payments for each driver
        try:
            with open("EmployeePayments.dat", "r") as payments_file:
                for line in payments_file:
                    parts = line.strip().split(", ")
                    driverNum = int(parts[0])  # Driver number (1st value)
                    paymentAmount = float(parts[1])  # Payment amount (2nd value)
                    
                    # Add the payment to the respective driver's total payments
                    if driverNum in driverFinancialReport:
                        driverFinancialReport[driverNum]['total_payments'] += paymentAmount
        except:
            print("EmployeePayments data file not found.")

        # Display the driver financial details in a tabular format
        print(f"{'Driver Number':<15} {'Driver Name':<15} {'Balance Due':<15} {'Total Payments':<15}")
        print("-" * 63)

        # Iterate through the financial data and print each driver's financial status
        for driverNum, financial_info in driverFinancialReport.items():
            final_balance_due = financial_info['balance_due'] - financial_info['total_payments']
            print(f"{driverNum:<15} {financial_info['name']:<15} ${financial_info['balance_due']:<15,.2f} ${financial_info['total_payments']:<15,.2f}")
        
        print("-"*63)

    elif choice == "8":
        print("Exiting Program")
        break
