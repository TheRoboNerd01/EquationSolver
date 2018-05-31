# Created by Javier Romero Sanchez

import socket
IP_DIRECTION = ""
SOCKET = 'atclab.esi.uclm.es'


#Collects the key for the Stage0
def get_key():
    #Stablishes the first connection with TCP to get the first key for the stage 1.
    print("Test....")
    socket0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket0.connect((SOCKET, 2000))
    messageget = (socket0.recv(1024))
    keyget=messageget[0:5]
    messageget=keyget.decode("utf-8")
    return messageget


#Gets the key from the Stage0, sends it to the server and receives another key.
def send_key():
    socket1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    socket1.bind((IP_DIRECTION,3500))
    messagesend= get_key() + " 3500"
    print(messagesend+"\n")
    socket1.sendto(messagesend.encode('utf-8'),(SOCKET,2000))

    message = socket1.recvfrom(2048)
    messagesend = message[0]
    keyget = messagesend[0:5]
    messagesend = keyget.decode("utf-8")

    return messagesend


#Gets the key fromthe Stage1, connects to that Socket, and proceeds to evaluate the ecuations.
def arithmetic():
    socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key=int(send_key())
    socket2.connect(('atclab.esi.uclm.es',key))

    op = False  #Condition that classifies the received equation is not well formed.

    while True:
        message = socket2.recvfrom(2048)
        if message == "": #If receives an empty message, breaks the loop-
            break
        operation = message[0]
        operation = operation.decode("utf-8")
        operation= simpl_oper(operation) #Replaces [ and { for ( and also for the closing ones.
        if len(operation) > 200: #In case we receive the instructions for the Stage 3, we break the loop.
            break
        if op: #In case the operation is not well formed, we save the original part and wait for the next packege, where the next part of the equation is.
            operation=part1+operation #Concatenate the 2 parts of the operation to create a well formed one.
        if check_balance(operation): #Checks if the received operation is well formed.
            op=False
            result = "(" + str(calculator(operation)) + ")" #Evaluates the equation and transforms it into string.
            socket2.sendto(result.encode('utf-8'), (SOCKET, key)) #Sends the result to the server.
        else: #In case is not well formed, triggers the op condition.
            print("Not well formed operation.")
            op = True
            part1 = str(operation)
    print("Out of loop.")


#Replaces the [,] and {,}  with (,)
def simpl_oper(operation):
    operation = operation.replace('[', '(')
    operation = operation.replace(']', ')')
    operation = operation.replace('{', '(')
    operation = operation.replace('}', ')')
    print(operation)
    return operation


# Based on https://codereview.stackexchange.com/questions/180567/checking-for-balanced-brackets-in-python
# Checks if the received operation
def check_balance(operation):
    queue = []

    for letter in operation:  # Goes throuth the whole operation, checking every single char in the operation.
        if letter == '(':  # If one of the characters in (, the closing one is added to the queue
            queue.append(')')
        elif letter == ')':
            if not queue or letter != queue.pop():  # Return false if queue is not empty or if that char is different to the one at the top of the queue.
                return False
    return not queue


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

        elif operation[i] == '+' or operation[i] == '-' or operation[i] == '*' or operation[i] == '/':
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
    else:
        print("Operation not found.")
        return int(0)


#Checks the preference of the operands.
def check_pref(char1, char2):

    if char2 == '(' or char2 == ')':
        return False
    elif (char1 == '*' or char1 == '/') and (char2 == '+' or char2 == '-'):
        return False
    else:
        return True


arithmetic()