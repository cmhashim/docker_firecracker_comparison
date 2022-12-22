# To run 
# python inference.py <audiofile> <number of time to run inference>
# python inference.py 8555-292519-0009.wav 3
import sys
import subprocess
import timeit
import shlex
# total arguments
n = len(sys.argv)
if n==1:
    audiofile ='8555-292519-0009.wav'
    run_times = 1
elif n==2:
    audiofile = sys.argv[1]
    run_times = 1
elif n==3:
    audiofile = sys.argv[1]
    run_times = sys.argv[2]

print('Running inference -',run_times,'time')
result = timeit.timeit('subprocess.run("deepspeech --model ./models/deepspeech-0.9.3-models.pbmm --scorer ./models/deepspeech-0.9.3-models.scorer --audio ./test_audios/"+audiofile, check=True, text=True,  shell=True)',globals=globals(),number=int(run_times))
print('## Time taken for inference of',audiofile,str(run_times),'times -',result)
