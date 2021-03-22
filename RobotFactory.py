import pandas as pd
import random

class RobotFactory:
    def __init__(self, df, rang = 100, multiplier = 1):
      self.__rang = rang
      self.__multiplier = multiplier
      self.__columns = self.__getColumns(df)
      self.__statTypes = self.__getStatTypes(df)
      self.__df = self.__getDataFrame(df)
      self.__rows = self.__getRows()
      self.__types = self.__getTypes()

    def __getColumns(self, df):
      columns = []
      for item in list(df.columns):
        components = item.replace(',', '.').split(' ')
        key = components[0]
        value = ''
        if len(components) > 1:
          value = float(components[1]) * self.__rang * self.__multiplier
        columns.append(f'{key} {value}')
      return columns

    def __getStatTypes(self, df):
      firstColumn = df[df.columns[0]]
      filteredColumn = filter(lambda i: type(i) == str, firstColumn)
      return list(filteredColumn)

    def __getDataFrame(self, df):
      data = []
      for i in range(len(df)):
        row = df.iloc[i]
        dataRow = []
        for item in row:
          elem = item
          if type(item) != str: 
            elem = item * self.__rang * self.__multiplier
          dataRow.append(elem)
        if type(df.iloc[i, 0]) == str:
          title = df.iloc[i, 0]
        dataRow[0] = title
        data.append(dataRow)
      return pd.DataFrame(data, columns=self.__columns)
      
    def __getRows(self, column = 0):
      data = []
      for i in range(len(self.__df)):
        statType = self.__df.iloc[i, 0]
        statTitle = self.__df.iloc[i, 1]
        statValue = self.__df.iloc[i, column + 2]
        data.append({
          'type': statType,
          'title': statTitle,
          'value': statValue,
        })
      return data

    def __getTypes(self):
      types = []
      for i in range(2, len(self.__columns)):
        item = self.__columns[i]
        key, value = item.split(' ')
        types.append({
          'orig': item,
          'title': key,
          'count': float(value),
        })
      types = self.__typesWithStats(types)
      return types

    def __findAllBy(self, array, key, value):
      return list(filter(lambda i: i[key] == value, array))
    
    def __pick(self, array, params):
      result = []
      for item in array:
        elem = {}
        for field in params:
          if field in list(item.keys()):
            elem[field] = item[field]
        result.append(elem)
      return result

    def __typesWithStats(self, types):
      for i in range(len(types)):
        data = self.__getRows(i)
        for statType in self.__statTypes:
          values = self.__findAllBy(data, 'type', statType)
          types[i][statType] = self.__pick(values, ['title', 'value'])
      return types

    def __next__(self):
      data = {}
      while len(self.__types):
        typeIndex = random.randint(0, len(self.__types) - 1)
        if self.__types[typeIndex]['count'] == 0.0:
          self.__types.remove(self.__types[typeIndex])
          continue;

        data['title'] = self.__types[typeIndex]['title']
        
        for statType in self.__statTypes:
          stats = self.__types[typeIndex][statType]
          while len(stats):
            statsIndex = random.randint(0, len(stats) - 1)
            if stats[statsIndex]['value'] == 0.0:
              self.__types[typeIndex][statType].remove(stats[statsIndex])
              continue;

            data[statType] = {
              'title': stats[statsIndex]['title'],
            }
            break;

        self.__types[typeIndex]['count'] -= 1
        break;
      return data
    
    def __getData(self):
      return self.__types

    data = property(__getData)