class Interval:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, hour):
        return self.start <= hour <= self.end

# end Interval

class Activity(Interval):

    def __init__(self, start, end, activity):
        super().__init__(start, end)
        self.activity = activity

# end Activity

class Fork(Interval):

    def __init__(self, start, end, branches):
        super().__init__(start, end)
        self.branches = branches
    
# end Activity

class Branch:

    def __init__(self, prob_funct, value = 1, flags = [], activities = []):
        self.prob_funct = prob_funct
        self.value = value
        self.flags = flags
        self.activities = activities

    def tryChoice(self, data): #TODO: implement flags
        return self.prob_funct(data, self.value)

# end Branch