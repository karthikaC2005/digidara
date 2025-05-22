def ispalin(string):
        if(string.lower()==string[::-1].lower()):
            return "It is a palindrome"
        else:
            return "It is not a palindrome"
string=input("enter a string")
print(ispalin(string))         