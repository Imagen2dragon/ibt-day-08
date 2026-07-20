name = "hello world "
def reversefunction(name):
	if len(name) == 0:
		return ""

	stack = []
	for character in name:
		stack.append(character)

	reversed_name = ""
	while len(stack) > 0:
		reversed_name += stack.pop()
	return reversed_name

print(reversefunction(name))

"""" two pointer"""
list_number = [1,2,3,4,5,6,7,8,9]
x = len(list_number)
Left = 0
Right = len(list_number) - 1

while Left < Right:
    list_number[Left], list_number[Right] = list_number[Right], list_number[Left]
    Left += 1
    Right -= 1

print(list_number)
for i in range (x -1, -1, -1) :
    print(list_number[i])


