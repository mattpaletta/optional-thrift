import sys
sys.path.append('gen-py')

from calculator_handler import CalculatorHandler


if __name__ == '__main__':
	handler = CalculatorHandler(use_rpc=True, server=True)

