import sys
sys.path.append('gen-py')

from calculator_handler import CalculatorHandler


if __name__ == '__main__':
    import logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]')
    ch.setFormatter(formatter)
    root.addHandler(ch)	
    handler = CalculatorHandler(use_rpc=True, server=True)

