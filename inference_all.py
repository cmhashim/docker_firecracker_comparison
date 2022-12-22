# To run 
# python inference_all.py <number of time to run inference>
import sys
import subprocess
import timeit
import shlex
import os


# total arguments
n = len(sys.argv)
if n==1:
    run_times = 1
elif n==2:
    run_times = sys.argv[1]
total_time=0.0

print('Running inference -',run_times,'time')

dirname = './test_audios/'
for i in range(int(run_times)):
    print('## Running inference -',i+1,'of',run_times,'time')
    for files in os.listdir(dirname):
        if files.endswith('.wav'):
            temp = timeit.timeit('subprocess.run("deepspeech --model ./models/deepspeech-0.9.3-models.pbmm --scorer ./models/deepspeech-0.9.3-models.scorer --audio ./test_audios/"+files, check=True, text=True, shell=True)',globals=globals(),number=1)
            print('## Time taken for inference of',files,temp)
            total_time+=temp
        else:
            continue
print('#### Time taken for inference of 12 audio files -',str(run_times),'times -',total_time)
