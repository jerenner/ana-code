import os

run_number = [7878, 7879, 7880, 7881, 7882,
              7883,  7889, 7890, 7891,7892,
              7893, 7894, 7895, 7896, 7897, 
              7898, 7899, 7901, 
              7949, 7950, 7951, 7952]

f = open('./to_run.sh','w')


for run in run_number:
    print(run)
    f.write(f'python ana.py -c config/config_{run}.cnf')
    f.write('\n')

f.close()
    
