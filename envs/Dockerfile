FROM hear-eval-kit:latest

USER root
RUN mkdir /soundnetbrain_hear
COPY . /soundnetbrain_hear/
RUN rm -rf /soundnetbrain_hear/models/*
RUN rm -rf /soundnetbrain_hear/data/*
RUN rm -rf /soundnetbrain_hear/logs/*
RUN rm -rf /soundnetbrain_hear/embeddings/*
RUN rm -rf /soundnetbrain_hear/envs/hear-eval-kit

WORKDIR /soundnetbrain_hear
RUN python3 -m pip install -r requirements.txt

RUN useradd --create-home --shell /bin/bash jovyan
USER jovyan