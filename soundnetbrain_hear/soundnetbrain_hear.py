import os
import numpy as np
from torch import load, device
import torch
from .model import SoundNetEncoding_conv
from torchaudio.transforms import Resample



def load_model(model_file_path, device=None):
    if device is None:
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    modeldict = load(model_file_path, map_location=device)

    model = SoundNetEncoding_conv(out_size=modeldict['out_size'],output_layer=modeldict['output_layer'],
    kernel_size=modeldict['kernel_size'])

    # Set model weights using checkpoint file
    model.load_state_dict(modeldict['checkpoint'])

    model = model.to(device)
    model.sample_rate = 48000  # Input sample rate
    model.scene_embedding_size = 1024
    model.timestamp_embedding_size = 128

    return model


def get_scene_embeddings(x, model):
    device = x.device
    resampling = Resample(48000, 22000).to(device)
    
    x = resampling(x)
    audio_length = x.shape[1]
    batch_size = x.shape[0]
    minimum_length = 32000
    
    x = x.reshape(batch_size, 1,audio_length,1)

    if audio_length < minimum_length:
        
        
        x = torch.cat((x, torch.zeros(batch_size, 1,minimum_length - audio_length,1).to(device)), dim=2)

    with torch.no_grad():
        model.eval()
        Y,outputlist = model.soundnet.extract_feat(x,'conv7')
    
    Y=Y[:,:,0]
    
    conv7 = torch.mean(Y,axis=2)
    return conv7


def get_timestamp_embeddings(x, model):
    device = x.device
    resampling = Resample(48000, 22000).to(device)
    x = resampling(x)
    audio_length = x.shape[1]
    batch_size = x.shape[0]
    minimum_length = 32000


    x = x.reshape(batch_size, 1,audio_length,1)

    if audio_length < minimum_length:
        batch_size = x.shape[0]
        
        x = torch.cat((x, torch.zeros(batch_size, 1,minimum_length - audio_length,1).to(device)), dim=2)

    with torch.no_grad():
        model.eval()
        Y,outputlist = model.soundnet.extract_feat(x,'conv4')
    
    embs=Y[:,:,:,0].swapaxes(1,2)

    batch_size, frames_num, embedding_size = embs.shape

    ### perio and offset were estimated using soundnet architecture, taking into account paddings, strides and maxpool
    offset = 0.03345455 * 1000
    perio = 1000 / 24.55357142857143
    nframes_neg = 5
    nframes_end = 1
    time_steps = (torch.arange(frames_num-nframes_neg-nframes_end)[None, :] * perio) + offset    # (frames_num,)
    time_steps = time_steps.repeat(batch_size, 1)   # (batch_size, frames_num)
    
    
    return embs[:,nframes_neg:-nframes_end,:],time_steps