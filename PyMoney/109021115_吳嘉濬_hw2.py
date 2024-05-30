import sys
import os

def initialize():
    try:
        fh=open('records.txt')
        try:
            if os.stat('records.txt').st_size<=1:
                sys.stderr.write('Empty file.\n')
            money=int(fh.readline())
            T=[(line.split()[0], int(line.split()[1])) for line in fh.readlines()]  #read each record and store it in (str(desc), int(amt)) type in list
            #print(T)  #for testing
            print('Welcome back!')
        except ValueError: #EOFError, TypeError
            sys.stderr.write('Invalid value in records.txt. Deleting the contents.\n')
            T=[]
            try:
                money=int(input('How much money do you have? '))
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                money=0
        except:
            sys.stderr.write('Invalid format in records.txt. Deleting the contents.\n')
            T=[]
            try:
                money=int(input('How much money do you have? '))
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                money=0
        #for line in fh.readlines():
        #    t=(line.split()[0], int(line.split()[1]))
        #    T.append(t)
    except FileNotFoundError as err:
        #sys.stderr.write(str(err))

        try:
            money=int(input('How much money do tou have? '))
        except ValueError:
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
            money=0
        T=[]  #initial overall record
    return money, T

def add(T):
    L=input('Add some expense or income records with description and amount:\ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n')
    try:
        for i in L.split(','):
            temp0=i.split()[0]
            temp1=i.split()[1]
    except:
        sys.stderr.write('The format of a record should be like this: breakfast -50.\nFail to add a record.\n')
    else:
        try:
            L=[(i.split()[0], int(i.split()[1])) for i in L.split(',')]  #first split records by ',', then split desc and amt by ' ', finally, covert str type amt to int type amt
            T.extend(L)  #extend newly added records to overall record
            #print(L)  #for testing
            #print(T)  #for testing
        except ValueError:
            sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
    return T

def view(money, T):
    print('Here\'s your expense and income records:')
    print('Description          Amount')
    print('==================== ======')
    for i in T:
        print(f'{i[0]:<20s} {i[1]:<6d}')  #align to the left
    print('==================== ======')
    total=sum([i[1] for i in T])  #compute total earn/cost
    print(f'Now you have {money+total} dollars.')

def delete(T):
    de=input('Which record do you want to delete?\n')
    try:
        de=(de.split()[0], int(de.split()[1]))  #convert to desire tuple to find/count record
    except:
        sys.stderr.write('Invalid format. Fail to delete a record.\n')
    #print(de)  #for testing
    cnt=T.count(de)
    if cnt==0:
        sys.stderr.write(f'There\'s no record with {de[0]} {de[1]}. Fail to delete a record.\n')
    elif cnt==1:
        T.remove(de)
    elif cnt>1:  #handle identical record case
        try:
            num=int(input(f'There are {cnt} identical records.\nPlease specify which one to delete by typing integer between 1(earliest) to {cnt}(latest)\n'))
        except ValueError:
            sys.stderr.write('Invalid value. Fail to delete a record.\n')
        else:
            if num>cnt or num<1:
                sys.stderr.write('Invalid input. Fail to delete a record.\n')
            else:
                count=0
                for i,j in enumerate(T):  #use enumerate() to get index info
                    if j==de:
                        count+=1
                    if count==num:  #num^th occurrence of de
                        del(T[i])  #need to know the corresponding index to delete desire record
                        break
    return T

def save(money, T):
    with open('records.txt','w') as fh:
        fh.write(str(money)+'\n')
        T2=[]
        for i in T:
            T2.append(i[0]+' '+str(i[1])+'\n')  #save each record in 'desc amt\n' format
        fh.writelines(T2)

initial_money, records = initialize()

while True:
    command = input('\nWhat do you want to do (add / view / delete / exit)? ')
    if command == 'add':
        records = add(records)
    elif command == 'view':
        view(initial_money, records)
    elif command == 'delete':
        records = delete(records)
    elif command == 'exit':
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')