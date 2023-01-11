from flask import Flask, request, jsonify
import math

app = Flask(__name__)
host = "localhost"
port = 8496
stack = list()
simple_sign = ["plus", "minus", "times", "divide", "pow"]
one_num_sign = ["abs", "fact"]


@app.route('/stack/size', methods=['GET'])
def get_stack_size():
    return str(len(stack)), 200


@app.route('/stack/operate', methods=['GET'])
def invoke_operation():
    sign = request.args.get('operation').lower()
    if sign in simple_sign:
        if len(stack) < 2:
            return "Error: cannot implement operation" + sign + ". It requires 2 " \
                                                                "arguments and the stack has only " + str(
                len(stack)) + " arguments", 409
        numbers = [stack.pop(), stack.pop()]
        if numbers[1] == 0 and sign == "divide":
            return "Error while performing operation Divide: division by 0", 409
        else:
            return str(calc(sign, numbers))

    elif sign in one_num_sign:
        if len(stack) < 1:
            return "Error: cannot implement operation" + sign + ". It requires 1 " \
                                                                "arguments and the stack has only" + str(
                len(stack)) + "arguments", 409
        numbers = [stack.pop()]
        if numbers[0] < 0 and sign == "fact":
            return "Error while performing operation Factorial: not supported for the negative number", 409
        else:
            return str(calc(sign, numbers))
    else:
        return "Error: unknown operation: " + sign, 409


@app.route('/stack/arguments', methods=['PUT'])
def add_arguments():
    content = request.json
    numbers = content['arguments']
    for number in numbers:
        stack.append(int(number))
    return str(len(stack)), 200


@app.route('/independent/calculate', methods=['POST'])
def independent_calc():
    content = request.json
    numbers = content['arguments']
    sign = content['operation'].lower()

    if sign in one_num_sign:
        if len(numbers) < 1:
            return "Error: Not enough arguments to perform the operation" + sign, 409
        elif len(numbers) > 1:
            return "Error: Too many arguments to perform the operation " + sign, 409
        elif sign == "factorial" and int(numbers[0]) < 0:
            return "Error while performing operation Factorial: not supported for the negative number", 409
        else:
            return str(calc(sign, numbers))

    elif sign in simple_sign:
        if len(numbers) < 2:
            return "Error: Not enough arguments to perform the operation" + sign, 409
        elif len(numbers) > 2:
            return "Error: Too many arguments to perform the operation " + sign, 409
        elif sign == 'divide' and int(numbers[1]) == 0:
            return "Error while performing operation Divide: division by 0", 409
        else:
            return str(calc(sign, numbers))

    else:
        return "Error: unknown operation: " + sign


@app.route('/stack/arguments', methods=['DELETE'])
def delete_from_stack():
    count = int(request.args.get('count'))
    if len(stack) < count:
        return "Error: cannot remove " + str(count) + " from the stack. It has only " + str(
            len(stack)) + " arguments", 409
    for i in range(count):
        stack.pop()
    return str(len(stack)), 200


def calc(sign, numbers):
    if sign == "plus":
        return int(numbers[0]) + int(numbers[1])
    elif sign == "minus":
        return int(numbers[0]) - int(numbers[1])
    elif sign == "times":
        return int(numbers[0]) * int(numbers[1])
    elif sign == "divide":
        return int(int(numbers[0]) / int(numbers[1]))
    elif sign == "pow":
        return pow(int(numbers[0]), int(numbers[1]))
    elif sign == "abs":
        return abs(int(numbers[0]))
    elif sign == "fact":
        return math.factorial(numbers[0])


if __name__ == '__main__':
    app.run(host=host, port=port)
