#importing libraries
import time
import random
import deap
from deap import creator, base, tools, algorithms
import csv
#Our loss function should be as low as possible
print ('Beginning intialization')
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
Log_output=open('EA_log.csv',"w")
Log_writer = csv.writer(Log_output)

Reduced_output=open('EA_ReducedSpace.csv',"w")
Reduced_writer = csv.writer(Reduced_output)
print('Log created')
Log_writer.writerow(['['+str(time.time())+']: '+'Initialising Log'])
#Initializing some fixed parameters
dZgap = 10 #Gap
zGap = dZgap / 2  # halflengh of gap


#Creating Genetic representation of the Muon Shield configuration
toolbox.register("attr_int1", random.randint, 1, 5)
#toolbox.register("attr_int1", random.randint, 170 + zGap, 300 + zGap)
#toolbox.register("attr_int2", random.randint, 170 + zGap, 300 + zGap)
#toolbox.register("attr_int3", random.randint, 170 + zGap, 300 + zGap)
toolbox.register("attr_int2", random.randint, 1, 5)
#toolbox.register("attr_int4", random.randint, 170 + zGap, 300 + zGap)
#toolbox.register("attr_int5", random.randint, 170 + zGap, 300 + zGap)
toolbox.register("attr_int3", random.randint, 1, 5)
#toolbox.register("attr_int6", random.randint, 170 + zGap, 300 + zGap)
#toolbox.register("attr_int7", random.randint, 170 + zGap, 300 + zGap)
#toolbox.register("attr_int8", random.randint, 170 + zGap, 300 + zGap)
toolbox.register("attr_int4", random.randint, 1, 5)

#toolbox.register("attr_int9", random.randint, 10, 100)
toolbox.register("attr_int5", random.randint, 1, 5)
#toolbox.register("attr_int10", random.randint, 10, 100)
#toolbox.register("attr_int11", random.randint, 20, 200)
#toolbox.register("attr_int12", random.randint, 20, 200)
#toolbox.register("attr_int13", random.randint, 2, 70)
#toolbox.register("attr_int14", random.randint, 2, 70)
#toolbox.register("attr_int15", random.randint, 10, 100)
#toolbox.register("attr_int6", random.randint, 1, 5)
#toolbox.register("attr_int16", random.randint, 10, 100)
#toolbox.register("attr_int17", random.randint, 20, 200)
#toolbox.register("attr_int18", random.randint, 20, 200)
#toolbox.register("attr_int19", random.randint, 2, 70)
#toolbox.register("attr_int20", random.randint, 2, 70)
#toolbox.register("attr_int21", random.randint, 10, 100)
toolbox.register("attr_int6", random.randint, 1, 5)
#toolbox.register("attr_int22", random.randint, 10, 100)
#toolbox.register("attr_int23", random.randint, 20, 200)
#toolbox.register("attr_int24", random.randint, 20, 200)
#toolbox.register("attr_int25", random.randint, 2, 70)
#toolbox.register("attr_int26", random.randint, 2, 70)
#toolbox.register("attr_int27", random.randint, 10, 100)
#toolbox.register("attr_int8", random.randint, 1, 5)
#toolbox.register("attr_int28", random.randint, 10, 100)
#toolbox.register("attr_int29", random.randint, 20, 200)
#toolbox.register("attr_int30", random.randint, 20, 200)
#toolbox.register("attr_int31", random.randint, 2, 70)
#toolbox.register("attr_int32", random.randint, 2, 70)
#toolbox.register("attr_int33", random.randint, 10, 100)
toolbox.register("attr_int7", random.randint, 1, 5)
#toolbox.register("attr_int34", random.randint, 10, 100)
#toolbox.register("attr_int35", random.randint, 20, 200)
#toolbox.register("attr_int36", random.randint, 20, 200)
#toolbox.register("attr_int37", random.randint, 2, 70)
#toolbox.register("attr_int38", random.randint, 2, 70)
#toolbox.register("attr_int39", random.randint, 10, 100)
#toolbox.register("attr_int7", random.randint, 1, 5)
#toolbox.register("attr_int40", random.randint, 10, 100)
#toolbox.register("attr_int41", random.randint, 20, 200)
#toolbox.register("attr_int42", random.randint, 20, 200)
#toolbox.register("attr_int43", random.randint, 2, 70)
#toolbox.register("attr_int44", random.randint, 2, 70)
#toolbox.register("attr_int45", random.randint, 10, 100)
toolbox.register("attr_int8", random.randint, 1, 5)
#toolbox.register("attr_int46", random.randint, 10, 100)
#toolbox.register("attr_int47", random.randint, 20, 200)
#toolbox.register("attr_int48", random.randint, 20, 200)
#toolbox.register("attr_int49", random.randint, 2, 70)
#toolbox.register("attr_int50", random.randint, 2, 70)
#toolbox.register("attr_int51", random.randint, 10, 100)
#toolbox.register("attr_int10", random.randint, 1, 5)
#toolbox.register("attr_int52", random.randint, 10, 100)
#toolbox.register("attr_int53", random.randint, 20, 200)
#toolbox.register("attr_int54", random.randint, 20, 200)
#toolbox.register("attr_int55", random.randint, 2, 70)
#toolbox.register("attr_int56", random.randint, 2, 70)
toolbox.register("individual", tools.initCycle, creator.Individual,
         (toolbox.attr_int1, toolbox.attr_int2, toolbox.attr_int3, toolbox.attr_int4, toolbox.attr_int5, toolbox.attr_int6,
toolbox.attr_int7, toolbox.attr_int8),
          n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

def RF_convert(a,b,c,d,e,f):
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
    
def GenerateReducedSpace():
    for a in range(1,6):
        for b in range(1,6):
           for c in range(1,6):
              for d in range(1,6):
                 for e in range(1,6):
                    for f in range(1,6):
                        Reduced_writer.writerow(RF_convert(a,b,c,d,e,f))

def GenerateReducedFakeSpace():
    for a in range(1,6):
        for b in range(1,6):
           for c in range(1,6):
              for d in range(1,6):
                 for e in range(1,6):
                    for f in range(1,6):
                        Reduced_writer.writerow(RF_convert(a,b,c,d,e,f))

def StripFixedParams(point):
    stripped_point = []
    pos = 0
    for low, high in FIXED_RANGES:
        stripped_point += point[:low-pos]
        point = point[high-pos:]
        pos = high
    _, high = FIXED_RANGES[-1]
    stripped_point += point[high-pos:]
    return stripped_point


#toolbox.register("evaluate", evalOneMax)
#toolbox.register("mate", tools.cxTwoPoint)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
#toolbox.register("select", tools.selTournament, tournsize=3)
#ind1 = toolbox.individual(n=2)

#mutant = toolbox.clone(ind1)
#print (tools.mutUniformInt(mutant, -5, 5, 0.5))
#Mut = tools.mutate(population)
#NGEN=40
#for gen in range(NGEN):
#    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

#    fits = toolbox.map(toolbox.evaluate, offspring)
#    for fit, ind in zip(fits, offspring):
#        ind.fitness.values = fit
#    population = toolbox.select(offspring, k=len(population))
#top10 = tools.selBest(population, k=30)
#print (Mut)
GenerateReducedFakeSpace()
Log_output.close()
Reduced_output.close()
