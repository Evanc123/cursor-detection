import cv2
import numpy as np

# Load the image
image = cv2.imread("screenshots/templates/apple_mouse_default_pointer_template.png")

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to find pure white areas
# Note: 255 is the value for pure white in grayscale
_, mask = cv2.threshold(gray, 195, 255, cv2.THRESH_BINARY)

# Invert the mask so pure white is 0 (black)
mask_inv = cv2.bitwise_not(mask)

# Convert the mask back to BGR format to combine with original
mask_inv_bgr = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR)

# Apply the mask to the original image
final_image = cv2.bitwise_and(image, mask_inv_bgr)

# Save the resulting image
cv2.imwrite("image_with_black_background.png", final_image)

# Optionally display the image
cv2.imshow("Image with Black Background", final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
