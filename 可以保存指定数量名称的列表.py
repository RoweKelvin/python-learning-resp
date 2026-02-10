status=True
arr=[]
arrMaxLength=4
while status:
  if len(arr)==arrMaxLength:
    status=False
    break
  newName=input("请输入需要保存的名称")
  arr.append(newName)
print(arr)
