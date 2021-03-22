import pandas as pd
from RobotFactory import RobotFactory

def exists(array, item):
  try:
    array.index(item)
    return True
  except ValueError:
    return False

def generateUniqRobots(path, count):
  df = pd.read_excel(path)
  robot = RobotFactory(df, 2 * count)

  result = []

  for i in range(count):
    while True:
      Robot = next(robot)
      if exists(result, Robot):
        continue
      result.append(Robot)
      break

  return result

def checkUniq(array):
  count = 0
  for i in range(len(array)):
    for j in range(len(array)):
      if i != j and array[i] == array[j]:
        count += 1
        print('Item: ', array[i])
  print(f'Найдено совпадений: {count}')


def objToStr(array):
  data = []
  for i in array:
    result = []
    items = list(i.items())
    for item in items:
      if type(item[1]) == str:
        result.append(f'{item[1]}')
      if type(item[1]) == dict:
        result.append(f'{item[0]}: {item[1]["title"]}')
    data.append(', '.join(result))
  return data