def forLoop(numList:list):
  for i in numList:
    print(i)
def count(maxNum:int=5):
  for i in range(maxNum):
    print(i)
def main():
  forLoop([1,5,6,8,9])
  count()
main()
