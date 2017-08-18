import random
a=str(random.randint(1000,9999))
print(a)
b=str(input('enter 4 digit number'))
count1=0
count2=0
for i in range(4):
    if a[i]==b[i]:
         count1=count1+1
    else:
        count2=count2+1

print('number of cows is'+" "+str(count1))
print('number of bulls is'+" "+str(count2))
