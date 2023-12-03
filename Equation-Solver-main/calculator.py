from sympy.abc import *
from sympy import solve
from sympy.parsing.sympy_parser import parse_expr

def solve_meThis(string_, no_of_equations):
    try:
        equations = []
        splits = string_.split(',')
        for index in range(no_of_equations):
            lhs =  parse_expr(splits[index].split("=")[0])
            rhs =  parse_expr(splits[index].split("=")[1])
            eq = lhs-rhs
            equations.append(eq)

        solution = solve(equations)
        if type(solution) is not list:
            solution = [solution]
        return solution
    except:
        print("invalid equation")

def solver(operation):
    def operate(fb, sb, op):
        result = 0
        if operator == '+':
            result = int(first_buffer) + int(second_buffer)
        elif operator == '-':
            result = int(first_buffer) - int(second_buffer)
        elif operator == 'x':
            result = int(first_buffer) * int(second_buffer)
        elif operator == '/':
            result = int(first_buffer) / int(second_buffer)            
        return result

    if not operation or not operation[0].isdigit():
        return -1

    operator = ''
    first_buffer = ''
    second_buffer = ''

    for i in range(len(operation)):
        if operation[i].isdigit():
            if len(second_buffer) == 0 and len(operator) == 0:
                first_buffer += operation[i]
            else:
                second_buffer += operation[i]
        else:
            if len(second_buffer) != 0:
                result = operate(first_buffer, second_buffer, operator)
                first_buffer = str(result)
                second_buffer = ''
            operator = operation[i]

    result = int(first_buffer)
    if len(second_buffer) != 0 and len(operator) != 0:
        result = operate(first_buffer, second_buffer, operator)

    if type(result) is not list:
            result = [result]
    return result

def calculate(operation):
    string,head = '', None
    temp = string = str(operation)
    if 'D' in string:
        string = string.replace('D', '0')
    if 'G' in string:
        string = string.replace('G', '6')
    if 'B' in string:
        string = string.replace('B', '8')
    if 'Z' in string:
        string = string.replace('Z', '2')
    if 'S' in string:
        string = string.replace('S', '=')
    if 'M' in string:
        string = string.replace('M', '-')
    if 'W' in string:
        string = string.replace('W', '-')

    if '=' not in string:
        if 'X' in string:
            string = string.replace('X', '*')

        solution = eval(string)
        if type(solution) is not list:
            solution = [solution]
        return string, solution
        
    splits = string.split(',')
    no_of_equations = len(splits)
    result = ''
    for operation in splits:
        if result != '':
            result += ','
        string = ''
        for k in operation:
            if head is None:
                head = k
                string += head
            elif k in ['+', '-', '=', '/'] or head in ['+', '-', '=', '/']:
                head = k
                string += head
            elif k in ['('] and head in [')']:
                head = k
                added = '*' + k
                string += added
            elif k in ['(', ')'] or head in ['(', ')']:
                head = k
                string += head
            elif k.isnumeric() and not head.isnumeric():
                head = k
                added = '**' + k
                string += added
            elif not k.isnumeric() and head.isnumeric():
                head = k
                added = '*' + k
                string += added
            elif k.isnumeric():
                head = k
                string += head
        result += string
    
    print(result)
    if '=' not in result:
        return result, solver(result)
    else:
        return result, solve_meThis(result, no_of_equations)
