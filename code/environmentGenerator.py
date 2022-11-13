import random
def genLayout(x,y):
    for length in range(1,y+1):
        if(length==1 or length==y):
            for _ in range(x):
                print("%",end='')
            print('')
        else:
            print("%",end='')
            for _ in range(x-2):
                if random.randint(0,9)%5==0:
                    print(".",end="")
                elif random.randint(0,9)%5==1:
                    print("%",end="")
                else:
                    print(" ",end='')
            print("%")
    



genLayout(100,300)

# i=1
# while(i<10):
#     envString = "envgen{}.lay".format(i)
#     x = open(envString,"w")
