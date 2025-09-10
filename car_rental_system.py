import mysql.connector        
import datetime


# MySQL Connection #
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',       # Change if your MySQL user is different
        password='',  # Update with your MySQL password
        database='car_rental'
    )


# Admin Functions #
def add_car():
    brand = input("Enter Car Brand: ")
    model = input("Enter Car Model: ")
    price = float(input("Enter Price per day: "))
    

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO cars (brand, model, price_per_day) VALUES (%s, %s, %s)", 
                   (brand, model, price))
    
    conn.commit()
    conn.close()

    print("Car added successfully!\n")

def view_all_cars():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()

    print("\n--- Available Cars ---")
    print("ID | Brand | Model | Price/Day | Status")
    print("-----------------------------------------")
    for car in cars:
        status = "Available" if car[4] else "Not Available"
        print(f"{car[0]} | {car[1]} | {car[2]} | Rs.{car[3]} | {status}")
    print()

def delete_car():
    car_id = int(input("Enter Car ID to delete: "))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE car_id = %s", (car_id,))
    conn.commit()
    conn.close()

    print("Car deleted successfully!\n")

# Customer Functions #
def view_available_cars():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE is_available = TRUE")
    cars = cursor.fetchall()
    conn.close()

    if not cars:
        print("No cars available right now.\n")
        return

    print("\n--- Available Cars ---")
    print("ID | Brand | Model | Price/Day")
    print("---------------------------------")
    for car in cars:
        print(f"{car[0]} | {car[1]} | {car[2]} | Rs.{car[3]}")
    print()

def rent_car():
    view_available_cars()
    car_id = int(input("Enter Car ID to rent: "))
    customer_name = input("Enter your name: ")
    days = int(input("Enter number of days to rent: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Check if car is available
    cursor.execute("SELECT price_per_day, is_available FROM cars WHERE car_id = %s", (car_id,))
    car = cursor.fetchone()

    if not car:
        print("Invalid Car ID!\n")
        conn.close()
        return
    if not car[1]:
        print("Car is not available!\n")
        conn.close()
        return

    price_per_day = car[0]
    total_cost = price_per_day * days
    rental_date = datetime.date.today()
    return_date = rental_date + datetime.timedelta(days=days)

    # Insert into rentals table
    cursor.execute("""
        INSERT INTO rentals (car_id, customer_name, days, total_cost, rental_date, return_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (car_id, customer_name, days, total_cost, rental_date, return_date))

    # Update car availability
    cursor.execute("UPDATE cars SET is_available = FALSE WHERE car_id = %s", (car_id,))

    conn.commit()
    conn.close()

    print(f"\nCar rented successfully to {customer_name}!")
    print(f"Total Cost: Rs.{total_cost}")
    print(f"Return Date: {return_date}\n")

def return_car():
    rental_id = int(input("Enter Rental ID to return: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Check rental record
    cursor.execute("SELECT car_id FROM rentals WHERE rental_id = %s", (rental_id,))
    rental = cursor.fetchone()

    if not rental:
        print("Invalid Rental ID!\n")
        conn.close()
        return

    car_id = rental[0]

    # Update car availability
    cursor.execute("UPDATE cars SET is_available = TRUE WHERE car_id = %s", (car_id,))
    conn.commit()
    conn.close()

    print("Car returned successfully!\n")

# Main Menu #
def main():
    while True:
        print("=== Car Rental System ===")
        print("1. Admin - Add Car")
        print("2. Admin - View All Cars")
        print("3. Admin - Delete Car")
        print("4. Customer - View Available Cars")
        print("5. Customer - Rent a Car")
        print("6. Customer - Return a Car")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_car()
        elif choice == "2":
            view_all_cars()
        elif choice == "3":
            delete_car()
        elif choice == "4":
            view_available_cars()
        elif choice == "5":
            rent_car()
        elif choice == "6":
            return_car()
        elif choice == "7":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")



if __name__ == "__main__":
    main()

