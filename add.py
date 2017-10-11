import sys
def add(num1, num2):
	return num1 / num2

def multiply(num3, num4):
	return num3 * num4

print(int(multiply(add(int(sys.argv[1]), int(sys.argv[2])), 100)))