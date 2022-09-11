import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
import matplotlib.pyplot as plt

# GUI backend so we can draw the images
matplotlib.use('TkAgg')

# enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

IMAGE_PATHS = [
    './images/intersection.jpeg',
    './images/traffic.jpeg',
    './images/jungle.jpeg',
    './images/walkingdog.jpeg'
]

PATH_TO_MODEL_DIR = './models/ssd_resnet50_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03'
PATH_TO_LABELS = './labels/mscoco_complete_label_map.pbtxt'
PATH_TO_SAVED_MODEL = os.path.join(PATH_TO_MODEL_DIR, 'saved_model')

print(f'Loading model from {PATH_TO_SAVED_MODEL}...')

# load the saved model and build the detection function
model = tf.saved_model.load(PATH_TO_SAVED_MODEL)
detect_fn = model.signatures['serving_default']

print('Model loaded successfully')

# load the labels into a category index
print(f'Loading labels from {PATH_TO_LABELS}')
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)


def detect_objects(image):
    # convert the np array into a tensor
    input_tensor = tf.convert_to_tensor(image)

    # this gives us a single tensor but we need to feed the network with an array of
    # tensors so we have to add a new axis
    input_tensor = input_tensor[tf.newaxis, ...]

    # do the detections
    detections = detect_fn(input_tensor)

    # remove the additional structure needed for image batches
    for key in detections:
        detections[key] = detections[key][0, ...]

    # num_detections can be cast to an int
    detections['num_detections'] = int(detections['num_detections'])

    return detections


image = Image.open(IMAGE_PATHS[3])
image_data = np.array(image)
detected_objects = detect_objects(image_data)
print(f'Found objects:\n{detected_objects}')

SCORE_CUTOFF = 0.45

for i in range(detected_objects['num_detections']):
    detection_score = float(detected_objects['detection_scores'][i])
    if detection_score >= SCORE_CUTOFF:
        detection_box = detected_objects['detection_boxes'][i]
        class_index = int(detected_objects['detection_classes'][i])
        class_name = category_index[class_index]['name']
        viz_utils.draw_bounding_box_on_image_array(
            image_data, detection_box[0], detection_box[1], detection_box[2], detection_box[3],
            color=viz_utils.STANDARD_COLORS[class_index % len(viz_utils.STANDARD_COLORS)],
            display_str_list=[class_name],
            use_normalized_coordinates=True)

plt.title(f"Image with {detected_objects['num_detections']} found")
plt.imshow(image_data)
plt.show()
