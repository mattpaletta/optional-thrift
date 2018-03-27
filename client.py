import sys
sys.path.append('gen-py')

from calculator_handler import CalculatorHandler
from tutorial.ttypes import InvalidOperation, Operation, Work


def main():
    client = CalculatorHandler(use_rpc=True, server=False)
    
    client.ping()
    print('ping()')

    sum_ = client.add(1, 1)
    print('1+1=%d' % sum_)

    work = Work()

    work.op = Operation.DIVIDE
    work.num1 = 1
    work.num2 = 0

    try:
        quotient = client.calculate(1, work)
        print('Whoa? You know how to divide by zero?')
        print('FYI the answer is %d' % quotient)
    except InvalidOperation as e:
        print('InvalidOperation: %r' % e)

    work.op = Operation.SUBTRACT
    work.num1 = 15
    work.num2 = 10

    diff = client.calculate(1, work)
    print('15-10=%d' % diff)

    log = client.getStruct(1)
    print('Check log: %s' % log.value)

main()
