from structures.location import Location
import random

from engine.virus import Virus
from walkers.Walker import Walker

import walkers.healthState as h

HOME = 0
WORKPLACE = 1
GROCERIES_STORE = 2
SCHOOL = 3
LEISURE = 4

# Home default parameters
HOME_X = 640 # HOME_X = 20
HOME_Y = 480 # HOME_Y = 30
HOME_CAPACITY = 6

STARTING_FOOD = 10
FAMILY_MEMBERS = HOME_CAPACITY
STARTING_MONEY = 4000

# Workplace default parameters
WORK_X = 50
WORK_Y = 100
WORK_CAPACITY = 30

REST_DAYS = [5, 6]
SALARY = 1500

# GroceriesStore default parameters
STORE_X = 60
STORE_Y = 80
STORE_CAPACITY = 30

FOOD_PRICE = 3

# School default parameters
SCHOOL_X = 100
SCHOOL_Y = 100
SCHOOL_CAPACITY = 100

# Leisure default parameters
FUN_X = 60
FUN_Y = 80
FUN_CAPACITY = 30


class Home (Location):

    def __init__(self, size_x, size_y, max_capacity, food_qty, family_qty, money):

        super().__init__(size_x, size_y, max_capacity)
        self.food_qty = food_qty
        self.family_qty = family_qty
        self.money = money
    # end __init__

    def needFood(self):
        return self.food_qty < self.family_qty
    # end needFood

    def eatFood(self):
        self.food_qty -= self.family_qty
    # end eatFood

    def bringFood(self, food):
        self.food_qty += food
    # end bringFood

# end class Home


def buildDefaultHome():
    return Home(HOME_X, HOME_Y, HOME_CAPACITY, STARTING_FOOD,FAMILY_MEMBERS, STARTING_MONEY)
# end buildDefaultHome


class Workplace (Location):

    def __init__(self, size_x, size_y, max_capacity, rest_days, salary):

        super().__init__(size_x, size_y, max_capacity)
        self.rest_days = rest_days
        self.salary = salary
    # end __init__

    def getSalary(self):
        return self.salary
    # end getSalary

    def getRestDays(self):
        return self.rest_days
    # end getRestDays

# end class Workplace


def buildDefaultWorkplace():
    return Workplace(WORK_X, WORK_Y, WORK_CAPACITY, REST_DAYS, SALARY)
# end buildDefaultWorkplace


def buildWorkplaceRandomDays():
    days = [0, 1, 2, 3, 4, 5, 6]
    day1 = random.choice(days)
    days.remove(day1)
    day2 = random.choice(days)
    return Workplace(WORK_X, WORK_Y, WORK_CAPACITY, [day1, day2], SALARY)
# end buildWorkplaceRandomDays


class GroceriesStore(Location):

    def __init__(self, size_x, size_y, max_capacity, food_price):

        super().__init__(size_x, size_y, max_capacity)
        self.food_price = food_price
    # end __init__

    def buyFood(self, food_qty):
        return self.food_price * food_qty
    # end buyFood

# end class GroceriesStore


def buildDefaultStore():
    return GroceriesStore(STORE_X, STORE_Y, STORE_CAPACITY, FOOD_PRICE)
# end buildDefaultStore


class School (Location):

    def __init__(self, size_x, size_y, max_capacity):

        super().__init__(size_x, size_y, max_capacity)
        self.rest_days = REST_DAYS
    # end __init__

    def getRestDays(self):
        return self.rest_days
    # end getRestDays

# end class School


def buildDefaultSchool():
    return School(SCHOOL_X, SCHOOL_Y, SCHOOL_CAPACITY)
# end buildDefaultStore


class Leisure (Location):

    def __init__(self, size_x, size_y, max_capacity):

        super().__init__(size_x, size_y, max_capacity)
        self.rest_days = REST_DAYS
    # end __init__

# end class Leisure


def buildDefaultLeisure():
    return Leisure(FUN_X, FUN_Y, FUN_CAPACITY)
# end buildDefaultLeisure


def buildDefaultLocation(loc_type):
    if loc_type == HOME:
        return buildDefaultHome()
    elif loc_type == WORKPLACE:
        return buildWorkplaceRandomDays()
    elif loc_type == GROCERIES_STORE:
        return buildDefaultStore()
    elif loc_type == SCHOOL:
        return buildDefaultSchool()
    elif loc_type == LEISURE:
        return buildDefaultLeisure()
    else:
        return None
# end buildDefaultLocation