FROM python:3.9

RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz && \
   tar -zxvf audio-0.9.3.tar.gz && \
   rm audio-0.9.3.tar.gz
RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/models_0.9.tar.gz && \
   tar -zxvf models_0.9.tar.gz && \
   rm models_0.9.tar.gz

RUN pip3 install deepspeech

# to run deepspeech:
CMD deepspeech --model ./models/deepspeech-0.9.3-models.pbmm --scorer ./models/deepspeech-0.9.3-models.scorer --audio ./audio/4507-16021-0012.wav

CMD deepspeech --model ./models/deepspeech-0.9.3-models.pbmm --scorer ./models/deepspeech-0.9.3-models.scorer --audio ./audio/2830-3980-0043.wav
