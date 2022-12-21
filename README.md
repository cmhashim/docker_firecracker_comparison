# Performance analysis of Docker and Firecracker running ML inferences

## Objective

- [x] To deploy a ML inference on a **Firecracker VM**.
- [x] To deploy same ML inference model using **Docker**.
- [x] Compare the performance of the ML inference model in **Docker** and **Firecracker**.

# 1. Docker
## 1.1 Build a Docker Image
To build a Docker image, a base image is necessary, onto which all the required dependencies and libraries can be installed. We  intend to deploy a DeepSpeech ASR model, that can transcribe a given audio file. A base image, Python:3.9 and other required libraries and files are specified in the Dockerfile to build the image. 

The contents of the Dockerfile is listed below


```
FROM python:3.9

RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz && \
   tar -zxvf audio-0.9.3.tar.gz && \
   rm audio-0.9.3.tar.gz
RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/models_0.9.tar.gz && \
   tar -zxvf models_0.9.tar.gz && \
   rm models_0.9.tar.gz
COPY . /

RUN pip3 install deepspeech

# to run deepspeech:
CMD deepspeech --model ./models/deepspeech-0.9.3-models.pbmm --scorer ./models/deepspeech-0.9.3-models.scorer --audio ./audio/4507-16021-0012.wav
```

Once Dockerfile is created, run the following commands from the same directory, naming the docker image as ds:1.2


```
sudo docker build -t ds:1.2 .
```
## 1.2 Start Docker Container

Once the Docker image is created, you can check the list of images that can be used by Docker to run the containers using the command

```
sudo docker images
```
The Docker container is created using these docker images. There are two ways to run a container, either using the `run` or `create` and `start` commands. 
To create and start the container, use the command

```
sudo docker run ds:1.2
```

To only create a container, and not starting it , use

```
sudo docker create ds:1.2
```

To start already created containers, (use the container id from `sudo docker ps -a`)

```
sudo docker start <container-id>
```
## 1.3 Running ASR Inference

* To run a container and get into interactive bash 

```
sudo docker run -it --entrypoint bash --rm ds:1.2
```
Restrict the resources to be used for running the container using the command

```
sudo docker run -m 2GB --cpus 2.0 -it --entrypoint bash --rm ds:1.2

```

* Once inside the container, you can run deepspeech for any audio files inside the directory `/test-audios` using the command

```
deepspeech --model ./models/deepspeech-0.9.3-models.pbmm --scorer ./models/deepspeech-0.9.3-models.scorer --audio ./test_audios/8555-292519-0009.wav 
```

or run the file `inference.py` specifying the audio file and number time to run the inference

```
python inference.py 8555-292519-0009.wav 2
```


To exit from the container, type `exit`



# 2. Firecracker
## 2.1 Create a firecracker VM
Ignite supports OCI images to run as a firecracker VM. The docker image is saved and imported to be used as ignite images 

```
sudo docker save ds:1.1 | sudo ctr -n firecracker image import -
sudo ignite image import ds:1.1
```

The firecracker vm can be created with specific reousrces defined during the command
```
sudo ignite run ds:1.0 --cpus 2 --memory 2GB --ssh --name my-vm
```
This method actually uses ignite to boot up the imported docker image as the firecracker VM

Once VM is started, you can get into the terminal
```
sudo ignite attach my-vm
```
The deepspeech is already installed and can be used to perform inference. `mount proc /proc -t proc` is set before running the inference.

Any running Vm's can be killed and removed using `sudo ignite rm my-vm`

## 2.2 Running ASR inference

* To run the Firecracker VM, 

```
sudo ignite run ds:1.2 --cpus 2 --memory 2GB  --name my-vm 
```

* Once inside the VM, you can run deepspeech for any audio files inside the directory `/test-audios` using the command

```
deepspeech --model ./models/deepspeech-0.9.3-models.pbmm --scorer ./models/deepspeech-0.9.3-models.scorer --audio ./test_audios/8555-292519-0009.wav 
```

or run the file `inference.py` specifying the audio file and number time to run the inference

```
python inference.py 8555-292519-0009.wav 2
```
or run the file `inference_all.py` with number time to run the inference of all the audios in dir `test_audios`

```
python inference_all.py 3
```


To exit from the container, type `exit`


# 3 Performance Analysis

**No.**         | **Task**           | **Details**     | **Docker** | **Firecracker** 
----------------|-----------------------------|--------------------------|---------------------|--------------------------
 1              | **Import time**                 | import deepspeech        | 0.411s              | **0.142s**              
 2              | **Single instance inference**   | time deepspeech ...      | 11.526s             | -                        
 2              | (8555-292519-0009.wav)      | model load time          | **0.012s**         | 0.186s                   
 2              | (17.965s)                   | inference time           | **8.452s**        | 57.445s                  
 3              | **Single instance inference-1** | python inference.py      | 101.257s            | **79.801s**             
 3              | (1221-135766-0010.wav)      | model load time          | **0.012s**         | 0.015s                   
 3              | (15.050s)                   | inference time           | 32.663s             | **19.246s**             
 3              | **Single instance inference-2** | model load time          | 0.021s              | **0.014s**            
 3              | (1221-135766-0010.wav)      | inference time           | 7.294s              | **6.412s**             
 3              | **Single instance inference **   | model load time          | avg **0.012s**    | avg 0.015s               
 3              |  (3rd-10th time)            | inference time           | avg 7.158s          | avg **6.418s**         
 4              | **Multiple instance inference** | python inference\_all.py | 256.818s            | **202.987s**           
 4              | (12 audios)                 | model load time          | avg **0.012s**     | avg 0.015s               
 5              | **Multiple instance inference** | python inference\_all.py | 438.088s            | **376.980s**           
 5              | (12 audios, 3 times)        | model load time          | avg **0.012s**      | avg 0.015s               

## Whats Next ?

* Run different ML frameworks to compare performance effectively.
* Deploy ML model with web application in Docker and firecracker VM in AWS EC2 instance.
* Run multiple applications or overload to benchmark the bottleneck of Docker and Firecracker VM.
* Use Prometheus to monitor the resource utilization and visualization using Grafana can be done.
* Deloy a ML model on Nvidia Jetson and compare the performances.ep




