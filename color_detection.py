import argparse
import cv2
import numpy as np
import pandas as pd

# agrument parser
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required=True,
                    help='image path to input', type=str)
args = parser.parse_args()


class BGRValues:
    def __init__(self):
        self.values = ()

    def get_bgr_values(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            image = params[0]
            # print(image.shape, x, y)
            b, g, r = image[y][x]
            self.values = (int(b), int(g), int(r))

    def get_values(self):
        return self.values


def get_color_name(bgr_value, colors_df):
    colors_df['distance'] = colors_df.apply(lambda row: abs(
        row.B - bgr_value[0]) + abs(row.G - bgr_value[1]) + abs(row.R - bgr_value[2]), axis=1)
    colors_df = colors_df.sort_values('distance', ascending=True).reset_index()

    return (colors_df.loc[0, 'color_name'], colors_df.loc[0, 'B'], colors_df.loc[0, 'G'], colors_df.loc[0, 'R'])


def main():
    bgr = BGRValues()

    # Reading csv file with pandas and giving names to each column
    index = ["color", "color_name", "hex_value", "R", "G", "B"]
    colors = pd.read_csv('data/colors.csv', names=index, header=None)

    while True:
        # reading image with opencv
        img = cv2.imread(args.image, 1)
        img_name = 'Canvas'
        cv2.imshow(img_name, img)

        # handle mouse clicking event
        params = [np.copy(img)]
        cv2.setMouseCallback(img_name, bgr.get_bgr_values, params)

        bgr_value = bgr.get_values()
        if bgr_value:
            (color_name, b, g, r) = get_color_name(bgr_value, colors)
            # print(color_name, bgr_value)

            img = cv2.rectangle(img, (20, 20), (750, 60),
                                (int(b), int(g), int(r)), -1)
            img = cv2.putText(img, '{} R={} G={} B={}'.format(color_name, int(r), int(
                g), int(b)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow(img_name, img)

        # loop until Esc key is pressed
        if cv2.waitKey(20) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
