FROM hear-eval-kit:latest

USER root
RUN mkdir /soundnetbrain_hear
COPY . /soundnetbrain_hear/
WORKDIR /soundnetbrain_hear
RUN python3 -m pip install -r requirements.txt

RUN useradd --create-home --shell /bin/bash jovyan
USER jovyan
WORKDIR /home/jovyan