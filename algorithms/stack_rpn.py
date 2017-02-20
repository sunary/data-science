__author__ = 'sunary'


def eval_rpn(tokens):
    stack = []

    for elem in tokens:
        if elem in '+-*/':
            stack.append(str(eval(stack.pop() + elem + stack.pop())))
        else:
            stack.append(elem)

    return stack.pop()


if __name__ == '__main__':
    print eval_rpn(["2", "1", "+", "3", "*"])
    print eval_rpn(["4", "13", "5", "/", "+"])
