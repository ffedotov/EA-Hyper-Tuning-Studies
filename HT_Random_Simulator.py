print "------------------------------------------------------------------------------------------"
print "-----------------------HT Random Search Simulation initialization-------------------------"
print "------------------------------------------------------------------------------------------"  

#importing modules
import math
import random
import csv
import EA_Utilities
import argparse
print EA_Utilities.TimeStamp()+" Modules have been imported successfully"

#initializing parser variables
parser = argparse.ArgumentParser(description='Start Random Search.')
parser.add_argument('--cycle', default=None)
args = parser.parse_args()
HT_Random_output=open('HT_Random_Simulation_Data.csv',"w")
#HT_Random_Log=open('HT_Random_Simulation_Log.csv',"w")
HT_Random_writer = csv.writer(HT_Random_output)
#HT_Random_Log_Writer = csv.writer(HT_Random_Log)
HT_Random_writer.writerow(['Cycle','Iteration','F_best'])
#HT_Random_Log_Writer.writerow(['Cycle','Step','Point','F_curr','Iteration','F_best'])
print EA_Utilities.TimeStamp(), "Data will be saved in the file: HT_Random_Simulation_Data.csv"
#initializing global variables
best_results=[]
GOP=0
GM=31335
F_best=GM
F_curr=GM
Max_Itr=0
Max_Itrs=[]

print EA_Utilities.TimeStamp()+" Global parameters established:"
print "           Global Maximum set at value:        ",GM
print "           Global Optimum Point set at value:  ",GOP 

for c in range (0,int(args.cycle)):
 t=0
 i=0
 itr=0
 #We set this parameter manually depending on the data subset
 F_best=GM
 candidates=EA_Utilities.CandidateLoader()
 cache=[]
 Max_Itr=0
 Step=0
 F_curr=GM
 
 print EA_Utilities.TimeStamp()+" Beginning evaluation cycle "+str(c)
 print EA_Utilities.TimeStamp(), "Progress  : ", int((c*100/int(args.cycle))),"%"
 print "--------------------------------------------------------------"
 while F_best > GOP and itr <= 15625: 
    Step+=1
    candidate=EA_Utilities.GenerateRandomPoint()
#Testing whether the point is in the cache
#Cache query is free, but querying FRT cost iteration
    if EA_Utilities.CachingTest(cache, candidate)==False:
      cache.append(candidate)
      itr+=1
      t+=1
      for i in range (0, len(candidates)):
        if candidate==candidates[i]:
          if F_best>EA_Utilities.FitnessLoader()[i]:
             F_best=EA_Utilities.FitnessLoader()[i]
             best_point=candidate
          F_curr=EA_Utilities.FitnessLoader()[i]
#      HT_Random_Log_Writer.writerow([c,Step,candidate,F_curr,itr,F_best])
      HT_Random_writer.writerow([c,itr,F_best])
      if F_best==GOP: 
        print EA_Utilities.TimeStamp()+" Success at " + str(itr)
        Max_Itrs.append(itr)
        print EA_Utilities.TimeStamp()+" Average result so far: ", sum(Max_Itrs)/len(Max_Itrs)
        continue  
      if (t==500):
          print EA_Utilities.TimeStamp()+" "+str(itr)+" iterations completed"
          print EA_Utilities.TimeStamp()+" "+"Best result: "+ str(F_best)
          print "-------------------"
          t=0
          continue
    else:
        continue
HT_Random_output.close()
print EA_Utilities.TimeStamp()+" Evaluation ended"
print EA_Utilities.TimeStamp()+" Average result: ", sum(Max_Itrs)/len(Max_Itrs)
print "------------------------------------------------------------------------"
print "-------------------------------Byee-------------------------------------"
      

        

    
    

    




















