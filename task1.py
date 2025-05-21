a=int(input("enter a value:"))
if a>=0 and a>100:
    print("it is a positive number and it is greater than 100")
elif a>=0 and a<100:
    print("it is a positive number and it is less than 100")
elif a<0 and a>-100:
    print("it is a negative number and it is greater than -100")
elif a<0 and a<-100:
    print("it is a negative number and it is less than -100")
else:
    print("it is a zero")
