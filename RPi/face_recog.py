from facerecg.face_recognition.face_recog import Face

usr_dir = "./reg_user"
face = Face(usr_dir)

result = face.detect_faces()
print(result)