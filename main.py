import sys
filename = "records.txt"
# other functions
def first_set_money():
  """
  要求重新輸入money並reset record
  """
  try:
    init_money = int(input("How much money do you have?\n"))
  except ValueError:#(1)The user inputs a string that cannot be converted to integer.
    sys.stderr.write("Invalid value for money. Set to 0 by default.")
    init_money = 0
  record = [] 
  return init_money, record
  
def check_tuple(line):
  """
  用於確認item string是否符合格式，並將之轉換為tuple回傳
  否則回傳(0,0)
  """
  try:
    # 切分字串為兩個部分，預期第二個為整數，第一個為字串
    parts = line.split()
    cate = parts[0]
    name = parts[1]
    cost = int(parts[2])
    # 創建元組
    item = (cate, name, cost)
    
  except (IndexError, ValueError):
    # 當切分出現問題或者轉換成整數出現問題時報錯
    item = (0, 0, 0)
  return item
 
# class definitions here
class Record:
  """Represent a record."""
  def __init__(self, cat, name, cost):
    self._cat = cat
    self._name = name
    self._cost = cost
  @property
  def cat(self): return self._cat
  @property
  def name(self): return self._name
  @property
  def cost(self): return self._cost
  
class Records:
  """
  Maintain a list of all the 'Record's and the initial amount of
  money.
  """
  def __init__(self):
    """
    從recrods.txt讀取，或要求user重新輸入money
    初始化record money的值
    """
    self._records = []
    self._init_money = 0
    try:
      with open(filename, "r") as f: #file exit
        first =True
        lines = f.readlines()
        for line in lines:
          if(first):#讀取money
            try:
              first = False
              self._init_money = int(line.strip())
              print("Welcom back!")
            except ValueError:#(9)The first line can't be money number
              sys.stderr.write("Invald format in records.txt. Deleting the contents.\n")
              f.close()
              with open(filename, 'w') as f: pass
              self._init_money, self._records = first_set_money() 
              break
          else:#讀取record
            item = check_tuple(line.strip())#(10)Lines can't be records
            if item == (0,0,0):
              sys.stderr.write("Invald format in records.txt. Deleting the contents.\n")
              self._init_money, self._records = first_set_money()
              break
            else:
              record = Record(item[0], item[1], item[2])
              self._records.append(record)  
        if(first):#(8)no lines in the file
          #sys.stderr.write("No lines in the file \"records.txt\"\n")
          self._init_money, self._records = first_set_money()
    except FileNotFoundError: #(7)找不到records.txt檔案
      #sys.stderr.write("File \"records.txt\" does not exit.\n");
      self._init_money, self._records = first_set_money() 
  @property
  def init_money(self): return self._init_money
  @property
  def records(self): return self._records
    
  def add(self,line, all_cat):
    """    讀入新的item項目並更新money，若不符合格式則輸出錯誤並不做改變    """
    item = check_tuple(line)
    if(item == (0,0,0)):#(3)User inputs a string that cannot be split into a list of two strings
      checkType = len(list(line.split()))
      if(checkType != 3):
        sys.stderr.write("The format of a record should be like this: breakfast -50\n")
      else:#(4) the second string cannot be converted to integer.
        sys.stderr.write("Invalid value for money.\n")
      sys.stderr.write("Fail to add a record")
    else:#將item加入record並更新money
      if(all_cat.is_category_valid(item[0])):
        record = Record(item[0], item[1], item[2])
        self._records.append(record)
        self._init_money += item[2]
      else:
        sys.stderr.write("The specified category is not in the category list.\n")
        sys.stderr.write("You can check the category list by command \"view categories\".\n")
        sys.stderr.write("Fail to add a record.\n")
      
  def view(self):
    """
    依照格式輸出花費、收入以及餘額。
    参数：餘額、紀錄
    """
    print("Here's your expense and income records:")
    print("{cat: <15s}{des: <15s}{amount: <15s}".format(cat = "Category", des = "Description", amount = "Amount"))#給每個字15格的空間並置左對齊
    print(f'{"="*14} {"="*14} {"="*14}')
    for item in self._records:#給每個字15格的空間並置左對齊
      print("{cat: <15s}{des: <15s}{amount: <15s}".format(cat = item.cat, des = item.name, amount = str(item.cost)))
    print(f'{"="*14} {"="*14} {"="*14}')
    print("Now you have {} dollars.".format(self._init_money))
    
  def delete(self, record):
    """    輸入欲刪除之record，刪除特定item，若輸入不合格式則輸出error    """
    item = check_tuple(record)
    if(item == (0,0,0)):#(3)User inputs a string that cannot be split into a list of three strings
      checkType = len(list(record.split()))
      if(checkType != 3):
        sys.stderr.write("The format of a record should be like this: meal breakfast -50\n")
      else:#(4) the second string cannot be converted to integer.
        sys.stderr.write("Invalid value for money.\n")
      sys.stderr.write("Fail to delete a record")
    else:#將item從record刪除並更新money
      not_found = True
      for re in self._records:
        if(item[0]==re.cat and item[1]==re.name and item[2]==re.cost):
          self._init_money -= re.cost
          self._records.remove(re)          
          not_found = False

      if(not_found):
        sys.stderr.write("Record \"{}\"is not found.\n".format(record))
        sys.stderr.write("You can check the records list by command \"view\".\n")
        sys.stderr.write("Fail to delete a record.\n")
    
  def find(self, sub_cat):
    """
    給所有sub cat
    印出涵蓋範圍之類別的所有紀錄"""
    
    if(sub_cat==[]):
      sys.stderr.write("There is no such category.\n")
    else:
      tt_amount = 0
      print("{cat: <15s}{des: <15s}{amount: <15s}".format(cat = "Category", des = "Description", amount = "Amount"))
      print(f'{"="*14} {"="*14} {"="*14}')
      sub_record = filter(lambda x:x.cat in sub_cat, self._records)
      for item in sub_record:
        tt_amount += item.cost
        print("{cat: <15s}{des: <15s}{amount: <15s}".format(cat = item.cat, des = item.name, amount = str(item.cost)))
      print(f'{"="*14} {"="*14} {"="*14}')
      print(f"The total amount above is {tt_amount}.")
      
  def save(self):
    """ 將經歷了一連串更新的record與money，存回去原先的文件""" 
    try:
      with open(filename, 'w') as f:#開啟欲寫入的文件
        f.write(str(self._init_money)+'\n')#寫入money值
        for tpl in self._records:#寫入records
          f.write('{} {} {}\n'.format(tpl.cat, tpl.name, tpl.cost))
    except FileNotFoundError:#(7)找不到records.txt檔案
      with open(filename, 'a') as f:#創建一個file
        f.write(str(self._init_money)+'\n')#寫入money值
        for tpl in self._records:#寫入records
          f.write('{} {} {}\n'.format(tpl.cat, tpl.name, tpl.cost))

