import numpy as np
### Conv2d in out kernel stride padding
### Input frequency : 22000
### after conv1 : same size, 11000

### Max pool : 1375

### after conv2 : 687.5

## Max pool  : 85.9

## after conv3 : 42.9

## after conv4 : 21.45

## after conv5 : 10.725

## POOL4 : 2.68

## after conv6 : 1.34

## after conv7 : 0.67 Hz

## after fmri encoding : 0.67 Hz

## after conv8 : 0.335 Hz

## Hear benchmark recommends to return embeddings at least every 50 ms, which corresponds to a frequency of 20 Hz. So, embeddings of Conv4 would be fine. 



def timestamps(timestamps_in,padding):
    ### assuming regular spacing
    perio = timestamps_in[1] - timestamps_in[0]

    ### padding is applied to the beginning and end

    ## calculate the sequence of intervals for padding
    pad = np.arange(1,padding+1) * perio

    ## negative one 
    pad_m = -pad

    ## positive one 
    pad_p = pad + timestamps_in[-1]

    return list(np.flip(pad_m)) + list(timestamps_in) + list(pad_p)

def striding(timestamps_in,val):
    return np.take(timestamps_in,np.arange(0,len(timestamps_in),val),mode='wrap')

def conv_pad_stride_pool(timestamps_in,padding,stride,pool):
    t_conv = timestamps(timestamps_in,padding)
    t_strided = striding(t_conv,stride)
    return striding(t_strided,pool)



#### timings at each layer 

#### input : 22000 Hz, 32 padding before -> 

sr=22000
period = 1/sr

### input signal : lsec is length in seconds 
lsec = 10
X = np.arange(0,lsec,period)

## out conv 1

X_conv1 = conv_pad_stride_pool(X,32,2,8)

## out conv 2 

X_conv2 = conv_pad_stride_pool(X_conv1,16,2,8)

## out conv 3

X_conv3 = conv_pad_stride_pool(X_conv2,8,2,1)

## out conv 4

X_conv4 = conv_pad_stride_pool(X_conv3,4,2,1)

## out conv 5

X_conv5 = conv_pad_stride_pool(X_conv4,2,2,4)

## out conv 6

X_conv6 = conv_pad_stride_pool(X_conv5,2,2,1)

## out conv 7

X_conv7 = conv_pad_stride_pool(X_conv6,2,2,1)


print(X.shape,X_conv1.shape,X_conv2.shape,X_conv3.shape,X_conv4.shape,X_conv5.shape,X_conv6.shape,X_conv7.shape)


print(X_conv5)


## Hear benchmark recommends to return embeddings at least every 50 ms, which corresponds to a frequency of 20 Hz. So, embeddings of Conv4 would be fine. 
