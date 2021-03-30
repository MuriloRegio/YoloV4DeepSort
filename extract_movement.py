import numpy as np
np.random.seed(42)

import warnings
warnings.filterwarnings('ignore')


import yolo as yolov4
yolo = yolov4.YOLO()

import cv2

from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet

import os
from io import StringIO
import pandas as pd

if __name__ == '__main__':
	filename = "0Ow4cotKOuw_0"
	groundtruth = 'Fight'




model_filename = 'weights/mars-small128.pb'
encoder = gdet.create_box_encoder(model_filename,batch_size=1)

sep = '\t'
import time
def main(filename, metrics=False):
	movement = {}
	ids = {}

	max_cosine_distance = 0.5

	metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance)
	tracker = Tracker(metric)

	video_capture = cv2.VideoCapture(filename)

	ts = 0
	total_time = 0

	while True:
		ts += 1

		ret, frame = video_capture.read()
		if ret != True:
			break

		movement[ts] = {}
		
		ti = time.time()
		boxs,_ = yolo.detect_image(frame)
		total_time += time.time() - ti

		features = encoder(frame,boxs)
		detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]

		ti = time.time()
		tracker.predict()
		tracker.update(detections)

		for track in tracker.tracks:
			if not track.is_confirmed() or track.time_since_update > 1:
				continue
				
			# bbox = track.to_tlbr()
			tx,ty,w,h = track.to_tlwh()
			center = (int(tx + w/2), int(ty + h/2))
			
			_id = track.track_id
			movement[ts][_id] = center
			
			if _id not in ids:
				ids[_id] = []
			ids[_id].append(w)
		total_time += time.time() - ti
		# print (time.time() - ti)


	video_capture.release()

	if metrics:
		return movement, ids, total_time

	return movement, ids


def toDataframe(move_hist, obj_ids):
	timestamps = sorted(list(move_hist.keys()))

	txt_data = []
	for _id in list(obj_ids):
		row = [str(_id), str((sum(obj_ids[_id])/len(obj_ids[_id]))//2)]
		
		for instant_ts in timestamps:
			instant = move_hist[instant_ts]

			if _id in instant:
				row.append('({}, {})'.format(*instant[_id]))
			else:
				row.append('')

		txt_data.append(sep.join(row))

	tabledata = StringIO(
		sep.join(
			['ID', 'Radius']
			+ 
			[f'Instant {i}' for i in timestamps]
		)
		+
		'\n'
		+
		'\n'.join(txt_data)
	)

	return pd.read_csv(tabledata, sep=sep)



def interpolate(table):
	for row in range(table.shape[0]):
		nan   = 0
		start = 0

		for col in range(2, table.shape[1]):
			p = table.iloc[row,col]

			if str(p) == 'nan':
				nan += 1
				continue

			if not start:
				start = 1
				nan = 0
				continue

			if nan > 1:
				last = table.iloc[row, col-nan-1]

				p1 = tuple(int(x) for x in eval(p))
				p2 = tuple(int(x) for x in eval(last))

				diff = tuple(abs(p1[i]-p2[i])/nan for i in range(2))

				for k in range(1, nan):
					pn = tuple(p2[i]+k*diff[i] for i in range(2))
					table.iloc[row,col-nan+k-1] = str(pn)

			nan = 0


if __name__ == '__main__':
	filename = f"./RWF-2000/val/{groundtruth}/{filename}.avi"
	move_hist, obj_ids = main(filename)

	file = os.path.splitext(os.path.basename(filename))[0]
	table = toDataframe(move_hist, obj_ids)

	interpolate(table)

	table.to_csv(file+'.tsv', sep=sep, index=False)
