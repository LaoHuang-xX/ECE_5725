import face_recognition

image = face_recognition.load_image_file("photo.jpg")

# # Find all the faces in the image
# face_locations = face_recognition.face_locations(image)

# # Or maybe find the facial features in the image
# face_landmarks_list = face_recognition.face_landmarks(image)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("./face_recognition/examples/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("./face_recognition/examples/biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]

known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Or you could get face encodings for each face in the image:
list_of_face_encodings = face_recognition.face_encodings(image)

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_face_encodings, list_of_face_encodings)