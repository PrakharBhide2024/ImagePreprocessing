import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
# Define the MedianFilter function
def MedianFilter(image, filtersize):
    output = np.zeros(image.shape, np.uint8)
    filterarray = [0] * filtersize
    if filtersize == 9:
        for j in range(1, image.shape[0] - 1):
            for i in range(1, image.shape[1] - 1):
                filterarray[0] = image[j - 1, i - 1]
                filterarray[1] = image[j, i - 1]
                filterarray[2] = image[j + 1, i - 1]
                filterarray[3] = image[j - 1, i]
                filterarray[4] = image[j, i]
                filterarray[5] = image[j + 1, i]
                filterarray[6] = image[j - 1, i + 1]
                filterarray[7] = image[j, i + 1]
                filterarray[8] = image[j + 1, i + 1]
                filterarray.sort()
                output[j, i] = filterarray[4]
    return output

# Define the cropimage function
def cropimage(finalfilteredimg, cropvalue):
    # Convert image to numpy array
    imgarray = np.array(finalfilteredimg)
    # Get dimensions of the input image
    length, breadth, _ = imgarray.shape
    # Calculate maximum crop length and breadth
    maxcroplength = length - cropvalue
    maxcropbreadth = breadth - cropvalue
    # Crop the image
    croppedimage = imgarray[cropvalue:maxcroplength, cropvalue:maxcropbreadth, :]
    # Convert the cropped array back to an image
    cropped_finalfilteredimg = Image.fromarray(croppedimage)
    return cropped_finalfilteredimg
# Paths for the dataset and output folder
inputfolder = 'C:\\Users\\Prakhar Bhide\\Desktop\\INPUTIMAGES\\TomatoDataset\\Test\\Tomato_Yellow_Leaf_Curl_Virus'
outputfolder = 'C:\\Users\\Prakhar Bhide\\Desktop\\OUTPUTIMAGES\\Tomato_Yellow_Leaf_Curl_Virus\\Cropping'
# Ensure the output folder exists
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)

# Initialize a list to hold image pairs for batch display
image_pairs = []

# Process each image in the dataset
for filename in os.listdir(inputfolder):
    if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
        # Load the image
        img_path = os.path.join(inputfolder, filename)
        img = Image.open(img_path)
        imgarray = np.array(img)

        # Extract each color channel
        rimg = imgarray[:, :, 0]
        gimg = imgarray[:, :, 1]
        bimg = imgarray[:, :, 2]

        # Apply median filter to all extracted color channels
        filteredrimg = MedianFilter(rimg, 9)
        filteredgimg = MedianFilter(gimg, 9)
        filteredbimg = MedianFilter(bimg, 9)

        # Combine the filtered channels back into one image
        filteredimagearray = np.stack((filteredrimg, filteredgimg, filteredbimg), axis=2)
        # Convert the combined array back to an image
        finalfilteredimg = Image.fromarray(filteredimagearray)

        # Crop the image
        croppedfinalfilteredimg = cropimage(finalfilteredimg, 10)
        
        # Save the cropped image
        output_path = os.path.join(outputfolder, filename)
        croppedfinalfilteredimg.save(output_path)

        # Print dimensions
        original_width, original_height = img.size
        cropped_width, cropped_height = croppedfinalfilteredimg.size
        print(f'Original (Width, Height): ({original_width}, {original_height})')
        print(f'Cropped (Width, Height): ({cropped_width}, {cropped_height})')

        # Add the original and filtered image pair to the list
        image_pairs.append((img, croppedfinalfilteredimg))

        # Display the images in batches of 5
        if len(image_pairs) == 5:
            plt.figure(figsize=(20, 10))  # Adjust figure size if needed
            for i, (original, filtered) in enumerate(image_pairs):
                plt.subplot(2, 5, i + 1)
                plt.title('Original Image')
                plt.imshow(original)
                plt.axis('off')
                plt.subplot(2, 5, i + 1 + 5)
                plt.title('Filtered and Cropped Image')
                plt.imshow(filtered)
                plt.axis('off')
            plt.tight_layout()
            plt.show()
            image_pairs = []

# Display any remaining image pairs
if image_pairs:
    plt.figure(figsize=(20, 10))  # Adjust figure size if needed
    for i, (original, filtered) in enumerate(image_pairs):
        plt.subplot(2, 5, i + 1)
        plt.title('Original Image')
        plt.imshow(original)
        plt.axis('off')
        plt.subplot(2, 5, i + 1 + 5)
        plt.title('Filtered and Cropped Image')
        plt.imshow(filtered)
        plt.axis('off')
    plt.tight_layout()
    plt.show()