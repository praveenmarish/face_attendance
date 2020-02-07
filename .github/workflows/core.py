import sys
import cv2
import os
import numpy as np
import pickle
import xlsxwriter
import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import Workbook
import datetime
from tkinter import messagebox
from tkinter import *
import PIL.Image
     
#cascade for detect face
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

def test():
    #initiate camera
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        cv2.imshow('Image with faces', frame)

        if len(faces) == 0:
            print("No faces found")
            if cv2.waitKey(20) & 0xff==ord('q'):
                break 
        

        else:
            print("Number of faces detected: " + str(faces.shape[0]))
            if cv2.waitKey(20) & 0xff==ord('q'):
                break

        if cv2.waitKey(20) & 0xff==ord('q'):
            break 
    

    cap.release()
    cv2.destroyAllWindows()
    pass
        

def take_photos():
    def take():        
        i=0 #for iterating towards folder to save image
        tk.withdraw()
        #initiate camera,get path,name of floder
        webcam = cv2.VideoCapture(0)
        BASE_DIR =os.getcwd()
        name=input("enter student name:")
        #name="marish"
        pathneed="images\\"+name
        image_dir = os.path.join(BASE_DIR, pathneed)
        def overwrite():
            return messagebox.askquestion("confirm","Do you want to over write the content?")

        #create or use existing folder
        if (not os.path.exists(image_dir)):
            os.mkdir(image_dir)
            messagebox.showinfo("Message","Directory was successfully Created")
            s='y'

        else:
            ab=overwrite()
            if ab=='yes' :
                s = 'y'
            else:
                s ='n'
            #s=input("do you want to over write the condent(y/n)")


        #capture image frame by frame
        while ((i<20) & (s=='y')):

            check, frame = webcam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            cv2.imshow("Capturing", frame)

            #detect faces and save
            for (x,y,w,h) in faces:
                if cv2.waitKey(50) & (faces.shape[0]==1):
                    cv2.imwrite(filename=pathneed+"\\"+str(i)+'.jpg', img=frame)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    org = (40, 450) 
                    color = (255, 0, 0) 
                    fontScale = 1
                    thickness = 1
                    frame1=cv2.putText(frame, 'Image Saving...', org, font,  fontScale, color, thickness, cv2.LINE_AA)
                    cv2.imshow("Capturing", frame1)
                    i+=1
                    if cv2.waitKey(20) & 0xFF == ord('q'):
                        break

            if cv2.waitKey(20) & 0xFF == ord('q'):
                        break

        webcam.release()
        cv2.destroyAllWindows()
    tk=Tk()
    tk.geometry("500x300")
    l1=Label(tk,text="Enter name")
    l1.place(x=100,y=100)
    e1=Entry(tk,width = 30)
    e1.place(x=180,y=100)
    name1=e1.get()
    b1=Button(tk,text="Ok",width=10,command=take).place(x=200,y=140)
    tk.mainloop()
    pass
        
def train():
    
    tk=Tk()
    tk.withdraw()
    #get path of image
    BASE_DIR = os.getcwd()
    image_dir = os.path.join(BASE_DIR, "images")
    
    #get recognizer file ref=https://docs.opencv.org/3.4/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html#ac33ba992b16f29f2824761cea5cd5fc5
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    #initialize variable for image and label
    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []   

    #take every image from name folder inside image folder
    for root, dirs, files in os.walk(image_dir):
           for file in files:            
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()

                    #save name in lable with id
                    if not label in label_ids:
                        label_ids[label] = current_id
                        current_id += 1
                    id_ = label_ids[label]

                    #y_labels.append(label) # some number
                    #x_train.append(path) # verify this image, turn into a NUMPY arrray, GRAY
                    pil_image = PIL.Image.open(path).convert("L") # grayscale
                    size = (550, 550)
                    final_image = pil_image.resize(size, PIL.Image.ANTIALIAS)
                    image_array = np.array(final_image, "uint8")

                    #detect face from image and map with lable using id
                    faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.01, minNeighbors=5)
                    for (x,y,w,h) in faces:
                        roi = image_array[y:y+h, x:x+w]
                        x_train.append(roi)
                        y_labels.append(id_)

    def create():
              
        #save name and id
        with open("pickles/face-labels.pickle", 'wb') as f:
            pickle.dump(label_ids, f)

        #save face matrix and id 
        recognizer.train(x_train, np.array(y_labels))
        recognizer.save("recognizers/face-trainner.yml")

        #create and initiate excel sheet
        workbook = xlsxwriter.Workbook('Attendance.xls')
        worksheet = workbook.add_worksheet('class1') 
        worksheet.write(0, 0, 'S.no')
        worksheet.write(0, 1, 'names')
        for key,val in label_ids.items():
                worksheet.write(1+val, 0, val+1)
                worksheet.write(1+val, 1, key)
        workbook.close() 
        pass
    create()
    messagebox.showinfo("Message","Faces trained successfully")
        
def attendence():
    
    #get path of excel
    path_xl = os.getcwd()
    xlfile = os.path.join(path_xl, "Attendance.xls")

    #get recognizer file ref=https://docs.opencv.org/3.4/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html#ac33ba992b16f29f2824761cea5cd5fc5
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./recognizers/face-trainner.yml")

    #get pickle file
    labels = {"person_name": 1}
    with open("pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    # To open Workbook for read
    rb = xlrd.open_workbook(xlfile) 
    sheet = rb.sheet_by_index(0)
    cols=sheet.ncols

    # To open Workbook for write
    wb = copy(rb)
    sheet1 = wb.get_sheet(0) 
    rows=sheet.nrows
    date_object = datetime.date.today()

    #style formate for date
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    #write date in excel
    sheet1.write(0,cols,date_object,date_format)

    #write data to excel sheet
    def xlent():
        for i in range(rows):
            if name==sheet.cell_value(i,1):
                now = datetime.datetime.now()
                time = now.strftime("%H:%M:%S")
                sheet1.write(i,cols,'last seen '+time)
                wb.save('Attendance.xls')
        pass

    #object for capture image
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)

            # use recognizer and label to predict face
            id_, conf = recognizer.predict(roi_gray)
            if (conf>=45) and (conf<=85):
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                #write text on over rectangle
                #xlent() function call
                xlent()



            else:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = "unknown"
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                #write text on over rectangle

            color = (255, 0, 0) #BGR 0-255 
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            #draw rectangle over face

            # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    pass
        
