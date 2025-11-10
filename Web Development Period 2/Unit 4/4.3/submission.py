list_of_words = open('enable1.txt').read().splitlines()

number_one = [w for w in list_of_words if len(w) == 6]

number_two = [w for w in list_of_words if 'e' in w]

number_three = [w for w in list_of_words if 'e' not in w] 

number_four=[w for w in list_of_words if len(w)==5 and 'e' in w[1:]]