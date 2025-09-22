def add(x, y):
    """This function adds two numbers"""
    return x + y
def subtract(x, y):
    """This function subtracts two numbers"""
    return x - y
def multiply(x, y):
    """This function multiplies two numbers"""
    return x * y
def divide(x, y):
    """This function divides two numbers"""
    if y == 0:
        return "Error! Division by zero is not allowed."
    else:
        return x / y
def main():
    """Main function to run the calculator CLI"""
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    while True:
        # This will take input from the user
        choice = input("Enter choice(1 or 2 or 3 or 4): ")
        # It will check here 
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                continue 
              # It'll skip the rest of the loop and start over
            if choice == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"{num1} / {num2} = {result}")
            # Here it'll ask if the user wants to do another calculation or not 
            next_calculation = input("Let's do the next calculation? (yes or no): ")
            if next_calculation.lower() != 'yes':
                break 
              # Exits the loop if the answer is "no"
        else:
            print("Invalid input. Please select a valid operation (1 or 2 or 3 or 4).")           
if __name__ == "__main__":
    main()                       