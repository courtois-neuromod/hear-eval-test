import torch, warnings
import torch.nn as nn
# from nistats import hemodynamic_models
import numpy as np

#adapted from https://github.com/smallflyingpig/SoundNet_Pytorch

class SoundNet8_pytorch(nn.Module):
    def __init__(self):
        super(SoundNet8_pytorch, self).__init__()
        
        self.define_module()
        self.indexes= {"conv1" : 0, "pool1" : 1, "conv2" : 2, "pool2" : 3, "conv3" : 4, "conv4" : 5, 
                        "conv5" : 6, "pool5" : 7, "conv6" : 8, "conv7" : 9, "conv8" : 10} 
        self.layers = [self.conv1, self.pool1, self.conv2, self.pool2, self.conv3, self.conv4, 
                        self.conv5, self.pool5, self.conv6, self.conv7, (self.conv8, self.conv8_2)]
        self.layers_size = {"conv1" : 16, "pool1" : 16, "conv2" : 32, "pool2" : 32, "conv3" : 64, "conv4" : 128,
                            "conv5" : 256, "pool5" : 256, "conv6" : 512, "conv7" : 1024, "conv8" : 1000, "conv8_2" : 401} 
        
    def define_module(self):
        self.conv1 = nn.Sequential(
            nn.Conv2d(1,16, (64,1), (2,1), (32,0), bias=True),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True)
        )
        self.pool1 = nn.MaxPool2d((8,1),(8,1))

        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, (32,1), (2,1), (16,0), bias=True),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )
        self.pool2 = nn.MaxPool2d((8,1),(8,1))

        self.conv3 = nn.Sequential(
            nn.Conv2d(32, 64, (16,1), (2,1), (8,0), bias=True),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(64, 128, (8,1), (2,1), (4,0), bias=True),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
        )
        self.conv5 = nn.Sequential(
            nn.Conv2d(128, 256, (4,1),(2,1),(2,0), bias=True),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True)
        )
        self.pool5 = nn.MaxPool2d((4,1),(4,1))

        self.conv6 = nn.Sequential(
            nn.Conv2d(256, 512, (4,1), (2,1), (2,0), bias=True),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True)
        )
        self.conv7 = nn.Sequential(
            nn.Conv2d(512, 1024, (4,1), (2,1), (2,0), bias=True),
            nn.BatchNorm2d(1024),
            nn.ReLU(inplace=True)
        )
        self.conv8 = nn.Sequential(
            nn.Conv2d(1024, 1000, (8,1), (2,1), (0,0), bias=True),
        ) 
        self.conv8_2 = nn.Sequential(
            nn.Conv2d(1024, 401, (8,1), (2,1), (0,0), bias=True)
        )

    def forward(self, x, output_layer = "conv8", train_start = None):
        warnings.filterwarnings("ignore")
        
        train_start_index = self.indexes[train_start] if train_start != None else self.indexes["conv8"]
        #train_start_index is the index of the FIRST layer to be trained, 
        # if train_start == None --> transfer learning without finetuning
        output_index = self.indexes[output_layer] if output_layer != "conv8" else self.indexes["conv7"]
        
        with torch.no_grad(): 
            for net in self.layers[:train_start_index]:
                x = net(x)
        for net in self.layers[train_start_index:output_index+1]: #+1 to include the output layer, otherwise it will give you the output of the previous layer
            x = net(x) 

        #-------WIP : See if we can include conv8 and conv8_2 in the loop torch.no_grad before ? Has it really interest ?
        if output_layer == "conv8":
            object_pred = self.conv8(x)
            scene_pred = self.conv8_2(x)
            return (object_pred, scene_pred)
        else :  
            return x
        #----------------------END-WIP----------------

    def extract_feat(self,x:torch.Tensor, output = "conv8")->dict:
        output_list = {}
        for (layer_name, index), net in zip(self.indexes.items(), self.layers):
    
            if layer_name != "conv8" : 
                x = net(x)
                output_list[layer_name] = x.detach().cpu().numpy()
            elif layer_name == "conv8" : 
                object_pred = self.conv8(x)
                output_list["conv8"] = object_pred.detach().cpu().numpy()
                scene_pred = self.conv8_2(x) 
                output_list["conv8"] = scene_pred.detach().cpu().numpy()
            
            if layer_name == output:
                return (x, output_list)


#change start_finetuning in function of epoch n°
 
class SoundNetEncoding_conv(nn.Module):
    def __init__(self, out_size, output_layer, fmrihidden=1000, kernel_size = 1, 
                train_start = None, epoch_start=None, nroi_attention=None, power_transform=False, hrf_model=None, 
                oversampling = 16, tr = 1.49, audiopad = 0, pytorch_param_path = None):
        super(SoundNetEncoding_conv, self).__init__()

        self.soundnet = SoundNet8_pytorch()
        self.fmrihidden = fmrihidden
        self.out_size = out_size
        self.train_start = train_start
        self.epoch_start = epoch_start
        self.output_layer = output_layer
        self.layers_features = {}
        self.power_transform = power_transform

        if pytorch_param_path is not None:
            print("Loading SoundNet weights...")
            # load pretrained weights of original soundnet model
            self.soundnet.load_state_dict(torch.load(pytorch_param_path))
        
        self.encoding_fmri = nn.Conv1d(self.soundnet.layers_size[output_layer],self.out_size,
                                        kernel_size=(kernel_size,1), padding=(kernel_size-1,0))
        print('shape of encoding matrice from last encoding layer : {} X {}'.format(self.soundnet.layers_size[output_layer], self.out_size))
        #nn.init.kaiming_normal_(self.encoding_fmri, mode='fan_in', nonlinearity='relu')
        
        if nroi_attention is not None:
            self.maskattention = torch.nn.Parameter(torch.rand(out_size,nroi_attention))
        else:
            self.maskattention = None
        
        if hrf_model is not None : 
            self.hrf_model = hrf_model
            self.oversampling = oversampling
            self.audiopad = audiopad
            self.tr = tr
        else :
            self.hrf_model=None

    def forward(self, x, epoch):        
        if self.epoch_start == None or epoch < self.epoch_start:
            emb = self.soundnet(x, self.output_layer)
        else : 
            emb = self.soundnet(x, self.output_layer, self.train_start)
        emb = torch.sqrt(emb) if self.power_transform else emb
        out = self.encoding_fmri(emb)
        return out
    
    def extract_feat(self,x:torch.Tensor)->dict:
        (x, output_list) = self.soundnet.extract_feat(x=x, output=output_layer)

        if self.power_transform:
            x = torch.sqrt(x)
            output_list['power_transform'] = x.detach().cpu().numpy()

        x = self.encoding_fmri(x)
        output_list['encoding_layer'] = x.detach().cpu().numpy()
 
        return (x, output_list)
