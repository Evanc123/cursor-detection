import cv2
import numpy as np


# Below works for one screenshot / template pair
def multi_scale_template_matching(screenshot_path, template_path):
    img = cv2.imread(screenshot_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    # List to store the rectangles
    rectangles = []

    # Scale factors to adjust size of the template
    for scale in np.linspace(0.1, 1.5, 10):  # Adjust range and steps as needed
        resized_template = cv2.resize(
            template, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA
        )
        res = cv2.matchTemplate(img_gray, resized_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Threshold might need adjustment based on results
        loc = np.where(res >= threshold)

        # Store rectangles for each scale
        for pt in zip(*loc[::-1]):  # Switch columns and rows in loc
            rectangles.append(
                (int(pt[0]), int(pt[1]), int(pt[0] + w * scale), int(pt[1] + h * scale))
            )

    # Use function to filter for the best rectangle per location (to avoid duplicates)
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    print(rectangles)

    # Draw rectangles on the original image
    for x, y, x2, y2 in rectangles:
        cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)

    # Show the result
    cv2.imshow("Detected Apple Mouses", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# multi_scale_template_matching(
#     "screenshots/testers/apple_pointer_easy.png",
#     "screenshots/templates/apple_mouse_default_pointer_template.png",
# )


# the more general version
def detect_apple_mouse(screenshot_path, template_paths):
    # Load the screenshot
    img = cv2.imread(screenshot_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Variables to store the best matches for each template
    best_matches = []

    # Iterate over each template and scale
    for template_path in template_paths:
        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]

        # Scale factors to adjust size of the template
        for scale in np.linspace(0.1, 1.5, 30):  # Adjust range and steps as needed
            resized_template = cv2.resize(
                template, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA
            )
            channels = cv2.split(resized_template)
            zero_channel = np.zeros_like(channels[0])
            mask = np.array(channels[3])
            mask[channels[3] == 0] = 1
            mask[channels[3] == 100] = 0
            transparent_mask = cv2.merge(
                [zero_channel, zero_channel, zero_channel, mask]
            )

            # Perform template matching
            res = cv2.matchTemplate(
                img_gray, resized_template, cv2.TM_SQDIFF, mask=transparent_mask
            )
            min_val, max_val_temp, min_loc, max_loc_temp = cv2.minMaxLoc(res)

            # Store the best match for this template and scale
            if max_val_temp > 0.2:  # Consider matches above a certain threshold
                best_matches.append(
                    (max_val_temp, max_loc_temp, int(w * scale), int(h * scale))
                )

    # Sort matches by the match quality
    best_matches.sort(reverse=True, key=lambda x: x[0])

    # Draw rectangles around the best matches
    for match in best_matches[:1]:  # Limit to top 3 matches
        max_val, best_loc, best_w, best_h = match
        top_left = best_loc
        bottom_right = (top_left[0] + best_w, top_left[1] + best_h)
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        print("Match found with value: ", max_val)

        # Display the result
        cv2.imshow("Best Detected Apple Mouse", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No match found.")


# Example usage
template_paths = [
    # "screenshots/templates/apple_hand_template.png",
    # "screenshots/templates/apple_mouse_default_pointer_template.png",
    # "screenshots/templates/apple_text_selection_template.png",
    "screenshots/templates/image_with_black_background.png",
]

testers = [
    # "screenshots/testers/apple_text_select_hard.png", # doesn't work on this one :(
    "screenshots/testers/apple_hand_easy.png",
    "screenshots/testers/apple_pointer_easy.png",
    "screenshots/testers/apple_text_select_easy.png",
]

for tester in testers:
    detect_apple_mouse(tester, template_paths)
