def my_function():
    print("All inputs are valid. Function called successfully!")

def get_valid_input(prompt, validation_func, error_message):
    while True:
        try:
            value = input(prompt)
            if validation_func(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print("Invalid input! Please try again.")

def main():
    while True:
        input1 = int(get_valid_input(
            "Enter the first number (1-100): ",
            lambda x: x.isdigit() and 1 <= int(x) <= 100,
            "The first input is invalid. Must be a number between 1 and 100."
        ))

        input2 = int(get_valid_input(
            "Enter the second number (1-600): ",
            lambda x: x.isdigit() and 1 <= int(x) <= 600,
            "The second input is invalid. Must be a number between 1 and 600."
        ))

        input3 = int(get_valid_input(
            "Enter the third number (0-10): ",
            lambda x: x.isdigit() and 0 <= int(x) <= 10,
            "The third input is invalid. Must be a number between 0 and 10."
        ))

        input4 = get_valid_input(
            "Enter the fourth input (must be 'OK'): ",
            lambda x: x.strip().upper() == "OK",
            "The fourth input is invalid. Must be 'OK'."
        )

        my_function()

if __name__ == "__main__":
    main()
