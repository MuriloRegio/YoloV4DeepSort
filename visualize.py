import pandas as pd
import numpy as np
import cv2

np.random.seed(42)

# file = '0Ow4cotKOuw_0'
# file = '1Kbw1bUw_1'
# file = '39BFeYnbu-I_0'
file = 'EFv961C5RgY_0'



filename = f"./RWF-2000/val/Fight/{file}.avi"


table = pd.read_csv(f'{file}.tsv', sep='\t')
# print(table.head())

info = dict(zip(list(table['ID'].iloc), [int(x) for x in table['Radius'].iloc]))
COLORS = np.random.randint(0, 255, size=(table.shape[0], 3), dtype="uint8")

alpha = 1
thickness = 1

######
## Display
vid = cv2.VideoCapture(filename)
w = int(vid.get(3))
h = int(vid.get(4))


frame = np.zeros((h, w, 3), dtype=np.uint8)
ret, img = vid.read()

for ts in range(1, table.shape[1]-1):
	col = f'Instant {ts}'

	ret, img = vid.read()
	if ret != True:
		break

	for i in range(table.shape[0]):
		center = table[col].iloc[i]
		if str(center) == 'nan':
			continue
		center = tuple(int(x) for x in eval(center))

		radius = int(info[table['ID'].iloc[i]]*alpha)
		color  = tuple([int(x) for x in COLORS[i]])

		# cv2.circle(frame, center, 1, color, 5)
		cv2.circle(  img, center, radius, color, thickness)

	img = cv2.bitwise_or(img, frame)

	cv2.imshow('Tracer Analyzer', img)
	if cv2.waitKey(60) & 0xFF == ord('q'):
		break
vid.release()
######
