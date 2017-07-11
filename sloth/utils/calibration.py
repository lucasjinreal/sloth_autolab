class Calibration:
    def __init__(self, n_cam=4, width=1920, height=1200):
        self._width = width
        self._height = height
        self._x0 = self._width / 2.0 - 50.0
        self._y0 = self._height / 2.0 + 30.0

        self._anchors = [None] * n_cam

        if n_cam == 2:
            self._anchors[0] = {
                'center_x': 0.0,
                'center_y': 0.0,
                'scale': 6.0
            }

            self._anchors[1] = {
                'center_x': 15.0,
                'center_y': -15.0,
                'scale': 25.0
            }
        elif n_cam == 4:
            self._anchors[0] = {
                'center_x': 0.0,
                'center_y': 0.0,
                'scale': 6.0
            }

            self._anchors[1] = {
                'center_x': 30.0,
                'center_y': 5.0,
                'scale': 12.5
            }

            self._anchors[2] = {
                'center_x': 15.0,
                'center_y': -15.0,
                'scale': 25.0
            }

            self._anchors[3] = {
                'center_x': 15.0,
                'center_y': 0.0,
                'scale': 50.0
            }
        else:
            raise ValueError('only support 2 or 4 camera for now')

    def getConvertedAnno(self, ann, idx_1, idx_2):
        ratio = self._anchors[idx_2]['scale'] / self._anchors[idx_1]['scale']
        dx = self._anchors[idx_2]['center_x'] - self._anchors[idx_1]['center_x']
        dy = self._anchors[idx_2]['center_y'] - self._anchors[idx_1]['center_y']

        x, y, w, h = ann['x'], ann['y'], ann['width'], ann['height']
        cx = x + w / 2
        cy = y + h / 2

        cx = ratio * (cx - self._x0) + self._x0
        cy = ratio * (cy - self._y0) + self._y0
        w *= ratio
        h *= ratio

        cx += dx
        cy += dy

        x = cx - w / 2
        y = cy - h / 2

        ann = ann.copy()
        ann['x'], ann['y'], ann['width'], ann['height'] = x, y, w, h

        return ann