class Categories:
  """Maintain the category list and provide some methods."""
  def __init__(self):
    """初始化所有分類"""
    self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation',['bus', 'railway']], 'income', ['salary', 'bonus']]
    
  @property
  def categories(self): return self._categories
  
 
  def view(self, L, level=0):
    """依照層級印出所有類別"""
    # 3. Alternatively, define an inner function to do the recursion.
    if L==None: return
    if type(L) in {list, tuple}:
      for child in L:
        self.view(child, level+1)
    else:
      print(f'{" "*4*level}-{L}')
  
  
  def is_category_valid(self, cat):
    """    確認cat這個類別是否存在於當前的all_cat中    """
    for i in self._flatten(self.categories):
      if i==cat: return True
    return False

  def find_subcategories(self, cat):
    """
    找cat類別的子集所有元素
    回傳一個包含cat以及其子集所有元素的list
    """
    def find_subcategories_gen(cat, all_cat, found = False):  
      same_level_f = False
      if type(all_cat) == list:
        for child in all_cat:
          if type(child) == list and same_level_f==False:#拆開下一個list
            yield from find_subcategories_gen(cat, child) #這裡要有from才可以一個一個抓出yield的東西
          elif type(child)==list and same_level_f:
            yield from self._flatten(child)
            break
          elif(child==cat):
            same_level_f = True
            yield cat
      elif cat == all_cat: 
        yield all_cat
      else: yield None
    return [i for i in find_subcategories_gen(cat, self.categories)]  

  def _flatten(self, L):
    if L is None: return
    if type(L) == list:
      for child in L:
        for atom in self._flatten(child):
          yield atom
    else: yield L
  

categories = Categories()
records = Records()
while True:
  command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)?\n ')
  if command == 'add':
    record = input('Add an expense or income record with categories, description and amount (separate by spaces):\n')
    records.add(record, categories)
  elif command == 'view':
    records.view()
  elif command == 'delete':
    delete_record = input("Which record do you want to delete? \n")
    records.delete(delete_record)
  elif command == 'view categories':
    categories.view(categories.categories, 0)
  elif command == 'find':
    category = input('Which category do you want to find? ')
    target_categories = categories.find_subcategories(category)
    records.find(target_categories)
  elif command == 'exit':
    records.save()
    break
  else:
    sys.stderr.write('Invalid command. Try again.\n')