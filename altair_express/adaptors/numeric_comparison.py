from ..interactors import Adaptor

def op_to_string(op):
    if op =="==":
        return "eq"
    elif op =="<":
        return "lt"
    elif op =="<=":
        return "lte"
    elif op ==">":
        return "gt"
    elif op ==">=":
        return "gte"
    elif op =="!=":
        return "ne"
    else:
        return "eq"

def numeric_comparison(input, op, value):
    adaptor = Adaptor(input, name=f"{input.name}{op_to_string(op)}{value}")
    adaptor.update = f"{input.name}{op}{value}"
    return adaptor