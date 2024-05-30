import sys
import os

class Record:
    """Represent a record."""
    def __init__(self, cat, desc, amt):
        '''For initialization, set the initial attribute value.'''
        self._cat = str(cat)
        self._desc = str(desc)
        self._amt = int(amt)
    @property
    def cat(self):
        '''Get cat attribute value.'''
        return self._cat
    @property
    def desc(self):
        '''Get desc attribute value.'''
        return self._desc
    @property
    def amt(self):
        '''Get amt attribute value.'''
        return self._amt

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        '''For initialization, loading the old records (if any).'''
        try:
            fh=open('records.txt')
            try:
                if os.stat('records.txt').st_size<=1:
                    sys.stderr.write('Empty file\n')
                self._initial_money=int(fh.readline())
                self._records=[Record(line.split()[0], line.split()[1], int(line.split()[2])) for line in fh.readlines()]
                print('Welcome back!')
            except:
                sys.stderr.write('Invalid value in records.txt. Deleting the contents.\n')
                self._records=[]
                try:
                    self._initial_money=int(input('How much money do you have? '))
                except ValueError:
                    sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                    self._initial_money=0
        except FileNotFoundError as err:
            try:
                self._initial_money=int(input('How much money do you have? '))
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                self._initial_money=0
            self._records=[]

    def add(self, record, categories):
        '''For adding new record(s) in "records".'''
        try:
            for i in record.split(','):
                temp0=i.split()[0]
                valid=categories.is_category_valid(temp0)  #correct? original:(temp0, categories)
                #print(valid)
                #valid=categories.find_subcategories(temp0)
                #print(valid)
                if valid==False:
                    print(f'The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.')
                    return
                temp1=i.split()[1]
                temp2=i.split()[2]
        except:
            sys.stderr.write('The format of a record should be like this: meal breakfast -50.\nFail to add a record.\n')
        else:
            try:
                #record=[(i.split()[0], i.split()[1], int(i.split()[2])) for i in record.split(',')]
                #self._records.extend(record)
                for i in record.split(','):
                    self._records.append(Record(i.split()[0], i.split()[1], int(i.split()[2])))
            except ValueError:
                sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
        #return  #can omit?

    def view(self):
        '''For viewing the overall records.'''
        print('Here\'s your expense and income records:')
        print('Category        Description          Amount')
        print('=============== ==================== ======')
        for i in self._records:
            print(f'{i.cat:<15s} {i.desc:<20s} {i.amt:<6d}')
        print('=============== ==================== ======')
        total=sum([i.amt for i in self._records])
        print(f'Now you have {self._initial_money+total} dollars.')

    def delete(self, delete_record):
        '''For deleting exist record.'''
        try:
            delete=(delete_record.split()[0], delete_record.split()[1], int(delete_record.split()[2]))
        except:
            sys.stderr.write('Invalid format. Fail to delete a record.\n')
            return
        cnt=0
        for i, j in enumerate(self._records):
            if delete[0]==j.cat and delete[1]==j.desc and delete[2]==j.amt:
                cnt+=1
        if cnt==0:
            sys.stderr.write(f'There\'s no record with {delete[0]} {delete[1]} {delete[2]}. Fail to delete a record.\n')
        elif cnt==1:
            for i, j in enumerate(self._records):
                if delete[0]==j.cat and delete[1]==j.desc and delete[2]==j.amt:
                    del(self._records[i])
        else:
            try:
                num=int(input(f'There are {cnt} identical records.\nPlease specify which one to delete by typing integer between 1(earliest) to {cnt}(latest)\n'))
            except ValueError:
                sys.stderr.write('Invalid value. Fail to delete a record.\n')
            else:
                if num>cnt or num<1:
                    sys.stderr.write('Invalid input. Fail to delete a record.\n')
                else:
                    count=0
                    for i, j in enumerate(self._records):
                        if delete[0]==j.cat and delete[1]==j.desc and delete[2]==j.amt:
                            count+=1
                        if count==num:
                            del(self._records[i])
                            break

    def find(self, target_categories, category):  #target_categories == l on top
        '''Show all records whose category is in "target_categories" list.'''
        t2=filter(lambda i:i.cat in target_categories, self._records)
        print(f'Here\'s your expense and income records under category "{category}":')
        print('Category        Description          Amount')
        print('=============== ==================== ======')
        total=0
        for j in t2:
            print(f'{j.cat:<15s} {j.desc:<20s} {j.amt:<6d}')
            total+=j.amt
        print('=============== ==================== ======')
        print(f'The total amount above is {total}.')

    def save(self):
        '''For saving all records in txt file, so next time when you re-execute this file, the old records will NOT be lost.'''
        with open('records.txt','w') as fh:
            fh.write(str(self._initial_money)+'\n')
            t2=[]
            for i in self._records:
                t2.append(i.cat+' '+i.desc+' '+str(i.amt)+'\n')
            fh.writelines(t2)

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        '''Record the categories\' structure hierarchically.'''
        self._categories=['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

    def view(self):
        '''Show all categories and subcategories hierarchically.'''
        def _view_cat(l, level=0):
            if l == None:
                return
            if type(l) == list:
                for child in l:
                    _view_cat(child, level+1)  #correct?
            else:
                print(f'{" "*2*(level-1)}- {l}')

        _view_cat(self._categories)

    def is_category_valid(self, cat):
        '''To check if the category name given by user is existed(valid).'''
        def _is_cat_valid(cat, cats):
            if type(cats) in {list, tuple}:
                for i, v in enumerate(cats):
                    p = _is_cat_valid(cat, v)
                    if p == True:
                        return (i,)
                    if p != False:
                        return (i,)+p
            return cat == cats

        return _is_cat_valid(cat, self._categories)

    def find_subcategories(self, cat):
        '''Find all (sub)categories rooted by "cat".'''
        def find_subcategories_gen(cat, cats, found=False):
            if type(cats) == list:
                for index, child in enumerate(cats):
                    yield from find_subcategories_gen(cat, child, found)
                    if child == cat and index + 1 < len(cats) and type(cats[index + 1]) == list:
                        yield from find_subcategories_gen(cat, cats[index + 1], True)
            else:
                if cats == cat or found == True:
                    yield cats

        #print([x for x in find_subcategories_gen(cat, self._categories)])
        return list(find_subcategories_gen(cat, self._categories))

categories = Categories()
records = Records()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input('Add some expense or income records with category, description, and amount (seperate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n')
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input('Which record do you want to delete? ')
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories, category)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')