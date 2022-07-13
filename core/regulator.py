from cmath import inf
import time
import random


class Subject:
    def __init__(self, weight = 0, gravity = 0, resistance = 0, initialPosition = 0, noise = 0, lowerLimit = -inf, upperLimit = inf, multiplier = 1):
        self.weight = weight
        self.momentum = 0
        self.gravity = gravity
        self.resistance = resistance
        self.position = initialPosition
        self.noise = noise
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self.multiplier = multiplier
    
    def reset(self):
        self.momentum = 0
        self.position = 0

    def simulate(self, inputValue):
        if inputValue < -1:
            inputValue = -1
        if inputValue > 1:
            inputValue = 1
        inputValue *= self.multiplier
        self.momentum  = self.momentum * self.resistance
        self.momentum += inputValue / self.weight
        self.momentum += self.gravity
        self.position += self.momentum + random.randint(-self.noise, self.noise)
        if self.position < self.lowerLimit:
            self.position = self.lowerLimit
        elif self.position > self.upperLimit:
            self.position = self.upperLimit

        
class PidRegulator:
    def __init__(self, kp = 1, ki = 0, kd = 0, mi = 0.97):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.mi = mi
        self.error = 0
        self.integral = 0
        self.lastError = 0
    
    def regulate(self, error):
        self.error = error
        self.integral *= self.mi
        self.integral += self.error
        derivative = self.error - self.lastError
        self.lastError = self.error
        result = self.kp * self.error + self.ki * self.integral + self.kd * derivative
        if result > 1:
            result = 1
        if result < -1:
            result = -1
        return result


class AverageFilter:
    def __init__(self, size = 10):
        self.size = size
        self.values = [0 for i in range(size)]
        self.index = 0
    
    def addValue(self, value):
        self.values[self.index] = value
        self.index = (self.index + 1) % self.size
    
    def getAverage(self):
        return sum(self.values) / len(self.values)

    def filter(self, value):
        self.addValue(value)
        return self.getAverage()


class Evaluator:
    def __init__(self, cycles = 100, offset = 1000):
        self.cycles = cycles
        self.offset = offset
        self.results = []
        self.totalRuns = 0
    
    def evaluate(self, subject, regulator, verbose = False):
        self.totalRuns += 1
        self.results.clear()
        subject.reset()
        filter = AverageFilter(size = 10)
        for i in range(self.cycles):
            res = regulator.regulate(self.offset - subject.position)
            res = filter.filter(res)
            subject.simulate(res)
            if verbose:
                print("Step {0: <5}".format(i), "     Regulator result: {0: <5}".format(round(res, 2)), "    Position: {0: <5}".format(round(subject.position, 2)))
            
            if subject.position < self.offset:
                self.results.append((self.offset - subject.position) / self.offset)
            else:
                self.results.append(5 * abs(self.offset - subject.position) / self.offset)
            
            #self.results.append(abs(self.offset - subject.position) / self.offset)
        return sum(self.results) / len(self.results)
    
    def standardDeviation(self):
        return (sum([(x - self.mean()) ** 2 for x in self.results]) / len(self.results)) ** 0.5

    def mean(self):
        return sum(self.results) / len(self.results)

    def median(self):
        return sorted(self.results)[len(self.results) // 2]

    def errorDistribution(self):
        distribution = {}
        for i in range(self.cycles):
            if self.results[i] in distribution:
                distribution[self.results[i]] += 1
            else:
                distribution[self.results[i]] = 1
        return distribution
    
    def errorDistributionNormalized(self):
        distribution = self.errorDistribution()
        total = sum(distribution.values())
        for key in distribution:
            distribution[key] /= total
        return distribution

    def printResult(self):
        print("-----------------------------------------------------")
        print("Report for run no. {0: <5}".format(self.totalRuns))
        print("Error percentage: {0: <5}%".format(round(100 * sum(self.results) / len(self.results), 2)))
        print("Max error: {0: <5}".format(round(max(self.results), 2)))
        print("Min error: {0: <5}".format(round(min(self.results), 2)))
        print("Standard deviation: {0: <5}".format(round(self.standardDeviation(), 2)))
        print("Mean error: {0: <5}".format(round(self.mean(), 2)))
        print("Median error: {0: <5}".format(round(self.median(), 2)))
        #print("Error distribution:", self.errorDistribution())
        #print("Error distribution (normalized):", self.errorDistributionNormalized())
        print("-----------------------------------------------------")



class autoTuner:
    def __init__(self, subject, verbose = False):
        self.subject = subject
        self.verbose = verbose
    
    def tune(self, offset = 1000, steps = 10000):
        
        bestError = inf
        bestKp = 0
        bestKi = 0
        bestKd = 0
    
        evaluator = Evaluator(cycles = 100, offset = 1000)

        print("Autotuner started")
        for kp in range(1, 1000):
            for ki in range(1, 10):
                for kd in range(1, 50):
                    regulator = PidRegulator(kp / 100, ki / 1000, kd / 10)
                    error = evaluator.evaluate(subject, regulator)
                    if error < bestError:
                        bestError = error
                        bestKp = kp / 100
                        bestKi = ki / 1000
                        bestKd = kd / 10

                        print("New record found, time: {0: <5}".format(time.time()))            
                        print("Best error: {0: <5}".format(round(bestError, 8)))
                        print("Best kp: {0: <5}".format(round(bestKp, 8)))
                        print("Best ki: {0: <5}".format(round(bestKi, 8)))
                        print("Best kd: {0: <5}".format(round(bestKd, 8)))
            

        print("Best error: {0: <5}".format(round(bestError, 8)))
        print("Best kp: {0: <5}".format(round(bestKp, 8)))
        print("Best ki: {0: <5}".format(round(bestKi, 8)))
        print("Best kd: {0: <5}".format(round(bestKd, 8)))



if __name__ == "__main__":
    subject = Subject(weight = 1, gravity = -5, resistance = 0.99, initialPosition = 0, noise = 0, lowerLimit = 0, multiplier=10)


    #tuner = autoTuner(subject, verbose = True)
    #tuner.tune()
    #exit()


    regulator = PidRegulator(kp = 0.01, ki = 0, kd = 0.1)
    #regulator2 = PidRegulator(kp = 0.21, ki = 0.003, kd = 3.3)
    #regulator2 = PidRegulator(kp = 0.03, ki = 0.001, kd = 0.1)

    regulator2 = PidRegulator(kp = 0.02, ki = 0.001, kd = 0.8) #Overhaul is punished more
    regulator2 = PidRegulator(kp = 0.04, ki = 0.002, kd = 1.1)

    evaluator = Evaluator(cycles = 100, offset = 1000)

    fitness = evaluator.evaluate(subject, regulator, verbose=True)
    evaluator.printResult()
    fitness = evaluator.evaluate(subject, regulator2, verbose=True)
    evaluator.printResult()
    exit()