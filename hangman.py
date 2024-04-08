import random

someWords = '''apple banana mango strawberry  
orange grape pineapple apricot lemon coconut watermelon 
cherry papaya berry peach lychee muskmelon'''

someWords = someWords.split(" ")

picking = list(random.choice(someWords))
picking_og=picking.copy()

print('Guess the word! HINT: word is a name of a fruit')
display = list(f'_'*len(picking))
print(display)

count = 0
incorrect_guess = 0

while True:
    if incorrect_guess == len(picking)+5:
        print('Missed Opportunity')
        print(f'The fruit was {"".join(picking_og)}')
        break
    else:
        a = input('Enter an alphabet')
        if a in picking:
            p = picking.index(a)
            picking[p] = ""
            display[p] = a
            count +=1
            print(display)
        else:
            print('Retry')
            print(display)
            incorrect_guess += 1
            continue
        if count == len(picking):
            print('You guessed it right')
            print("".join(display))
            break


    





    

        





