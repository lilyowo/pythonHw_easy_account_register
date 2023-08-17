import sys
filename = "records.txt"

#enumerate、check tuple、add、delete、view、exit


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
    name = parts[0]
    cost = int(parts[1])
    # 創建元組
    item = (name, cost)

  except (IndexError, ValueError):
    # 當切分出現問題或者轉換成整數出現問題時報錯
    item = (0, 0)
  return item
  
# The 5 function definitions here
def initialize():
  """
  從recrods.txt讀取，或要求user重新輸入money
  初始化record money的值
  """
  record = []
  init_money = 0
    
  try:
    with open(filename, "r") as f: #file exit
      first =True
      lines = f.readlines()
      for line in lines:
        if(first):#讀取money
          try:
            first = False
            init_money = int(line.strip())
            print("Welcom back!")
          except ValueError:#(9)The first line can't be money number
            sys.stderr.write("Invald format in records.txt. Deleting the contents.\n")
            f.close()
            with open(filename, 'w') as f: pass
            init_money, record = first_set_money() 
            break
        else:#讀取record
          item = check_tuple(line.strip())#(10)Lines can't be records
          if item == (0,0):
            sys.stderr.write("Invald format in records.txt. Deleting the contents.\n")
            init_money, record = first_set_money()
            break
          else:
            record.append(item)  
      if(first):#(8)no lines in the file
        #sys.stderr.write("No lines in the file \"records.txt\"\n")
        init_money, record = first_set_money()
  except FileNotFoundError: #(7)找不到records.txt檔案
    #sys.stderr.write("File \"records.txt\" does not exit.\n");
    init_money, record = first_set_money() 
  return init_money, record
  
def add(money, record):
  """
  讀入新的item項目並更新money，若不符合格式則輸出錯誤並不做改變
  """
  print("Add an expense or income record with description and amount:")
  line = input()
  item = check_tuple(line)
  if(item == (0,0)):#(3)User inputs a string that cannot be split into a list of two strings
    checkType = len(list(line.split()))
    if(checkType == 1 or checkType > 2):
      sys.stderr.write("The format of a record should be like this: breakfast -50\n")
    else:#(4) the second string cannot be converted to integer.
      sys.stderr.write("Invalid value for money.\n")
    sys.stderr.write("Fail to add a record")
  else:#將item加入record並更新money
    record.append(item)
    money += item[1]
  
  return money, record

def view(money, record):
  """
  依照格式輸出花費、收入以及餘額。
  参数：餘額、紀錄
  """
  print("Here's your expense and income records:")
  print("{des: <15s}{amount: <15s}".format(des = "Description", amount = "Amount"))#給每個字15格的空間並置左對齊
  print("="*30)
  for item in record:#給每個字15格的空間並置左對齊
    print("{des: <15s}{amount: <15s}".format(des = item[0], amount = str(item[1])))
  print("="*30)
  print("Now you have {} dollars.".format(money))
  
def delete(money, record):
  """
  輸出當前records供user選擇，要求輸入index來刪除特定item，若輸入不合格式則輸出error
  """
  print("Which record do you want to delete?\n")
  #印出當前records以及其index
  print("{idx: <15s}{des: <15s}{amount: <15s}".format(des = "Description", amount = "Amount", idx = "Index"))
  print("="*45)
  for index, element in enumerate(record):
    print("{:<15}{:<15}{:<15}".format(index, element[0], element[1]))
  print("="*45)
  print("\nPlease input the index of record which you want to delete")
  idx = input()
  try:
    idx = int(idx)
    if(idx<0):#(6)the specified record does not exist.
      sys.stderr.write("Index out of bound. The Record doesn't exit.\nFail to delete a record.")
    else:
      item = record[idx]
      money -= item[1]
      record.remove(item);
  except(ValueError):#(5) the user inputs in an invalid format 
    sys.stderr.write("Invalid format. Fail to delete a record.")
  except(IndexError):#(6)the specified record does not exist.
    sys.stderr.write("Index out of bound. The Record doesn't exit.\nFail to delete a record.")
  
  return money, record
  
def save(money, record):
  """
  將經歷了一連串更新的record與money，存回去原先的文件
  """ 
  try:
    with open(filename, 'w') as f:#開啟欲寫入的文件
      f.write(str(money)+'\n')#寫入money值
      for tpl in record:#寫入records
        f.write('{} {}\n'.format(tpl[0], tpl[1]))
  except FileNotFoundError:#(7)找不到records.txt檔案
    with open(filename, 'a') as f:#創建一個file
      f.write(str(money)+'\n')#寫入money值
      for tpl in record:#寫入records
        f.write('{} {}\n'.format(tpl[0], tpl[1]))    

initial_money, records = initialize()
while True:
    command = input('\nWhat do you want to do (add / view / delete / exit)?\n')
    if command == 'add':
        initial_money, records = add(initial_money, records)
    elif command == 'view':
        view(initial_money, records)
    elif command == 'delete':
        initial_money, records = delete(initial_money,records)
    elif command == 'exit':
        save(initial_money, records)
        break
    else:#(2)User inputs a string that is not one of the four commands above.
        sys.stderr.write('Invalid command. Try again.\n')
  