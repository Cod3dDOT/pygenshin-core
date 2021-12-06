import numpy
import cv2
import math

from numpy.core.records import array

from pygenshin.modules.additional_types import PYGenshinException, Rect, Vector2


def isInsideBounds(coordinates, bounds) -> bool:
    return not (coordinates[0] < bounds[0][0] or coordinates[0] > bounds[1][0] or coordinates[1] > bounds[0][1] or coordinates[1] < bounds[1][1])


def featureMatching(data, template, threshold=0.7):
    MIN_MATCH_COUNT = 10
    # Initiate SIFT detector
    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(data, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < threshold * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        src_pts = numpy.float32(
            [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = numpy.float32(
            [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h, w = template.shape
        pts = numpy.float32([[0, 0], [0, h-1], [w-1, h-1],
                            [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
    else:
        print("Not enough matches are found - %d/%d" %
              (len(good), MIN_MATCH_COUNT))

    np_o = numpy.int32(dst)
    bounds = [[np_o[1][0][0], np_o[1][0][1]], [np_o[3][0][0], np_o[3][0][1]]]

    # cv2.rectangle(data, bounds[0], bounds[1], (255, 0, 0), 10)
    # scale_percent = 10
    # width = int(data.shape[1] * scale_percent / 100)
    # height = int(data.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # img2 = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
    # cv2.imshow("", img2)
    # cv2.waitKey(0)

    return bounds


def non_max_suppression(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = numpy.argsort(y2)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = numpy.maximum(x1[i], x1[idxs[:last]])
        yy1 = numpy.maximum(y1[i], y1[idxs[:last]])
        xx2 = numpy.minimum(x2[i], x2[idxs[:last]])
        yy2 = numpy.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = numpy.maximum(0, xx2 - xx1 + 1)
        h = numpy.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = numpy.delete(idxs, numpy.concatenate(([last],
                                                     numpy.where(overlap > overlapThresh)[0])))
    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")


def allMatches(data, templates, threshold=0.8):
    data_gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    results = []
    for template in templates:
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        w, h = template_gray.shape[::-1]
        result = cv2.matchTemplate(
            data_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        loc = numpy.where(result >= threshold)
        points = zip(*loc[::-1])
        rects = [(point[0], point[1], point[0] + w, point[1] + h)
                 for point in points]
        rects = non_max_suppression(numpy.array(rects), 0.1)
        results.append(rects)
    return results


def bestMatches(data, templates, threshold=0.8):
    data_gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)

    results = []
    for template in templates:
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(
            data_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        if (maxVal > threshold):
            results.append(maxLoc)
        else:
            results.append([])

    return results


def distanceBetweenPoints(x1, y1, x2, y2) -> float:
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


def getImageSize(image) -> Vector2:
    return Vector2.fromTuple(image[:-1][::-1])


def cropImage(original, bounds: Rect):
    if (not isinstance(bounds, Rect)):
        raise PYGenshinException(
            "bounds must be of type Rect")

    return original[bounds.start.y + bounds.GetDimensions().y, bounds.start.x + bounds.GetDimensions().x]
