import cv2
from face_detection import face
from keras.models import load_model
import numpy as np
from embedding import emb
#from retreive_pymongo_data import database


label=None
a={0:0,1:0,2:0}
people={0:"trump",1:"obama",2:"thien"}
abhi=None
#data=database()
e=emb()
fd=face()

print('attendance till now is ')
#data.view()

model=load_model('face_reco2.MODEL')


def test():
    test_run=cv2.imread('demo.jpg',1)
    test_run=cv2.resize(test_run,(160,160))
    #test_run=np.rollaxis(test_run,2,0)
    test_run=test_run.astype('float')/255.0
    test_run=np.expand_dims(test_run,axis=0)
    test_run=e.calculate(test_run)
    test_run=np.expand_dims(test_run,axis=0)
    test_run=model.predict(test_run)[0]
    prediction=test_run
    result=int(np.argmax(prediction))
    print(prediction)
    print(result)


cap=cv2.VideoCapture(0)
# ret=False
ret=True
test()
while ret:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    det,coor=fd.detectFace(frame)

    if(det is not None):
        for i in range(len(det)):
            detected=det[i]
            k=coor[i]
            f=detected
            detected=cv2.resize(detected,(160,160))
            #detected=np.rollaxis(detected,2,0)
            detected=detected.astype('float')/255.0
            detected=np.expand_dims(detected,axis=0)
            feed=e.calculate(detected)
            feed=np.expand_dims(feed,axis=0)
            prediction=model.predict(feed)[0]

            result=int(np.argmax(prediction))
            print(prediction)
            print(result)
            if(np.max(prediction)>.70):
                for i in people:
                    if(result==i):
                        label=people[i]
                        print(label)
                        if(a[i]==0):
                            print("a")
                        a[i]=1
                        abhi=i
            else:
                label='unknown'
            #data.update(label)


            cv2.putText(frame,label,(k[0],k[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            #if(abhi is not None):
                #if(a[abhi]==1):
                    #cv2.putText(frame,"your attendance is complete",(x,y-30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.rectangle(frame,(k[0],k[1]),(k[0]+k[2],k[1]+k[3]),(252,160,39),3)
            cv2.imshow('onlyFace',f)
    cv2.imshow('frame',frame)
    if(cv2.waitKey(1) & 0XFF==ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
# data.export_csv()
