import pandas as pd
from RobotFactory import RobotFactory
import utils

pathRobots = './robots.xlsx'
pathStudents = 'students.txt'

robots = utils.generateUniqRobots(pathRobots, 50)
utils.checkUniq(robots)
robots = utils.objToStr(robots)

f = open(pathStudents, "r")
students = f.read().split('\n')

studentsCount = range(len(students))
data = map(lambda i: f'{i + 1}. {students[i]} => {robots[i]}', studentsCount)
print('\n'.join(data))