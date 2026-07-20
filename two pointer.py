"""two pointer example"""
number_arr = [4, 5, 9, 10, 11, 1]
target =21
arr_length = len(number_arr)
Left = 0
Right = len(number_arr) - 1
while Left < Right:
	current_sum = number_arr[Left] + number_arr[Right]
	if current_sum == target:
		print(f"Pair found: {number_arr[Left]}, {number_arr[Right]} for target {target}" )
		break
	elif current_sum < target:
		Left += 1
	elif current_sum > target:
		Right -= 1
	else :
		print("No pair found")