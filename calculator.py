import re
import sys
import csv

def main():
    """
    Main part of the program.
    Takes the expresion as input,
    processes it using BODMAS rule
    and prints the output
    """
    print("""
Welcome to the math calculator
If you ever want to quit then please enter 'n' at any time when asked for an input
Your history is automatically saved. Please enter 'h' for viewing the history.""")
    history = []
    while True:
        expression = input('Enter the math expression: ').replace(" ","")
        if expression == 'h':
            show_history(history)
            continue
        org = check(expression)
        if org == 'n':
            save_to_file(history)
        else:
            result = evaluate_expression(org)
            print("Result:",result)
            history.append(f"{org} = {result}")
        

def evaluate_expression(exp):
    """
    Recursively processes the input expression.
    Uses the BODMAS rule and supports and evaluates in the order
    1. Parenthesis
    2. Exponentiation
    3. Division
    4. Multiplication
    5. Addition
    6. Subtraction
    """
    
    #Handles the parenthesis first using re module
    bracket = r"(\(.*?\))"
    if re.search(bracket,exp):
        matches = re.findall(bracket,exp)
        for match in matches:
            #Recursively solves all expressions in parenthesis first
            inner = match.strip("(").strip(")")
            exp = exp.replace(match, evaluate_expression(inner))
        return evaluate_expression(exp)
    
    #List the patterns for various operations
    patterns = [
        (r"(\-?\d*\.?\d+[\^]\-?\d*\.?\d+)", "exponential"),
        (r"(\-?\d*\.?\d+[/]\-?\d*\.?\d+)", "div"),
        (r"(\-?\d*\.?\d+[\*]\-?\d*\.?\d+)", "mult"),
        (r"(\-?\d*\.?\d+[\+\-]\-?\d*\.?\d+)", "addsub"),
    ]
    #Recursively applies the each pattern and processes the expression in the BODMAS order
    for pattern, op in patterns:
        if re.search(pattern,exp):
            if op == "exponential":
                match_positions = list(re.finditer(pattern,exp))
                needed_positions = list(reversed(match_positions))
                for position in needed_positions:
                    value = do_math(position.group())
                    exp = exp[:position.start()]+value+exp[position.end():]
                    return evaluate_expression(exp)
            else:
                matches = re.findall(pattern,exp)
                for match in matches:
                    exp = exp.replace(match,do_math(match),1)
                    return evaluate_expression(exp)
    return exp   #Final result

def do_math(num_and_operator):
    """
    Evaluates a simple binary operation and gives the result
    """
    if "^" in num_and_operator:
        a,b = map(float, num_and_operator.split("^"))
        return str(round(a**b,2))
    elif "*" in num_and_operator:
        a,b = map(float, num_and_operator.split("*"))
        return str(round(a*b,2))
    elif "/" in num_and_operator:
        a,b = map(float, num_and_operator.split("/"))
        return str(round(a/b,2))
    elif "+" in num_and_operator:
        a,b = map(float, num_and_operator.split("+"))
        return str(round(a+b,2))
    elif "-" in num_and_operator:
        a, b = re.split(r'(?<!^)-', num_and_operator, 1)
        return str(round(float(a) - float(b), 2))
    
def show_history(history_list):
  '''
  Displays the history
  '''
    for no, exp in enumerate(history_list, start = 1):
        print(f"{no}. {exp}")

def exit_program():
  '''
  Exits the program
  '''
    sys.exit("Thank you for using the calculator. Have a great day")

def check(given):
  '''
  Checks the expression for any problems in it
  '''
  
  #Checks whether the expression only contains the aloowed characters
    allowed = "1234567890.+-/*^()"
    while True:
        if given.strip().lower() == "n":
            return "n"
        if all(char in allowed for char in given):
            break
        else:
            given = input("Please enter a valid numerical expression or 'n' to exit: ").replace(" ", "")
          
    #Checks whether the parenthesis given is correct
    while True:
        if given.strip().lower() == "n":
            return 'n'
        if given.count("(") != given.count(")"):
            given = input(f"""
There seems to be a problem in the brackets you have entered
{given}
Please check and enter the correct expression: """).replace(" ","")
        else:
            break
    #Replaces all the uneccessary elements to simplify the expression
    given = given.replace('**',"^")
    given = given.replace("--","+")
    given = given.replace("+-", '-')
    given = given.replace('-+','-')
    given = given.replace("++","+")

    #Checks whether the expression has any unecessary chracters at the beginning or end
    while given.startswith(("*","/","^")):
        print("You can enter 'n' to exit")
        ask = input(f"There seems to be an unwanted {given[0]} at the start of the expression. Enter y if you want to remove it: ").strip().lower()
        if ask.strip().lower() == "n":
            return 'n'
        if ask == "y":
            given = given[1:]
            break
        else:
            continue
    while given.endswith(("*","/","^",'-','+')):
        print("You can enter 'n' to exit")
        ask = input(f"There seems to be an unwanted {given[-1]} at the end of the expression. Enter y if you wish to remove it: ").strip().lower()
        if ask.strip().lower() == "n":
            return 'n'
        if ask == "y":
            given = given[:-1]
            break
        else:
            continue

    #Checks whether there is any division by zero and askes the user to enter a replacement for it
    if re.search(r"(\-?\d*\.?\d+[/]\-?\d*\.?\d+)",given):
        matches = re.findall(r"(\-?\d*\.?\d+[/]\-?\d*\.?\d+)",given)
        for match in matches:
            a,b = match.split("/")
            while float(b) == 0:
                print("""
Sorry cannot perform division by zero
You can enter 'n' to exit""")
                ask = (input(f"Please enter a valid number to replace the zero in {match}. Enter the number to replace zero"))
                if ask.strip().lower() == "n":
                   return 'n'
                try:
                    b = float(ask)
                    if b == 0:
                        continue
                    break
                except ValueError:
                    continue
            given = given.replace(match,f"{a}/{str(b)}")
    return given

def save_to_file(source):
  '''
  Saves the history to a file whose name and format are specified by the user
  '''
  #Ask user for the file specifications
    file_name = input("Enter the name of the file you want your history to be stored in: ").strip()
    format_choice = input("Enter '1' for saving your history as a CSV file or '2' for saving it as a txt file: ").strip()
    while not format_choice in ["1","2"]:
        format_choice = input("Please enter '1' for saving as a .csv file and '2' for saving as a .txt file: ").strip()

    #Saves the history accordingly
    if format_choice == "1":
        with open(f"{file_name}.csv","w", newline = '') as file:
            history_file = csv.DictWriter(file, fieldnames = ["SL. no", "Expression and result"])
            history_file.writeheader()
            for no, entry in enumerate(source, start = 1):
                history_file.writerow(
                    {"SL. no" : no,
                     "Expression and result" : entry
                    }
                )
    elif format_choice == "2":
        with open(f"{file_name}.txt", "w") as file:
            for no, entry in enumerate(source, start=1):
                file.write(f"{no}. {entry}\n")
    exit_program()


if __name__ == "__main__":
    main()
