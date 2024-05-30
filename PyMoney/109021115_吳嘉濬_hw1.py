money=input("How much money do you have? ")
while(1):
    print("Add an expense or income record with description and amount:")
    str=input().split()
    left=int(money)+int(str[1])
    if(left<0):
        print("You cannot afford it!\nYou need %d dollars more!" % -left)
        reply=input("Wanna buy something else? (y/n) ")
        if(reply!='y'):
            break
    else:
        print("Now you have %d dollars." % left)
        break