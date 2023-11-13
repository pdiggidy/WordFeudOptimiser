import cv2 as cv
import numpy as np
import pytesseract as tess


def screenshot_processing(path):
    # load the image and convert it to grayscale
    image = cv.imread(path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # apply adaptive thresholding to the image
    thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)

    # find contours in the thresholded image
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # create a mask for the text
    mask = np.zeros(image.shape, dtype=np.uint8)
    for c in cnts:
        area = cv.contourArea(c)
        if area > 1000:
            cv.drawContours(mask, [c], -1, (255, 255, 255), -1)

    # # save the result
    # cv.imwrite('Test_screenshot_thresh.png', thresh)
    # cv.imwrite('Test_screenshot_mask.png', mask)

    # convert the mask to grayscale
    mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

    # get the center of the image
    (h, w) = image.shape[:2]
    center = (h // 2, w // 2)
    # get the first coordinates up and down of the center on the mask which are black
    up = None
    down = None
    # check up
    for i in range(center[0]):
        if mask[center[0] - i][center[1]] == 0:
            up = (center[0] - i, center[1])
            break
    # check down
    for i in range(center[0], h):
        if mask[i][center[1]] == 0:
            down = (i, center[1])
            break

    grid_top = up[0]
    grid_bottom = down[0]

    grid_image = image[grid_top:grid_bottom, :]
    cv.imwrite('screenshot_grid.png', grid_image)

    # get the lower portion of the image
    lower_image = image[grid_bottom:, :]
    lower_image_mask = mask[grid_bottom:, :]
    # cv.imwrite('Test_screenshot_lower_mask.png', lower_image_mask)
    # cv.imwrite('Test_screenshot_lower.png', lower_image)

    # condense the lower_mask to a single list of 0s and 1s where if all the pixels in a row are white then it is 1 else 0
    # turn all 255 to 1
    lower_image_mask = lower_image_mask / 255
    lower_image_mask = lower_image_mask.astype(int)

    # height = 717, width = 1080
    lower_image_mask_list = []
    for i in range(len(lower_image_mask)):
        if sum(lower_image_mask[i]) == 1080:
            lower_image_mask_list.append(1)
        else:
            lower_image_mask_list.append(0)

    # find the first 1 in the list
    first_1 = lower_image_mask_list.index(1)
    # find the last 1 in the list
    last_1 = len(lower_image_mask_list) - lower_image_mask_list[::-1].index(1) - 1

    # crop the lower image to the first and last 1
    lower_image = lower_image[first_1:last_1, :]
    lower_image_mask = lower_image_mask[first_1:last_1, :]
    # print(lower_image_mask)

    # save lower image mask as black and white image

    shape = lower_image_mask.shape
    third = shape[0] // 3
    center = shape[1] // 2
    top = None
    bottom = None
    for i in range(third):
        if (lower_image_mask[third - i][center]) == 0:
            top = third - i
            break
    for i in range(third, shape[0]):
        if (lower_image_mask[i][center]) == 0:
            bottom = i
            break

    # crop the lower image and mask to the top and bottom
    lower_image = lower_image[top:bottom, :]
    cv.imwrite('Test_screenshot_lower.png', lower_image)
    return grid_image, lower_image


def get_text_from_image(image, mode):
    bw_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # image = cv.medianBlur(cv.cvtColor(image, cv.COLOR_BGR2GRAY), 3)
    # convert o black and white
    # image = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    if mode == "grid":
        l = []
        # Get the dimensions of the image
        height, width = bw_image.shape

        # Define the size of the subimages
        subimage_height, subimage_width = height // 15, width // 15

        # Initialize a list to store the subimages
        subimages = []

        # Iterate through the image and extract the subimages
        for i in range(15):
            for j in range(15):
                # Calculate the coordinates for each subimage
                y1 = i * subimage_height
                y2 = (i + 1) * subimage_height
                x1 = j * subimage_width
                x2 = (j + 1) * subimage_width

                # Extract the subimage from the original image
                subimage = image[y1:y2, x1:x2]

                # Append the subimage to the list
                subimages.append(subimage)
        i = 0
        custom_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for sub in subimages:
            # cv.imwrite('Test_screenshot_cell.png', cell)
            print(sub)
            # TODO: check for empty cells/ cells with color that isnt black or white
            # if sub is empty, add "" to the list, else add the text, test color (remeber to swutch RGB order)
            break
            sub = cv.medianBlur(sub, 5)
            text = tess.image_to_string(sub, config=custom_config)
            #     # print(text)
            #     # save the subset image as a png
            # cv.imwrite(f'cells/Test_screenshot_cell{i}.png', sub)
            i += 1
            l.append(text)
        # print(l)
    return l


if __name__ == '__main__':
    grid, letters = screenshot_processing('Test_screenshot.jpg')
    new_grid = get_text_from_image(grid, "grid")

correct_grid = ["TL", "", "", "", "TW", "", "", "DL", "", "", "TW", "", "", "", "TL",
                "", "DL", "", "", "", "TL", "", "", "", "TL", "", "", "", "DL", "",
                "", "", "DW", "", "", "", "DL", "", "DL", "", "", "", "DW", "", "M",
                "", "", "", "TL", "", "", "", "DW", "", "", "", "TL", "", "L", "A",
                "TW", "", "", "", "DW", "", "DL", "", "DL", "", "H", "", "M", "I", "X",
                "", "TL", "", "", "", "TL", "", "", "", "Q", "I", "S", "", "B", "",
                "", "", "DL", "", "DL", "", "", "", "", "A", "R", "", "DL", "E", "",
                "DL", "", "", "DW", "", "", "", "C", "I", "T", "E", "DW", "", "R", "E",
                "", "", "DL", "", "DL", "", "", "I", "", "", "DL", "", "Y", "", "N",
                "", "TL", "", "", "", "W", "A", "G", "E", "R", "", "L", "E", "A", "D",
                "TW", "", "", "", "DW", "", "H", "A", "DL", "", "DW", "", "N", "", "O",
                "", "", "", "TL", "", "", "", "R", "U", "S", "H", "TL", "S", "", "R",
                "", "", "DW", "", "", "", "V", "I", "T", "T", "A", "", "A", "N", "T", "E",
                "TL", "", "", "", "TW", "", "", "DL", "", "P", "I", "G", "", "", "TL"]

count = 0
for i in range(len(correct_grid)):
    if correct_grid[i] != new_grid[i].strip():
        print(i)
        if correct_grid[i] == "":
            print("empty")
        else:
            print(correct_grid[i])

        if new_grid[i] == "":
            print("empty")
        else:
            print(new_grid[i])
        print("-----")
        count += 1

print(count)
