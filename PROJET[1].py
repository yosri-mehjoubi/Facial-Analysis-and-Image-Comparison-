import tkinter as tk
import cv2
from deepface import DeepFace
from tkinter import filedialog
from PIL import Image, ImageTk

def start_processing():
    video = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    while True:
        ret, frame = video.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            image_test = 'image_test.png'
            cv2.imwrite(image_test, roi_gray)

            color = (255, 0, 0)
            stroke = 2
            toul = x+w
            ared = y+h
            cv2.rectangle(frame, (x, y), (toul, ared), color, stroke)

            try:
                analyze = DeepFace.analyze(frame, actions=['emotion', 'gender', 'age'])
                mytext = analyze[0]['dominant_emotion']
                gender = analyze[0]['dominant_gender']
                age = analyze[0]['age']
                print("Dominant Emotion:", mytext)
                print("Gender:", gender)
                print("Age:", age)

                cv2.putText(frame, "Dominant Emotion: " + mytext, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                cv2.putText(frame, "Gender: " + gender, (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                cv2.putText(frame, "Age: " + str(age), (x, y+h+60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            except:
                print("No face detected")

        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

def process_image(image_path):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    frame = cv2.imread(image_path)

    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = frame[y:y+h, x:x+w]

        color = (255, 0, 0)
        stroke = 2
        toul = x+w
        ared = y+h
        cv2.rectangle(frame, (x, y), (toul, ared), color, stroke)

        try:
            analyze = DeepFace.analyze(roi_gray, actions=['emotion', 'gender', 'age'])
            mytext = analyze[0]['dominant_emotion']
            gender = analyze[0]['dominant_gender']
            age = analyze[0]['age']
            print("Dominant Emotion:", mytext)
            print("Gender:", gender)
            print("Age:", age)

            cv2.putText(frame, "Dominant Emotion: " + mytext, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(frame, "Gender: " + gender, (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(frame, "Age: " + str(age), (x, y+h+60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        except:
            print("No face detected")

    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file_path:
        process_image(file_path)

# Création de la fenêtre principale
window = tk.Tk()
window.title("Home")
background_image = Image.open("iaa.jpg")  # Remplacez "background_image.jpg" par le chemin de votre image
background_photo = ImageTk.PhotoImage(background_image)
# Création d'un widget de canevas pour afficher l'image
canvas = tk.Canvas(window, width=900, height=900)  # Définissez les dimensions du canevas selon vos besoins
canvas.pack(fill="both", expand=True)
canvas.create_image(0,0, image=background_photo, anchor="nw")

# Création du bouton
button = tk.Button(window, text="Démarrer le traitement", command=start_processing)
button.place(relx=0.5, rely=0.5, anchor="center")

# Création du bouton de sélection d'image
select_button = tk.Button(window, text="Sélectionner une image", command=select_image)
select_button.place(relx=0.5, rely=0.4, anchor="center")



#verififcation de deux image 
def select_and_verify():
    file_path1 = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    file_path2 = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])

    if file_path1 and file_path2:
        # Chargement des images
        image1 = Image.open(file_path1)
        image2 = Image.open(file_path2)

        # Redimensionnement des images pour les afficher côte à côte
        image1 = image1.resize((400, 400))
        image2 = image2.resize((400, 400))

        # Création de la nouvelle fenêtre pour afficher les images
        image_window = tk.Toplevel()
        image_window.title("Images")

        # Création des objets ImageTk.PhotoImage et les assigner à des attributs de la fenêtre
        image_window.photo1 = ImageTk.PhotoImage(image1)
        image_window.photo2 = ImageTk.PhotoImage(image2)

        # Affichage de l'image 1
        label1 = tk.Label(image_window, image=image_window.photo1)
        label1.pack(side="left")

        # Affichage de l'image 2
        label2 = tk.Label(image_window, image=image_window.photo2)
        label2.pack(side="right")

        # Vérification des images avec DeepFace
        result = DeepFace.verify(img1_path=file_path1, img2_path=file_path2, distance_metric="euclidean")
        is_identical = result["verified"]

        # Affichage du texte sur les images
        if is_identical:
            label1_text = "Identique"
            label2_text = "Identique"
        else:
            label1_text = "Non Identique"
            label2_text = "Non Identique"

        # Création des labels de texte
        label1 = tk.Label(image_window, text=label1_text, font=("Arial", 16), fg="green" if is_identical else "red")
        label1.pack(side="left")
        label2 = tk.Label(image_window, text=label2_text, font=("Arial", 16), fg="green" if is_identical else "red")
        label2.pack(side="right")
# Création du bouton de sélection et de vérification
verify_button = tk.Button(window, text="Vérifier les images", command=select_and_verify,width=17, height=1)
verify_button.place(relx=0.5, rely=0.6, anchor="center")



# Lancement de la boucle principale de l'interface
window.mainloop()

