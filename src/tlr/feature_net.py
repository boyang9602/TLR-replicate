import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvBNScale(nn.Module):
    """
    This is a very common sub-structure in apollo's network: Convolution -> BatchNorm -> Scale.
    Note that there are inconsistencies between the Caffe's BatchNorm and standard BatchNorm. 
    Caffe's BatchNorm ->  Scale is similar to BatchNorm in PyTorch https://github.com/BVLC/caffe/blob/master/include/caffe/layers/batch_norm_layer.hpp#L28.
    Besides, Caffe's BatchNorm has an extra parameter called moving_average_fraction. The solution to handle this is in https://stackoverflow.com/questions/55644109/how-to-convert-batchnorm-weight-of-caffe-to-pytorch-bathnorm. 
    """
    def __init__(self, in_channels, out_channels, kernel_size, padding, stride, dilation=1, bias=False):
        super().__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, padding=padding, stride=stride, dilation=dilation, bias=bias)
        self.bn   = nn.BatchNorm2d(num_features=out_channels, affine=False)
        self.gamma = nn.Parameter(torch.FloatTensor(out_channels))
        self.beta  = nn.Parameter(torch.FloatTensor(out_channels))
    
    def forward(self, input):
        return self.bn(self.conv(input)) * self.gamma[None, :, None, None] + self.beta[None, :, None, None]

