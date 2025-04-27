#!/usr/bin/env python3
"""
Depth-aware privacy blur for crowd-analytics.
Author: Vibelytics (Konstantinos Sevdinoglou)
"""

import argparse
import time
import cv2
import depthai as dai
import numpy as np
import torch

parser = argparse.ArgumentParser()
parser.add_argument("--device", default="cpu", help="cpu | mps | cuda")
parser.add_argument("--source", default=0, help="camera index")
parser.add_argument("--nearest_cm", type=int, default=100,
                    help="pixels < this depth (cm) are blurred")
args = parser.parse_args()

# DepthAI pipeline (RGB + depth)
pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()
depth = pipeline.createStereoDepth()
cam.setPreviewSize(640, 360)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
xout = pipeline.createXLinkOut(); xout.setStreamName("rgb")
dout = pipeline.createXLinkOut(); dout.setStreamName("depth")
cam.preview.link(xout.input)
cam.isp.link(depth.left)
depth.depth.link(dout.input)

with dai.Device(pipeline) as device, \
     device.getOutputQueue("rgb") as rgb_q, \
     device.getOutputQueue("depth") as depth_q:

    while True:
        t0 = time.time()
        rgb = rgb_q.get().getCvFrame()
        d = depth_q.get().getFrame()
        mask = (d < args.nearest_cm*10).astype(np.uint8)  # mm to cm
        mask = cv2.resize(mask, (rgb.shape[1], rgb.shape[0]))
        mask = cv2.GaussianBlur(mask, (99, 99), 0)
        blurred = cv2.GaussianBlur(rgb, (99, 99), 0)
        out = np.where(mask[..., None] > 0, blurred, rgb)
        cv2.imshow("Vibelytics Privacy Blur", out)
        if cv2.waitKey(1) & 0xFF == 27: break
        fps = 1/(time.time()-t0)
        print(f"{fps:0.1f} FPS", end="\r")