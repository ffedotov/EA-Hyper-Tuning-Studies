#importing modules
import math
import random
import csv
import datetime
from itertools import repeat
from collections import Sequence
dZgap = 10 #Gap
zGap = dZgap / 2  # halflengh of gap
def TimeStamp():
 return "["+datetime.datetime.now().strftime("%H:%M:%S")+"]"
  
def ReducedPoint_convert(a,b,c,d,e,f):
    result_point=[]
    result_point.append(170+(a*5)+zGap)
    result_point.append(170)
    result_point.append(170+(b*5)+zGap)
    result_point.append(207)
    result_point.append(170+(c*5)+zGap)
    result_point.append(248)
    result_point.append(305)
    result_point.append(242)
  
    result_point.append(d*5)
    result_point.append(40)
    result_point.append(150)
    result_point.append(150)
    result_point.append(2)
    result_point.append(2)
    
    result_point.append(80)
    result_point.append(80)
    result_point.append(150)
    result_point.append(150)
    result_point.append(2)
    result_point.append(2)    

    result_point.append(e*5)
    result_point.append(51)
    result_point.append(29)
    result_point.append(46)
    result_point.append(10)
    result_point.append(7)
    
    result_point.append(54)
    result_point.append(38)
    result_point.append(46)
    result_point.append(192)
    result_point.append(14)
    result_point.append(9)  
    
    result_point.append(f*5)
    result_point.append(31)
    result_point.append(35)
    result_point.append(31)
    result_point.append(51)
    result_point.append(11)

    result_point.append(3)
    result_point.append(32)
    result_point.append(54)
    result_point.append(24)
    result_point.append(8)
    result_point.append(8)    
 
    result_point.append(22)
    result_point.append(31)
    result_point.append(209)
    result_point.append(35)
    result_point.append(8)
    result_point.append(13)
     
    result_point.append(33)
    result_point.append(77)
    result_point.append(85)
    result_point.append(241)
    result_point.append(9)
    result_point.append(26) 
    #result_point.append(random.uniform(0.0,20000.0))
    return result_point
    
def GenerateRandomPoint():
    RandPoint=[]
    a=random.randint(1,5)
    b=random.randint(1,5)
    c=random.randint(1,5)
    d=random.randint(1,5)
    e=random.randint(1,5)
    f=random.randint(1,5)               
    return ReducedPoint_convert(a,b,c,d,e,f)

def GenerateRandomReducedPoint():
    RandPoint=[]
    a=random.randint(1,5)
    b=random.randint(1,5)
    c=random.randint(1,5)
    d=random.randint(1,5)
    e=random.randint(1,5)
    f=random.randint(1,5)               
    RandPoint=[a,b,c,d,e,f]
    return RandPoint


def CandidateLoader():
 with open('/home/ffedotov/Documents/PhD/EA_Project/HyperTuning/HT_Fitness_Reference.csv') as csv_cash_file:
    csv_reader_cash = csv.reader(csv_cash_file, delimiter=',')
    veterans=[]
    veteran=[]
    for row in csv_reader_cash:
      for j in range (1,57):
       veteran.append(int(round(float(row[j]))))
      veterans.append(veteran)
      veteran=[]     
    csv_cash_file.close()
 return veterans

def FitnessLoader():
 with open('/home/ffedotov/Documents/PhD/EA_Project/HyperTuning/HT_Fitness_Reference.csv') as csv_cash_file:
    csv_reader_cash = csv.reader(csv_cash_file, delimiter=',')
    FitnessValue=[]
    for row in csv_reader_cash:
     FitnessValue.append(int(round(float(row[57]))))  
    csv_cash_file.close()
 return FitnessValue

def CachingTest(cache, individual):
    for c in range (0, len(cache)):
        if individual==cache[c]:
           return True
           break
    return False

def CachingRead(cache, individual):
    for c in range (0, len(cache)):
        if individual==cache[c]:
           return True
       
def mutCreepInt(individual, low, up, indpb):
    """Mutate an individual by replacing attributes, with probability *indpb*,
    by a integer uniformly drawn between *low* and *up* inclusively.
    
    :param individual: :term:`Sequence <sequence>` individual to be mutated.
    :param low: The lower bound or a :term:`python:sequence` of
                of lower bounds of the range from wich to draw the new
                integer.
    :param up: The upper bound or a :term:`python:sequence` of
               of upper bounds of the range from wich to draw the new
               integer.
    :param indpb: Independent probability for each attribute to be mutated.
    :returns: A tuple of one individual.
    """
    size = len(individual)
    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))
    
    for i, xl, xu in zip(xrange(size), low, up):
        if random.random() < indpb:
            individual[i] = max(1,individual[i]+random.randint(xl, xu))
    
    return individual,
        
    
    

    



   
















