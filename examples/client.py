import sys
sys.path.append('gen-py')

from calculator_handler import CalculatorHandler
from tutorial.ttypes import InvalidOperation, Operation, Work


def main():
    import logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode")
    args = parser.parse_args()
    
    assert args.mode in ["cluster", "local"], "mode can only be `local` or `cluster`"

    start_with_rpc = (args.mode == "cluster")
    client = CalculatorHandler(use_rpc=start_with_rpc, server=False)
    
    client.ping()
    logging.info('ping()')

    sum_ = client.add(1, 1)
    logging.info('1+1=%d' % sum_)

    work = Work()

    work.op = Operation.DIVIDE
    work.num1 = 1
    work.num2 = 0

    try:
        quotient = client.calculate(1, work)
        logging.info('Whoa? You know how to divide by zero?')
        logging.info('FYI the answer is %d' % quotient)
    except InvalidOperation as e:
        logging.info('InvalidOperation: %r' % e)

    work.op = Operation.SUBTRACT
    work.num1 = 15
    work.num2 = 10

    diff = client.calculate(1, work)
    logging.info('15-10=%d' % diff)

    log = client.getStruct(1)
    logging.info('Check log: %s' % log.value)

main()
