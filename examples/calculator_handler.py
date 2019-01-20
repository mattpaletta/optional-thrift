import sys
import logging
sys.path.append("gen-py")


from shared.ttypes import SharedStruct
from tutorial import Calculator
from tutorial.ttypes import InvalidOperation, Operation

from optionalthrift.service import Service


@Service(thrift_class=Calculator, port=1111)
class CalculatorHandler(object):
    def __init__(self, use_rpc=False, server=False):
        self.log = {}
        if use_rpc:
            logging.info("Using RPC!")
        else:
            logging.info("Not using RPC, using Singleton instead.")
        if server:
            logging.info("I'm a server!")
        else:
            logging.info("I'm a client!")

    def ping(self):
        logging.info('ping()')

    def add(self, n1, n2):
        logging.info('add({0}, {1})'.format(n1, n2))
        return n1 + n2

    def calculate(self, logid, work):
        logging.info('calculate({0}, {1})'.format(logid, work))

        if work.op == Operation.ADD:
            val = work.num1 + work.num2
        elif work.op == Operation.SUBTRACT:
            val = work.num1 - work.num2
        elif work.op == Operation.MULTIPLY:
            val = work.num1 * work.num2
        elif work.op == Operation.DIVIDE:
            if work.num2 == 0:
                x = InvalidOperation()
                x.whatOp = work.op
                x.why = 'Cannot divide by 0'
                raise x
            val = work.num1 / work.num2
        else:
            x = InvalidOperation()
            x.whatOp = work.op
            x.why = 'Invalid operation'
            raise x

        log = SharedStruct(key=int(logid), value=str(val))
        self.log[logid] = log

        return val

    def get_struct(self, key):
        logging.info('get_struct({0})'.format(key))
        return self.log[key]

    def done(self):
        from time import sleep
        logging.info("Waiting for client to sleep")
        sleep(10)
        logging.info("Goodbye!")
        exit(0)

