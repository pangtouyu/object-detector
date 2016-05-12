#!/usr/bin/env python

import csv
import pprint


def overlapping_area(detection_1, detection_2):

    # x-y co-ordinates of the rectangles
    x1_tl = detection_1[0]
    x1_br = detection_1[0] + detection_1[2]
    y1_tl = detection_1[1]
    y1_br = detection_1[1] + detection_1[3]

    x2_tl = detection_2[0]
    x2_br = detection_2[0] + detection_2[2]
    y2_tl = detection_2[1]
    y2_br = detection_2[1] + detection_2[3]

    # overlap area
    x_overlap = max(0, min(x1_br, x2_br)-max(x1_tl, x2_tl))
    y_overlap = max(0, min(y1_br, y2_br)-max(y1_tl, y2_tl))
    overlap_area = x_overlap * y_overlap

    area_1 = detection_1[2] * detection_1[3]
    area_2 = detection_2[2] * detection_2[3]
    total_area = area_1 + area_2 - overlap_area
    return overlap_area / float(total_area)


def nms(detections, threshold=.5):

    if len(detections) == 0:
        return []

    #  Sort detections based on confidence score
    detections.sort(key=lambda detections: detections[4], reverse=True)

    new_detections = []
    new_detections.append(detections.pop(0))

    while detections:

        # pprint.pprint(detections)
        # print '*'*50

        detection = detections.pop(0)
        for new_detection in new_detections:
            # For each detection, calculate the overlapping area
            if overlapping_area(detection, new_detection) > threshold:
                break  # great overlap --> pop next entry
        else:
            # when overlap area is less than threshold
            # append 'detection' to 'new_detections'
            new_detections.append(detection)

    return new_detections


def test_nms():

    detections = []

    with open('coords.csv') as f, open('nms_output.csv', 'wb') as o:

        reader = csv.reader(f, delimiter=',')
        for row in reader:
            detections.append([float(val) for val in row])

        nms_output = nms(detections)

        writer = csv.writer(o, delimiter=',')
        print "NMS Detections:"
        for row in nms_output:
            orow = map(int, row[:4])
            orow.append(row[4])
            writer.writerow(orow)
            print "{}".format(orow)


if __name__ == "__main__":

    # test_nms()

    # Example of how to use the NMS Module
    detections = [[31, 31, 10, 10, 0.9], [31, 31, 10, 10, .12], [100, 34, 10, 10, .8]]
    print "Detections before NMS = {}".format(detections)
    print "Detections after NMS = {}".format(nms(detections))
