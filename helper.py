from flask import make_response
from cv2 import CascadeClassifier, CASCADE_SCALE_IMAGE, COLOR_BGR2GRAY, cvtColor, imencode, imread, rectangle
from mimetypes import init, types_map
import base64
import sql

def faceDetect(imageName):
    if(imageName != '' and imageName != None):
        # Init type map
        init()

        # Load image and CASC file
        #imagePath = 'static/affiches/20230515182830655.png'
        imagePath = sql.cheminAffiche + imageName
        cascPath = './haarcascade_frontalface_default.xml'

        # Create the haar cascade
        faceCascade = CascadeClassifier(cascPath)

        # Read the image
        image = imread(imagePath)
        gray = cvtColor(image, COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.3,
            minNeighbors = 3, # 5 de base
            minSize = (30, 30),
            flags = CASCADE_SCALE_IMAGE
        )

        print('Found {} faces!'.format(len(faces)))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 5)

        # Encode image in BytesIO buffer
        retval, buffer = imencode('.jpg', image)

        # Build flask response
        response = make_response(buffer.tobytes())

        # Set flask content type (display image in web interface)
        response.headers['Content-Type'] = types_map['.{}'.format('jpg')]
        return base64.b64encode(buffer).decode('utf-8')
    else:
        return ''