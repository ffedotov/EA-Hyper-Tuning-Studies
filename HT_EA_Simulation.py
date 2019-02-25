#importing modules
print "------------------------------------------------------------------------------------------"
print "-----------------------HT EA Simulation by Filips Fedotovs--------------------------------"
print "------------------------------------------------------------------------------------------"  
import EA_Utilities
import math
import random
import csv
import deap
import argparse
from deap import creator, base, tools, algorithms

print EA_Utilities.TimeStamp()+" Modules have been imported successfully"  

#Hardcoded parameters - input should be based on Random Search and Fitness Reference Table (FRT) studies
GM=31335 #Global Maximum Value
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


IPO=int(args.IPO)
NI=int(args.NI)
MUT=args.MUT
CXX=args.CXX
SEL=args.SEL

Config_Name="Config_"+str(IPO)+"_"+MUT+"_"+CXX+"_"+SEL
toolbox = base.Toolbox()

print EA_Utilities.TimeStamp()+" Global parameters established:"
print "           Global Maximum set at value:        ",GM
print "           Global Optimum Point set at value:  ",GOP 
print "           EA Configuration setting:           ",Config_Name
HT_EA_Data=open('HT_EA_'+Config_Name+'.csv',"w") #We write run detail data for each individual config
#HT_EA_Test_Log_=open('HT_EA_Simulation_log.csv',"w")
HT_EA_DataWrite = csv.writer(HT_EA_Data)
HT_EA_DataWrite.writerow([Config_Name,'Crossing Probability','Mutation Probability','Cycle','Generation','n','F_best','n_least'])

print EA_Utilities.TimeStamp(), " Data will be saved in the file: ", Config_Name+".csv"

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
    individual_conv=EA_Utilities.ReducedPoint_convert(individual[0],individual[1],individual[2],individual[3],individual[4],individual[5])
    return FitnessEvaluator(individual_conv, CandidateList, FitnessList),

toolbox.register("evaluate", evalOneMax)
#Defining recombination operators depending on the user input
if CXX=='C1P':
   toolbox.register("mate", tools.cxOnePoint)
if CXX=='C2P':
   toolbox.register("mate", tools.cxTwoPoint)
if CXX=='CUP':
   toolbox.register("mate", tools.cxUniform)
 
#toolbox.register("select", tools.selTournament, tournsize=3)
#average_result=0

print EA_Utilities.TimeStamp()," Evolution tools initialized"

def FitnessEvaluator(candidate, candidates, valuelist): #This function evaluates fitness of the candidate using existing FRT
 for i in range (0, len(candidates)):
       if candidate==candidates[i]:
           return valuelist[i]
 return 6000 #Has to be fixed, there is a point that fails to be found in FRT




g = 0 #initial generation
itr=0 #We have invested some iterations in order to evaluate initial population
F_best=GM
AVG_F_best=GM
TOT_F_best=[]
n=15625
CXPB = 0.1 #Initial crossing probability
MUTPB = 0.0 #Initial Mutation probability

# Begin the evolution
print EA_Utilities.TimeStamp(), " Beginning evolution using configuration setting: ", Config_Name
print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
for CXPB_itr in range (0,10): #Iterating over all crossing probabilities from 0.1 to 1
    CXPB_itr+=1
    MUTPB=0.0
    for MUTPB_itr in range (0,11): #Iterating over all mutation probabilities from 0.1 to 1
      MUTPB_itr+=1
      AVG_F_best=0
      TOT_F_best=[]
      AVG_n_best=0
      TOT_n_best=[]
      for c in range (0,NI):
        itr=0
        #Initialize population - we do it during every cycle to eliminate bias
        pop = toolbox.population(IPO)
#        print EA_Utilities.TimeStamp()," Population of size: ", len(pop), " is initialized"
        #Assign fitnesses
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
         ind.fitness.values = fit
         itr+=1
        fits = [ind.fitness.values[0] for ind in pop]
