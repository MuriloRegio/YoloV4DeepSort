# Violence Detector

This project sought to identify fights in surveillance footage by using low-cost methods.

### Dependencies

Python 3.8+

    NumPy
    Pandas
    sklean
    OpenCV
    Pillow
    TensorFlow >= 2

### Installation

This repository uses a TensorFlow 2.x compatible version of the one proposed by https://github.com/Qidian213/deep_sort_yolov3.

* Weight Files
	* Download the YOLOv4 and DeepSORT weights

		[mars-small128.pb](https://drive.google.com/drive/folders/1m2ebLHB2JThZC8vWGDYEKGsevLssSkjo)<br>
		[yolov4.weights](https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT)

* Environment Setup
	* Clone and compile YOLOv4 from https://github.com/AlexeyAB/darknet
	* Copy the files `darknet` and `libdarknet.so` to this project's folder
	* Place the `mars-small128.pb` and `yolov4.weights` into a `weights` folder

* Dataset
	* Extract the *RWF-2000* dataset into this folder
	* Alternatively edit file `run_all.py` to change the path used



### Running


#### Evaluating

Running the `run_all.py` script will create an output table

| File | Ground Truth | #Frames | #Frames with Fights Detected |
|:----:|:------------:|:-------:|:----------------------------:|
| ... | ... | ... | ... |

Running then the script `plot.py` will process output tables
and create comparison graphs.

These tables can also be loaded by the [Facets app](https://pair-code.github.io/facets/).


#### Running Individual Videos

By editing the paths at the start of files `extract_movement.py` and `conflict_detector.py` , one can
first run the `extract_movement.py` script to create a table, registering the position of each person
during the video. 

By then running the `conflict_detector.py` script, one can see how many frames are there in the video
and how many of those contain potential fight scenes. Also, the tables loaded for this script can also
be loaded by the `visualize.py` script, which displays the video while showing the personal space of
each person detected.