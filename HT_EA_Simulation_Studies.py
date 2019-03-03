#importing modules
print ('HT EA Simulation initialization')  
import EA_Utilities
import math
import random
import csv
import deap
import datetime

from deap import creator, base, tools, algorithms

print EA_Utilities.TimeStamp()," Modules imported successfully"  


#initializing population parameters

GlobalMax=31335
GlobalMin=0
toolbox = base.Toolbox()

print ('Initialized global parameters, Global optimum is at value:', GlobalMax)  

HT_EA_output=open('HT_EA_Simulation_log.csv',"w")
HT_EA_writer = csv.writer(HT_EA_output)
HT_EA_writer.writerow(['Population','Active Population','Crossing Probability','Mutation Probability','Cycle','Generation','Cpu Cost','Best Result'])

print ('Created log output')

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("attr_int", random.randint, 1, 5)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, 6)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)



FitnessList=EA_Utilities.FitnessLoader()
CandidateList=EA_Utilities.CandidateLoader()

print ('Fitness reference data is loaded')

def evalOneMax(individual):
    individual_conv=EA_Utilities.ReducedPoint_convert(individual[0],individual[1],individual[2],individual[3],individual[4],individual[5])
    return FitnessEvaluator(individual_conv, CandidateList, FitnessList),
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
average_result=0

print ('Evolution tools initialized')

def FitnessEvaluator(candidate, candidates, valuelist):
 hit=False
 for i in range (0, len(candidates)):
       if candidate==candidates[i]:
           return valuelist[i]
           hit=True
 if hit==False:
       return 666

#Initialize population
pop = toolbox.population(n=100)

print ('Population of size: ',len(pop), ' is initialized') 

#Assign fitnesses
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
fits = [ind.fitness.values[0] for ind in pop]

print ('Population', len(pop))
      
MUTPB = 0.5



# Begin the evolution
temp_fits=fits
temp_fits = list(map(toolbox.clone, fits))
temp_fitnesses = list(map(toolbox.clone, fitnesses))
temp_pop = list(map(toolbox.clone, pop))
print ("Poulation", temp_pop)
MatingCandidates=tools.selTournament(temp_pop, 20, 10, fit_attr='fitness')
print ('Best   ', MatingCandidates)
for mutant in MatingCandidates:
    EA_Utilities.mutRsGaussianInt(mutant, 0.1, MUTPB)
    del mutant.fitness.values
print ('Mutated', MatingCandidates)
invalid_ind = [ind for ind in MatingCandidates if not ind.fitness.valid]
temp_fitnesses = map(toolbox.evaluate, invalid_ind)
for ind, fit in zip(invalid_ind, temp_fitnesses):
         ind.fitness.values = fit     
temp_fits = [ind.fitness.values[0] for ind in temp_pop]
    
 

    

    



   
















