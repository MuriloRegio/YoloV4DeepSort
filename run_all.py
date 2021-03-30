import extract_movement
import conflict_detector


import os
import time

folder = 'RWF-2000/val'
sep = ','

print ('\n\n\n')
data = []

total_fps = 0

for class_id, sub_folder in enumerate(sorted(os.listdir(folder), reverse=True)):
	sub_folder = os.path.join(folder, sub_folder)

	for file in os.listdir(sub_folder):
		print ('\n')
		path = os.path.join(sub_folder, file)

		move_hist, obj_ids, proc_time = extract_movement.main(path, metrics=True)

		t0 = time.time()
		table = extract_movement.toDataframe(move_hist, obj_ids)
		extract_movement.interpolate(table)

		n_frames, n_conflicts = conflictDetector.find_conflict(table)
		t1 = time.time()

		fps = round((n_frames+1)/(proc_time+(t1-t0)),2)
		print ('FPS:', fps)
		total_fps += fps
		
		data.append(sep.join([str(x) for x in [file, class_id, n_frames, n_conflicts]]))

print('Avg FPS:', round(total_fps/400, 2))

with open('new_results.csv', 'w') as outfile:
	outfile.write('\n'.join(data))