class FeatureNet(nn.Module):
    """
    This is the model to extract features from the image. I made it a separate network and used it in the TLDetector below.
    It is based on ResNet I think.
    """
    def __init__(self):
        super().__init__()
        self.conv1 = ConvBNScale(in_channels=3, out_channels=16, kernel_size=7, padding=3, stride=2)
        self.res2a_branch1 = ConvBNScale(in_channels=16, out_channels=16, kernel_size=1, padding=0, stride=1)
        self.res2a_branch2a = ConvBNScale(in_channels=16, out_channels=16, kernel_size=3, padding=1, stride=1)
        self.res2a_branch2b = ConvBNScale(in_channels=16, out_channels=16, kernel_size=3, padding=1, stride=1)
        self.res2b_branch2a = ConvBNScale(in_channels=16, out_channels=16, kernel_size=3, padding=1, stride=1)
        self.res2b_branch2b = ConvBNScale(in_channels=16, out_channels=16, kernel_size=3, padding=1, stride=1)
        self.res2c_branch2a = ConvBNScale(in_channels=16, out_channels=16, kernel_size=3, padding=1, stride=1)
        self.res2c_branch2b = ConvBNScale(in_channels=16, out_channels=16, kernel_size=3, padding=1, stride=1)
        self.res3a_branch1 = ConvBNScale(in_channels=16, out_channels=32, kernel_size=1, padding=0, stride=2)
        self.res3a_branch2a = ConvBNScale(in_channels=16, out_channels=32, kernel_size=3, padding=1, stride=2)
        self.res3a_branch2b = ConvBNScale(in_channels=32, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.res3b_branch2a = ConvBNScale(in_channels=32, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.res3b_branch2b = ConvBNScale(in_channels=32, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.res3c_branch2a = ConvBNScale(in_channels=32, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.res3c_branch2b = ConvBNScale(in_channels=32, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.res3d_branch2a = ConvBNScale(in_channels=32, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.res3d_branch2b = ConvBNScale(in_channels=32, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.res4a_branch1 = ConvBNScale(in_channels=32, out_channels=64, kernel_size=1, padding=0, stride=2)
        self.res4a_branch2a = ConvBNScale(in_channels=32, out_channels=64, kernel_size=3, padding=1, stride=2)
        self.res4a_branch2b = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4b_branch2a = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4b_branch2b = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4c_branch2a = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4c_branch2b = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4d_branch2a = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4d_branch2b = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4e_branch2a = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4e_branch2b = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4f_branch2a = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res4f_branch2b = ConvBNScale(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.res5a_branch1 = ConvBNScale(in_channels=64, out_channels=128, kernel_size=1, padding=0, stride=1)
        self.res5a_branch2a = ConvBNScale(in_channels=64, out_channels=128, kernel_size=3, padding=1, stride=1)
        self.res5a_branch2b = ConvBNScale(in_channels=128, out_channels=128, kernel_size=3, padding=2, dilation=2, stride=1)
        self.res5b_branch2a = ConvBNScale(in_channels=128, out_channels=128, kernel_size=3, padding=2, dilation=2, stride=1)
        self.res5b_branch2b = ConvBNScale(in_channels=128, out_channels=128, kernel_size=3, padding=2, dilation=2, stride=1)
        self.res5c_branch2a = ConvBNScale(in_channels=128, out_channels=128, kernel_size=3, padding=2, dilation=2, stride=1)
        self.res5c_branch2b = ConvBNScale(in_channels=128, out_channels=128, kernel_size=3, padding=2, dilation=2, stride=1)
        self.rpn_deconv = nn.ConvTranspose2d(in_channels=64, out_channels=256, kernel_size=4, padding=1, dilation=1, stride=2, bias=True)
        self.rpn_cls_score = nn.Conv2d(in_channels=256, out_channels=30, kernel_size=1, padding=0, dilation=1, stride=1, bias=True)
        self.rpn_bbox_pred = nn.Conv2d(in_channels=256, out_channels=60, kernel_size=1, padding=0, dilation=1, stride=1, bias=True)
        self.conv_new = nn.ConvTranspose2d(in_channels=128, out_channels=128, kernel_size=4, padding=1, stride=2, dilation=1, bias=True)
        self.conv_left_kx1 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(9, 1), padding=(4, 0), stride=(1, 1), dilation=(1, 1), bias=True)
        self.conv_left_1xk = nn.Conv2d(in_channels=128, out_channels=490, kernel_size=(1, 9), padding=(0, 4), stride=(1, 1), dilation=(1, 1), bias=True)
        self.conv_right_1xk = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(1, 9), padding=(0, 4), stride=(1, 1,), dilation=(1, 1), bias=True)
        self.conv_right_kx1 = nn.Conv2d(in_channels=128, out_channels=490, kernel_size=(9, 1), padding=(4, 0), stride=(1, 1,), dilation=(1, 1,), bias=True)
    def forward(self, x):
        pool1 = F.max_pool2d(F.relu(self.conv1(x)), kernel_size=3, padding=1, stride=2) # round_mode = 1
        res2a_branch1 = self.res2a_branch1(pool1)
        res2a_branch2a = F.relu(self.res2a_branch2a(pool1))
        res2a_branch2b = self.res2a_branch2b(res2a_branch2a)
        res2a = F.relu(res2a_branch1 + res2a_branch2b)
        res2b_branch2a = F.relu(self.res2b_branch2a(res2a))
        res2b_branch2b = self.res2b_branch2b(res2b_branch2a)
        res2b = F.relu(res2a + res2b_branch2b)
        res2c_branch2a = F.relu(self.res2c_branch2a(res2b))
        res2c_branch2b = self.res2c_branch2b(res2c_branch2a)
        res2c = F.relu(res2b + res2c_branch2b)
        res3a_branch1 = self.res3a_branch1(res2c)
        res3a_branch2a = F.relu(self.res3a_branch2a(res2c))
        res3a_branch2b = self.res3a_branch2b(res3a_branch2a)
        res3a = F.relu(res3a_branch1 + res3a_branch2b)
        res3b_branch2a = F.relu(self.res3b_branch2a(res3a))
        res3b_branch2b = self.res3b_branch2b(res3b_branch2a)
        res3b = F.relu(res3a + res3b_branch2b)
        res3c_branch2a = F.relu(self.res3c_branch2a(res3b))
        res3c_branch2b = self.res3c_branch2b(res3c_branch2a)
        res3c = F.relu(res3b + res3c_branch2b)
        res3d_branch2a = F.relu(self.res3d_branch2a(res3c))
        res3d_branch2b = self.res3d_branch2b(res3d_branch2a)
        res3d = F.relu(res3c + res3d_branch2b)
        res4a_branch1 = self.res4a_branch1(res3d)
        res4a_branch2a = F.relu(self.res4a_branch2a(res3d))
        res4a_branch2b = self.res4a_branch2b(res4a_branch2a)
        res4a = F.relu(res4a_branch1 + res4a_branch2b)
        res4b_branch2a = F.relu(self.res4b_branch2a(res4a))
        res4b_branch2b = self.res4b_branch2b(res4b_branch2a)
        res4b = F.relu(res4a + res4b_branch2b)
        res4c_branch2a = F.relu(self.res4c_branch2a(res4b))
        res4c_branch2b = self.res4c_branch2b(res4c_branch2a)
        res4c = F.relu(res4b + res4c_branch2b)
        res4d_branch2a = F.relu(self.res4d_branch2a(res4c))
        res4d_branch2b = self.res4d_branch2b(res4d_branch2a)
        res4d = F.relu(res4c + res4d_branch2b)
        res4e_branch2a = F.relu(self.res4e_branch2a(res4d))
        res4e_branch2b = self.res4e_branch2b(res4e_branch2a)
        res4e = F.relu(res4d + res4e_branch2b)
        res4f_branch2a = F.relu(self.res4f_branch2a(res4e))
        res4f_branch2b = self.res4f_branch2b(res4f_branch2a)
        res4f = F.relu(res4e + res4f_branch2b)
        res5a_branch1 = self.res5a_branch1(res4f)
        res5a_branch2a = F.relu(self.res5a_branch2a(res4f))
        res5a_branch2b = self.res5a_branch2b(res5a_branch2a)
        res5a = F.relu(res5a_branch1 + res5a_branch2b)
        res5b_branch2a = F.relu(self.res5b_branch2a(res5a))
        res5b_branch2b = self.res5b_branch2b(res5b_branch2a)
        res5b = F.relu(res5a + res5b_branch2b)
        res5c_branch2a = F.relu(self.res5c_branch2a(res5b))
        res5c_branch2b = self.res5c_branch2b(res5c_branch2a)
        res5c = F.relu(res5b + res5c_branch2b)
        rpn_output = F.relu(self.rpn_deconv(res4f))
        rpn_cls_score = self.rpn_cls_score(rpn_output)
        rpn_bbox_pred = self.rpn_bbox_pred(rpn_output)
        rpn_cls_prob = F.softmax(rpn_cls_score.reshape(rpn_cls_score.shape[0], 2, -1, rpn_cls_score.shape[3]), dim=1)
        rpn_cls_prob_reshape = rpn_cls_prob.reshape(rpn_cls_prob.shape[0], 30, -1, rpn_cls_prob.shape[3])
        conv_new = F.relu(self.conv_new(res5c))
        conv_left_kx1 = F.relu(self.conv_left_kx1(conv_new))
        conv_left_1xk = F.relu(self.conv_left_1xk(conv_left_kx1))
        conv_right_1xk = F.relu(self.conv_right_1xk(conv_new))
        conv_right_kx1 = F.relu(self.conv_right_kx1(conv_right_1xk))
        ft_add_left_right = conv_left_1xk + conv_right_kx1
        return rpn_cls_prob_reshape, rpn_bbox_pred, ft_add_left_right
