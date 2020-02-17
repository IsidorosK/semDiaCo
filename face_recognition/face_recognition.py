import os 
import sys
import cv2

cascade_dir = "/mnt/c/Users/Alekos/Desktop/alex/haarcascades/"
face_cascade = cv2.CascadeClassifier(cascade_dir + "haarcascade_frontalface_default.xml")

indir  = '/mnt/c/Users/Alekos/Desktop/alex/images'
outdir = '/mnt/c/Users/Alekos/Desktop/alex/processed_images'

images_with_faces    = []
images_without_faces = []

for root, dirs, filenames in os.walk(indir):
    for filename in filenames:
        
        img_path = os.path.join(root, filename)

        print("Examining... " + img_path)
        
        # open image and detect faces
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=3,minSize=(10, 10),flags=cv2.CASCADE_SCALE_IMAGE)
       

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # write to file in the appropriate directory
        if len(faces) > 0:
            write_filename = outdir + '/contain_faces/'
            images_with_faces.append(img_path)
        else:
            write_filename = outdir + '/do_not_contain_faces/'
            images_without_faces.append(img_path)

        write_filename = write_filename + filename

        cv2.imwrite(write_filename, image)

print("Images with faces: " + str(len(images_with_faces)))
[print(image) for image in images_with_faces]
print()
print("Images without faces: " + str(len(images_without_faces)))
[print(image) for image in images_without_faces]