#        print EA_Utilities.TimeStamp(), " Fitness Functions have been succesfully assigned to initial population by using Fitness Reference Table"
#        print "            Accumulated iteration cost is", itr,"iterations."
        Temp_Fitness_Values = list(map(toolbox.clone, fits)) #Cloning fitness values so we don't change original values
        Temp_Fitnesses = list(map(toolbox.clone, fitnesses))
#        print "Fitness Values", Temp_Fitness_Values
#        print "Fitnesses", Temp_Fitnesses
        g = 0
        F_best=GM
        Temp_pop = list(map(toolbox.clone, pop))
        while F_best > GOP and itr < N:
        # A new generation
         g = g + 1
         if SEL=='SLB': #Chosing different selection procedures based on user settings
          MatingCandidates=tools.selBest(Temp_pop, 10, fit_attr='fitness')
          Mates = list(map(toolbox.clone, MatingCandidates))
         if SEL=='SLT':
          MatingCandidates=tools.selTournament(Temp_pop, 10, 5, fit_attr='fitness')
          Mates = list(map(toolbox.clone, MatingCandidates))
         if SEL=='SLR':
          MatingCandidates=tools.selRandom(Temp_pop, 10)
          Mates = list(map(toolbox.clone, MatingCandidates))
         if SEL=='SLM':
          BestMatingCandidates=tools.selBest(Temp_pop, 8 , fit_attr='fitness')
          BestMates = list(map(toolbox.clone, BestMatingCandidates))
          RandomMatingCandidates=tools.selRandom(Temp_pop, 2)
          RandomMates = list(map(toolbox.clone, RandomMatingCandidates))
          Mates=BestMates+RandomMates
         for child1, child2 in zip(Mates[::2], Mates[1::2]): #Mating selected candidates
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values  #Delete children fitness values
                del child2.fitness.values
         for mutant in Mates: #Mutating based on settings
            if MUT=='MUF':
                 tools.mutUniformInt(mutant, 1, 5, MUTPB)
            if MUT=='MCP':
                 EA_Utilities.mutRsCreepInt(mutant, -1, 1, MUTPB)
            if MUT=='MGS':
                 EA_Utilities.mutRsGaussianInt(mutant, 0.1, MUTPB)
         del mutant.fitness.values
         invalid_ind = [ind for ind in Mates if not ind.fitness.valid]
         Temp_Fitnesses = map(toolbox.evaluate, invalid_ind)
         for ind, fit in zip(invalid_ind, Temp_Fitnesses):
            itr+=1
            ind.fitness.values = fit
         Temp_pop += Mates
         Temp_fits = [ind.fitness.values[0] for ind in Temp_pop]
         if F_best>min(Temp_fits):
           F_best=min(Temp_fits)
           n=itr
         HT_EA_DataWrite.writerow([Config_Name,CXPB,MUTPB,c,g,itr,F_best,n])
        AVG_F_best+=F_best
        TOT_F_best.append(F_best)
        AVG_n_best+=n
        TOT_n_best.append(n)
        #print EA_Utilities.TimeStamp(),"Cycle", c, "out of", NI
        #print EA_Utilities.TimeStamp(),"Best fitness", F_best
        #print EA_Utilities.TimeStamp(),"Achieved on iteration", n
        #print "----------------"
      print EA_Utilities.TimeStamp(),"Progress:", (CXPB_itr*MUTPB_itr), "%"
      print EA_Utilities.TimeStamp(),"Crossing probability", CXPB
      print EA_Utilities.TimeStamp(),"Mutation probability", MUTPB
      print EA_Utilities.TimeStamp(),"Average best fitness", AVG_F_best/len(TOT_F_best)
      print EA_Utilities.TimeStamp(),"Average lowest number of iterations", AVG_n_best/len(TOT_n_best)
      print EA_Utilities.TimeStamp(),"----------------------------------------"
      MUTPB+=0.1
    CXPB+=0.1
print EA_Utilities.TimeStamp(),"  EA simulation completed"
print "------------------------------------------Byee--------------------------------------------"
HT_EA_Data.close()
    

    



   
















