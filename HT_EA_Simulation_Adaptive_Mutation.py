#importing modules
print "------------------------------------------------------------------------------------------"
print "-----------------------Hyper Tuning EA studies by Filips Fedotovs-------------------------"
print "------------------------------------------------------------------------------------------"  
import EA_Utilities
import math
import random
import csv
import deap
import argparse
import numpy as np
from deap import creator, base, tools, algorithms
print EA_Utilities.TimeStamp()," Modules have been imported successfully"
#Hardcoded parameters - input should be based on Random Search and Fitness Reference Table (FRT) studies
GM=31335 #Global Maximum Value
GOP=0 #Global Optimim value
N=5812 #This value represent the average number of runs that it takes for Random Search to find GOP: this imposes a limit on the number of iterations for EA
#initializing population parameters to be input by user
parser = argparse.ArgumentParser(description='Enter configuration settings for Evolutionary algorithm')
parser.add_argument('--IPO',help='Enter size of the initial population', default=50)
parser.add_argument('--MUT',help='Enter mutation mode: "MUF" - Uniform, "MCP" - Creep, "MGS" - Gaussian', default='MUF')
parser.add_argument('--CXX', help='Enter recombination mode: "C1P" - One point, "C2P" - Two point, "CUP" - Uniform',default='C1P')
parser.add_argument('--SEL',help='Enter selection mode: "SLB" - Select 10 best, "SLR" - Select 10 random, "SLM" - Select 8 best and 2 random, "SLT" - Tournament', default='SLB')
parser.add_argument('--MUTPB',help='Enter initital mutation probability from 0.1 to 1.0', default='0.5')
parser.add_argument('--CXPB',help='Enter crossing probability from 0.1 to 1.0', default='0.5')
parser.add_argument('--MUTSTR',help='Select mutation variability strategy: MUGAF - Mutation adapts with generation avg Fitness Fuction, MUGBF - Mutation adapts with Mutation adapts with generation best Fitness Fuction ', default='MUGAF')
args = parser.parse_args()
# assign parameters entered by users to particular variables so can be used by EA
IPO=int(args.IPO)
MUT=args.MUT
CXX=args.CXX
SEL=args.SEL
CXPB = args.CXPB #Initial crossing probability
MUTPB = args.MUTPB #Initial Mutation probability

Config_Name="Config_"+str(IPO)+"_"+MUT+"_"+CXX+"_"+SEL+"_"+str(MUTPB)+"_"+str(CXPB)
cache=[] #Cache to store points that have been calculated already: Remember we only "charge" for queriyng RFT. Points can be freely reused.
toolbox = base.Toolbox()
print EA_Utilities.TimeStamp()," Global parameters established:"
print "            Global Maximum set at value:        ",GM
print "            Global Optimum Point set at value:  ",GOP
print "            EA Configuration setting:           ",Config_Name
HT_EA_Data=open('DataDetailedOutput/HT_EA_'+Config_Name+'.csv',"w") #We write run detail data for each individual config
HT_EA_DataWrite = csv.writer(HT_EA_Data)
HT_EA_DataWrite.writerow(['Iterations','Generation','Generation Average Fitness','Generation Best Fitness','Generation Worst Fitness','Population Size','Population Best Fitness'])
print EA_Utilities.TimeStamp(), " Data will be saved in the file:       ", Config_Name+".csv"
FitnessList=EA_Utilities.FitnessLoader() #Loading fitness function values from the FRT
CandidateList=EA_Utilities.CandidateLoader()
print EA_Utilities.TimeStamp()," Fitness reference data is loaded"
creator.create("FitnessMax", base.Fitness, weights=(-1.0,)) #We define the weighting of Fitness reference values: negative value indicates that the best fitness is the smallest one
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("attr_int", random.randint, 1, 5) #Range of values for Reduced space DNA
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, 6) #Specifying length of the DNA for each individual
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#This function evaluates Fitness Function of the given candidate based on FRT
def evalOneMax(individual):
    if EA_Utilities.CachingTest(cache, individual)==False: #Point has not been extracted from FRT before
          cache.append(individual) #Add point to the cash
    individual_conv=EA_Utilities.ReducedPoint_convert(individual[0],individual[1],individual[2],individual[3],individual[4],individual[5])
    #We have to convert points from short representation consisting of 6 integers to the full one consisting of 56
    return FitnessEvaluator(individual_conv, CandidateList, FitnessList), #Return tuple with result
def evalGeneration(individual):
    individual_conv=EA_Utilities.ReducedPoint_convert(individual[0],individual[1],individual[2],individual[3],individual[4],individual[5])
    #We have to convert points from short representation consisting of 6 integers to the full one consisting of 56
    return FitnessEvaluator(individual_conv, CandidateList, FitnessList), #Return tuple with result
toolbox.register("evaluate", evalOneMax) #This tool evaluates population using function evalOneMax()
toolbox.register("evaluate_generation", evalGeneration) #This tool evaluates population using function evalOneMax()
#Defining recombination operators depending on the user input
if CXX=='C1P': #Recombination happens by splitting DNA code of parents in two parts each and exchanging them
   toolbox.register("mate", tools.cxOnePoint)
