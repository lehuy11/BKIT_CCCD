import cv2

# Load the image
image_path = 'img/duc.jpg'
image = cv2.imread(image_path)

# Get the dimensions of the image
height, width, _ = image.shape

# Define the region of interest (ROI) to include only the MRZ lines
# Adjust the mrz_top and mrz_bottom to precisely match the provided MRZ image
mrz_top = height - 200  # Adjust as needed
mrz_bottom = height     # Adjust as needed
roi = image[mrz_top:mrz_bottom, 0:width]

# Save the cropped image
output_path = 'img/duc.jpg'
cv2.imwrite(output_path, roi)

output_path
