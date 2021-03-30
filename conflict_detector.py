import pandas as pd
import numpy as np
import math
import cv2

np.random.seed(42)


if __name__ == "__main__":
	file = '0Ow4cotKOuw_0'
	groundtruth = 'Fight'


expand_ratio = 1.0 ## Alpha








within_degree = lambda dgr, target : dgr <= target or dgr >= (360-target)


def intersection_type(c1, r1, c2, r2):
	x1, y1 = c1
	x2, y2 = c2

	d = ((x2-x1)**2 + (y2-y1)**2)

	if d > (r1+r2)**2:
		return 0
	if d < (r1-r2)**2:
		return -1
	return 1





def find_conflict(table):
	global info
	info = dict(zip(list(table['ID'].iloc), [int(x) for x in table['Radius'].iloc]))

	_id = lambda x : table['ID'].iloc[x]

	def get(row, ts):
		t = f'Instant {ts}'

		c = table[t].iloc[row]
		if str(c) == 'nan':
			return None, None
		c = tuple(int(x) for x in eval(c))

		r = int(info[_id(row)]*expand_ratio)

		return c, r

	def getVector(row, ts):
		c1, _ = get(row, ts)
		c2, _ = get(row, ts-1)

		if c1 is None or c2 is None:
			return (0,0)

		vec = np.asarray([c1[0]-c2[0], c1[1]-c2[1]])
		return vec / np.linalg.norm(vec)



	old = {}
	frames_with_conflict = []
	
	for ts in range(table.shape[1]-3):
		ts += 2
		AoC = {} ## Areas of Conflict

		for i in range(table.shape[0]-1):
			c1, r1 = get(i, ts)
			v1 = getVector(i, ts)

			if c1 is None:
				continue

			for j in range(i+1, table.shape[0]):
				c2, r2 = get(j, ts)
				v2 = getVector(j, ts)
				key = tuple([i,j])

				if c2 is None:
					continue

				if max([r1,r2])* 2/3 > min([r1,r2]):
					continue


				intersects = intersection_type(c1, r1, c2, r2)

				if not intersects:
					continue

				if intersects == -1 and key in old:
					AoC[key] = -1
					continue

				
				vd = np.asarray([c1[0]-c2[0], c1[1]-c2[1]])
				vd = vd / np.linalg.norm(vd)

				d1 = np.dot(v1, vd)
				d2 = np.dot(v2, vd)

				a1 = math.degrees(np.arccos(d1))
				a2 = math.degrees(np.arccos(d2))

				if within_degree(a1, 22) or within_degree(a2, 22) or key in old:
					AoC[key] = 1
					old[key] = 1

		if len(list(AoC)):
			frames_with_conflict.append(ts)

	return table.shape[1]-3, len(frames_with_conflict)
	### Returns amount of analyzed frames x amount of frames with potential conflict


if __name__ == '__main__':
	filename = f"./RWF-2000/val/{groundtruth}/{file}.avi"


	Table = pd.read_csv(f'{file}.tsv', sep='\t')
	print (find_conflict(Table))