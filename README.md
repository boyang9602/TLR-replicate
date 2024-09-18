# ApolloTLR Python Replication

This is a python / pytorch replication of [Apollo Traffic Light Detection and Recognition (TLR)](https://github.com/ApolloAuto/apollo/blob/v7.0.0/modules/perception/camera/app/traffic_light_camera_perception.h). 

You can install it by `python3 -m pip install -r requirements.txt --user .` You may need to install and configure pytorch with cuda. 

Example code

```python3
from tlr.pipeline import load_pipeline
import cv2
tlr = load_pipeline() # load_pipeline('cuda:0)
valid_detections, recognitions, assignments, invalid_detections = tlr(image, projection_bboxes)
```

Output
1. valid_detections is a n * 9 tensor. The first column is useless in this project. 1:5 are the bounding boxes, 5:9 are the TL type scores vector.
2. recognitions are the recognition scores vector.
3. assignments is a n * 2 tensor. Each row is match between the [projection](https://github.com/ApolloAuto/apollo/blob/v7.0.0/docs/specs/traffic_light.md#pre-process) and the valid detection. The first col is the idx of a projection of TLs and the second col is the idx of a valid detection. 
4. invalid_detections are discarded in Apollo.

Please refer to https://github.com/ApolloAuto/apollo/blob/v7.0.0/docs/specs/traffic_light.md for a high-level understanding of Apollo TLR. 

This project is part of `SITAR: Evaluating the Adversarial Robustness of Traffic Light Recognition in Level-4 Autonomous Driving`. Please consider to cite it if you found it useful. 
```
@INPROCEEDINGS{sitar,
  author={Yang, Bo and Yang, Jinqiu},
  booktitle={2024 IEEE Intelligent Vehicles Symposium (IV)}, 
  title={SITAR: Evaluating the Adversarial Robustness of Traffic Light Recognition in Level-4 Autonomous Driving}, 
  year={2024},
  volume={},
  number={},
  pages={1068-1075},
  keywords={Target tracking;Image recognition;Perturbation methods;Geology;Web and internet services;Object detection;Robustness},
  doi={10.1109/IV55156.2024.10588456}}

```