if CXX=='C2P': #Recombination happens by splitting DNA code of parents in three parts each and exchanging them
   toolbox.register("mate", tools.cxTwoPoint)
if CXX=='CUP': #Unigorm blending
   toolbox.register("mate", tools.cxUniform)
print EA_Utilities.TimeStamp()," Evolution tools initialized"
def FitnessEvaluator(candidate, candidates, valuelist): #This function evaluates fitness of the candidate using existing FRT
 for i in range (0, len(candidates)):
       if candidate==candidates[i]:
           return valuelist[i]
 return 6000 #Has to be fixed, there is a point that fails to be found in FRT
def EvaluationCost(candidates): #This function evaluates cost of evaluating population:
 cost=0
 for i in range (0, len(candidates)):
       if EA_Utilities.CachingTest(cache, candidates[i])==False: #If the point has not been evaluated before it has to be quared in the FRT
          cost+=1
 return cost
n=15625 #Size of the search space
# Begin the evolution
print EA_Utilities.TimeStamp(), " Beginning evolution using configuration setting: ", Config_Name
print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"

cache=[]
#Initialize population - we do it during every cycle to eliminate bias
pop = toolbox.population(IPO)
#Assign fitnesses
itr=EvaluationCost(pop)
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
g = 0 #generation consisting of only initialized population
F_best=GM #The best current value, set by default to the Global Maximum
n_snapshot=itr
snapshot_timer=0
direction=0
while F_best > GOP and itr<N:
    # A new generation
    Avg_Generation_F=0
    Max_Generation_F=0
    Min_Generation_F=0
    Generation=[]
    Temp_pop = list(map(toolbox.clone, pop))
    for ind, fit in zip(Temp_pop, fitnesses):
        ind.fitness.values = fit
        if F_best>fit[0]:
           F_best=fit[0]
           n=itr
    g = g + 1
    snapshot_timer+=1 #Snapshot timer to monitor EA cycle run and stop it if it start stagnating
    if snapshot_timer==1000: #We set 1000 times
           if n_snapshot==itr:
                print EA_Utilities.TimeStamp(), "Evolution has failed: rejecting operation..."
                RejectCycle=True        #Reject cycle
                break
           else:
                snapshot_timer=0
                n_snapshot=itr        #Restart countdown
    if SEL=='SLB': #Choosing different selection procedures based on user settings
         Temp_pop=tools.selBest(Temp_pop, 10, fit_attr='fitness')
    if SEL=='SLT': #Tournament selection
         Temp_pop=tools.selTournament(Temp_pop, 10, 10, fit_attr='fitness')
    if SEL=='SLR':  #Selecting 10 random candidates
         Temp_pop=tools.selRandom(Temp_pop, 10)
    if SEL=='SLM': #Selecting 8 best and 2 random candidates
          BestMatingCandidates=tools.selBest(Temp_pop, 8 , fit_attr='fitness')
          BestMates = list(map(toolbox.clone, BestMatingCandidates))
          RandomMatingCandidates=tools.selRandom(Temp_pop, 2)
          RandomMates = list(map(toolbox.clone, RandomMatingCandidates))
          Temp_pop=BestMates+RandomMates
#Now we can begin the mating
    for child1, child2 in zip(Temp_pop[::2], Temp_pop[1::2]): #Mating selected candidates
          if random.random() < CXPB:  #Mating happens with probability
               toolbox.mate(child1, child2)
    for mutant in Temp_pop: #Mutating based on settings
           if MUT=='MUF':
                 tools.mutUniformInt(mutant, 1, 5, MUTPB)
           if MUT=='MCP':
                 EA_Utilities.mutRsCreepInt(mutant, -1, 1, MUTPB)
           if MUT=='MGS':
                 EA_Utilities.mutRsGaussianInt(mutant, 0.1, MUTPB)
#Now here is the bit: We want to see how generation improves over time. No penalty for querying FRT
    generation_fitness=list(map(toolbox.evaluate_generation, Temp_pop))
    for ind, fit in zip(Temp_pop, generation_fitness):
        ind.fitness.values = fit
        Generation.append(fit[0])
    Avg_Generation_F=sum(Generation)/len(Generation)
    Max_Generation_F=max(Generation)
    Min_Generation_F=min(Generation)
    for ind in Temp_pop: #We don't want to fill our population with identical points
         if EA_Utilities.CachingTest(cache, ind)==False:
              pop.append(ind)
    itr+=EvaluationCost(pop)
    fitnesses = list(map(toolbox.evaluate, pop))
    HT_EA_DataWrite.writerow([itr,g,Avg_Generation_F,Max_Generation_F,Min_Generation_F,len(pop),F_best])
print EA_Utilities.TimeStamp(),"  Best fitness", F_best
print EA_Utilities.TimeStamp(),"  Achieved on iteration", n
print EA_Utilities.TimeStamp(),"  EA simulation completed"
print "------------------------------------------Byee--------------------------------------------"
HT_EA_Data.close()
    

    



   
















