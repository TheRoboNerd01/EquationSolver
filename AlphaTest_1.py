# Created by Javier Romero Sanchez


#Gets the key fromthe Stage1, connects to that Socket, and proceeds to evaluate the ecuations.
def arithmetic(operation):

        operation= simpl_oper(operation) #Replaces [ and { for ( and also for the closing ones.
        print("The result is: "+str(calculator(operation))) #Evaluates the equation and transforms it into string.



#Replaces the [,] and {,}  with (,)
def simpl_oper(operation):
    operation = operation.replace('[', '(')
    operation = operation.replace(']', ')')
    operation = operation.replace('{', '(')
    operation = operation.replace('}', ')')
    print(operation)
    return operation


# Executes the received operation and returns its numerical value.
def calculator(operation):

    print(operation)
    numbers=[] #Saves all the numbers in the operation.
    ops=[] #Saves all the operations and brackets of the operation in execution order.
    i = 0 #Goes through all the characters of the operation.
    while i in range(0, len(operation)):
        #If the first char is a digit:
        if operation[i].isdigit():
            number = operation[i]
            i += 1
            #Checks if next char is a digit, because there might be numbers with more than 1 digit.
            while i < (len(operation)) and operation[i].isdigit():
                number = str(number) + str(operation[i])
                i += 1
            numbers.append(int(number)) #Adds the number to the number stack.
            continue

        elif operation[i] == '(':
            ops.append(operation[i])  # Adds the brackets to the ops stack.
        elif operation[i] == ')':  # If finds a closing bracket, goes through all the ops stack, until it finds a closing one
            if len(ops) > 0:
                while ops[-1] != '(':
                    print("Stays (")

                    print("Operations:")

                    print(ops)

                    numbers.append(app_arith(str(ops.pop()), numbers.pop(), numbers.pop()))

                    print("New values of number:")

                    print(numbers)

                    print("New values of ops:")

                    print(ops)

                if ops[-1] == '(':
                    ops.pop()

        elif operation[i] == '+' or operation[i] == '-' or operation[i] == '*' or operation[i] == '/' or operation[i] == '^':
            while len(ops) > 0 and check_pref(operation[i], ops[-1]):
                numbers.append(app_arith(str(ops.pop()), numbers.pop(), numbers.pop()))
            ops.append(operation[i])
        i += 1
    while len(ops) != 0:
        numbers.append(app_arith(str(ops.pop()), numbers.pop(), numbers.pop()))
    print(numbers,ops)
    return numbers.pop()


#Receives an operation sign and the second number and first number of the operation, calculating its result.
def app_arith(op, num2, num1):

    if op == '+':
        print("Addition.." + str(int(num1 + num2)))
        return int(num1 + num2)
    elif op == '-':
        print("Substraction..." + str(int(num1 - num2)))
        return int(num1 - num2)
    elif op == '/':
        print("Division.." + str(int(num1 / num2)))
        return int(num1 / num2)
    elif op == '*':
        print("Multiplication..." + str(int(num1 * num2)))
        return int(num1 * num2)
    elif op == '^':
        print("Power of..." + str(int(num1 ** num2)))
        return int(num1 ** num2)
    else:
        print("Operation not found.")
        return int(0)


#Checks the preference of the operands.
def check_pref(char1, char2):
    print(char1+", "+char2)
    if char2 == '(' or char2 == ')':
        return False
    elif char1 =='^' or char2 =='^':
        return False
    elif (char1 == '*' or char1 == '/') and (char2 == '+' or char2 == '-'):
        return False
    else:
        return True


#Insert as a method the equation to resolve.
arithmetic("4*5 -(2^3)")