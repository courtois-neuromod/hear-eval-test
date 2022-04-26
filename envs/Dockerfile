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
# NUMBA cache dir needs to be writable https://stackoverflow.com/questions/59290386/runtimeerror-at-cannot-cache-function-shear-dense-no-locator-available-fo
ENV NUMBA_CACHE_DIR=/tmp
# deterministic cuBLAS https://docs.nvidia.com/cuda/cublas/index.html#cublasApi_reproducibility
ENV CUBLAS_WORKSPACE_CONFIG=:4096:8

RUN useradd --create-home --shell /bin/bash jovyan
USER jovyan
WORKDIR /soundnetbrain_hear