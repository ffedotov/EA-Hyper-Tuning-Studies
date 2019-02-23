#importing modules
print "------------------------------------------------------------------------------------------"
print "-----------------------HT EA Simulation initialization------------------------------------"
print "------------------------------------------------------------------------------------------"  
import EA_Utilities
import math
import random
import csv
import deap
import argparse
from deap import creator, base, tools, algorithms

print EA_Utilities.TimeStamp()+" Modules have been imported successfully"  

#Hardcoded parameters - input should be based on Random Search and Fitness Reference Table studies
GM=31335 #Global MAximum Value
GOP=0 #Global Optimim value
N=1500 #This value represent the average number of runs that it takes for Random Search to find GOP: this imposes a limit on the number of iterations for EA

#initializing population parameters
parser = argparse.ArgumentParser(description='Start Random Search.')
parser.add_argument('--NI', default=1)
parser.add_argument('--IPO', default=50)
parser.add_argument('--MUT', default='MUF')
parser.add_argument('--CXX', default='C1P')
parser.add_argument('--SEL', default='SLB')
args = parser.parse_args()

NI=args.NI
IPO=args.IPO
MUT=args.MUT
CXX=args.CXX
SEL=args.SEL

Config_Name="Config_"+str(IPO)+"_"+MUT+"_"+CXX+"_"+SEL
toolbox = base.Toolbox()

print EA_Utilities.TimeStamp()+" Global parameters established:"
print "           Global Maximum set at value:        ",GM
print "           Global Optimum Point set at value:  ",GOP 
print "           EA Configuration setting:           ",Config_Name
print "------------------------------------------------------------"
HT_EA_Data=open('HT_EA_'+Config_Name+'.csv',"w") #We write run detail data for each individual config
#HT_EA_Test_Log_=open('HT_EA_Simulation_log.csv',"w")
HT_EA_DataWrite = csv.writer(HT_EA_Data)
HT_EA_DataWrite.writerow([Config_Name,'Crossing Probability','Mutation Probability','Cycle','Generation','n','F_best','n_least'])

print EA_Utilities.TimeStamp(), " Data will be saved in the file: ", Config_Name+".csv"

FitnessList=EA_Utilities.FitnessLoader()
CandidateList=EA_Utilities.CandidateLoader()

print EA_Utilities.TimeStamp()," Fitness reference data is loaded"


creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("attr_int", random.randint, 1, 5)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, 6)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    individual_conv=EA_Utilities.ReducedPoint_convert(individual[0],individual[1],individual[2],individual[3],individual[4],individual[5])
    return FitnessEvaluator(individual_conv, CandidateList, FitnessList),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)

#toolbox.register("select", tools.selTournament, tournsize=3)
#average_result=0

print EA_Utilities.TimeStamp()," Evolution tools initialized"

def FitnessEvaluator(candidate, candidates, valuelist):
 hit=False
 for i in range (0, len(candidates)):
       if candidate==candidates[i]:
           return valuelist[i]
           hit=True
 if hit==False:
       return "Error"

#Initialize population
pop = toolbox.population(IPO) 

print EA_Utilities.TimeStamp()," Population of size: ", len(pop), " is initialized"

#Assign fitnesses
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
fits = [ind.fitness.values[0] for ind in pop]

print EA_Utilities.TimeStamp(), " Fitness Functions have been succesfully assigned to initial population by using Fitness Reference Table"
print "            Accumulated iteration cost is", len(pop),"iterations." 

g = 0
itr=len(pop)
F_best=GM
#baverage_best_value=31335.0
#AVG_F_best=GM
CXPB = -0.1 #Initial crossing probability
MUTPB = -0.1 #Initial Mutation probability
#BCXPB = 0.0
#BMUTPB = 0.0
total_count=0.0

# Begin the evolution
print EA_Utilities.TimeStamp(), "Beginning evolution using configuration setting: ", Config_Name

for CXPB_itr in range (0,11): #Iterating over all crossing probabilities from 0.1 to 1
    CXPB+=0.1 
    MUTPB=-0.1
    for MUTPB_itr in range (0,11): #Iterating over all mutation probabilities from 0.1 to 1
      MUTPB+=0.1 
#      for c in range (0,NI):
#       total_count+=1
#        temp_fits=fits
#        temp_fits = list(map(toolbox.clone, fits))
#        temp_fitnesses = list(map(toolbox.clone, fitnesses))
#        g = 0
#        itr=len(pop)
#        bestvalue=GlobalMax
#        temp_pop = list(map(toolbox.clone, pop))
#        while min(temp_fits) > GlobalMin and itr < 1500:
#        # A new generation
#         g = g + 1    
#         MatingCandidates=tools.selBest(temp_pop, 10, fit_attr='fitness')
#         Candidates = list(map(toolbox.clone, MatingCandidates))
#         for child1, child2 in zip(Candidates[::2], Candidates[1::2]):
#            if random.random() < CXPB:
#                toolbox.mate(child1, child2)
#                del child1.fitness.values
#                del child2.fitness.values
#         for mutant in Candidates:
#                EA_Utilities.mutCreepInt(mutant, -2, 2, MUTPB)
#                del mutant.fitness.values
#         invalid_ind = [ind for ind in Candidates if not ind.fitness.valid]
#         temp_fitnesses = map(toolbox.evaluate, invalid_ind)
#         for ind, fit in zip(invalid_ind, temp_fitnesses):
#            itr+=1
#            ind.fitness.values = fit
#         temp_pop += Candidates
#         
#         temp_fits = [ind.fitness.values[0] for ind in temp_pop]
#         if bestvalue>min(temp_fits):
#           bestvalue=min(temp_fits)
#         HT_EA_writer.writerow([len(pop),len(temp_pop),CXPB,MUTPB,c,g,itr,bestvalue])
#        average_best_value+=bestvalue 
#      print ('Best value: ', average_best_value/100)
#      print ('Population size:',len(pop))
#      print ('Active population size', len(temp_pop))
#      print ('Crossing probability:', CXPB)
#      print ('Mutation probability:', MUTPB)
#      print ('Progress:', (total_count/100), '%')
#      if baverage_best_value>average_best_value/100:
#        baverage_best_value=average_best_value/100
#         BCXPB=CXPB
#         BMUTPB=MUTPB
#      print ('Best value so far: ', baverage_best_value)
#      print ('For CXPB:', BCXPB)
#      print ('For MUTPB:', BMUTPB)
#
#      average_best_value=0.0
      
#HT_EA_output.close()
    

    



   
















