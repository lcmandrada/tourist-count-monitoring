""" logic layer for tourist monitoring """

import os
# import sys
import threading
import subprocess
from datetime import datetime
import numpy as np
import cv2 as cv

class Monitor():
    """ tourist monitoring class """
    def __init__(self, indir, outdir):
        self.cascade = cv.CascadeClassifier('classifier/haarcascade_frontalface_default.xml')
        self.recognizer = cv.face.LBPHFaceRecognizer_create()
        self.indir = indir
        self.outdir = outdir
        self.exdir = "except/"

    def train(self):
        """ train face recognizer """
        faces = []
        labels = []

        # prepare training set
        for outdir in [self.outdir, self.exdir]:
            for file in os.listdir(outdir):
                if not os.listdir(outdir):
                    break

                # load face
                face = cv.imread("{}{}".format(outdir, file))
                gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)

                # set face
                face = cv.resize(gray, (100, 100), interpolation=cv.INTER_NEAREST)
                faces.append(face)

                # set label
                label = int(file.replace(".jpg", ""))
                labels.append(label)

        # train set
        self.recognizer.train(faces, np.array(labels))

    def detect(self, path):
        """ detect faces """
        # load photo
        photo = cv.imread(path)
        copy = photo.copy()
        gray = cv.cvtColor(photo, cv.COLOR_BGR2GRAY)

        # count for detected, recognized, new
        count = [0, 0, 0]

        distance = [0]

        # detect faces
        # image, scaleFactor, minNeighbors
        # with self.suppress():
        faces = self.cascade.detectMultiScale(gray, 1.1, 9)

        # delete photo
        os.remove(path)

        return photo, gray, copy, count, distance, faces

    def recognize(self, photo, gray, copy, count, distance, faces):
        """ recognize detected faces """
        # iterate detected faces
        if len(faces) > 0:
            for (x_coord, y_coord, width, height) in faces:
                # cut and resize face
                face = gray[y_coord:y_coord + height, x_coord:x_coord + width]
                face = cv.resize(face, (100, 100), interpolation=cv.INTER_NEAREST)
                # cv.rectangle(copy,
                #              (x_coord, y_coord),
                #              (x_coord+width, y_coord+height),
                #              (255, 255, 255),
                #              2)

                # count detected
                count[0] += 1

                # recognize face
                result = self.recognizer.predict(face)

                distance.append(result[1])

                # if face is not recognized
                # then label and add to training set
                if result[1] > 90:
                    track = len(os.listdir(self.outdir)) + 1
                    cv.imwrite("{}{}.jpg".format(self.outdir, track),
                               photo[y_coord:y_coord + height, x_coord:x_coord + width])
                    # cv.putText(copy,
                    #            "+" + str(int(result[1])),
                    #            (x_coord, y_coord),
                    #            cv.FONT_HERSHEY_PLAIN,
                    #            1.5,
                    #            (255, 255, 255),
                    #            2)

                    # count new
                    count[2] += 1

                    # retrain
                    self.train()
                # else label accordingly
                else:
                    # cv.putText(copy,
                    #            str(result[0]),
                    #            (x_coord, y_coord),
                    #            cv.FONT_HERSHEY_PLAIN,
                    #            1.5,
                    #            (255, 255, 255),
                    #            2)

                    # count recognized
                    count[1] += 1

        # report
        print("\nDetected: {}\nRecognized: {}\nNew: {}\n".format(count[0], count[1], count[2]))
        print("Min: {:.0f}\nMax: {:.0f}\n".format(min(distance), max(distance)))

        # width, height, _ = copy.shape
        # copy = cv.resize(copy, (int(height/1), int(width/1)), interpolation=cv.INTER_NEAREST)

        # display detected and recognized
        # cv.imshow('copy', copy)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

    def total(self):
        """ total counting """
        path = ["tourist/fort-santiago/output/", "tourist/casa-manila/output/"]

        # count for detected, recognized, new
        count = [0, 0, 0]

        distance = [0]

        for folder in path:
            for file in os.listdir(folder):
                if not os.listdir(folder):
                    break

                # load and resize face
                face = cv.imread("{}{}".format(folder, file))
                # copy = face.copy()
                gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
                gray = cv.resize(gray, (100, 100), interpolation=cv.INTER_NEAREST)

                # count detected
                count[0] += 1

                # recognize face
                result = self.recognizer.predict(gray)

                distance.append(result[1])

                # if face is not recognized
                # then label and add to training set
                if result[1] > 90:
                    track = len(os.listdir(self.outdir)) + 1
                    cv.imwrite("{}{}.jpg".format(self.outdir, track), face)
                    # cv.putText(copy,
                    #            "+" + str(int(result[1])),
                    #            (10, 10),
                    #            cv.FONT_HERSHEY_PLAIN,
                    #            1.5,
                    #            (255, 255, 255),
                    #            2)

                    # count new
                    count[2] += 1

                    # retrain
                    self.train()
                # else label accordingly
                else:
                    # cv.putText(copy,
                    #            str(result[0]),
                    #            (10, 10),
                    #            cv.FONT_HERSHEY_PLAIN,
                    #            1.5,
                    #            (255, 255, 255),
                    #            2)

                    # count recognized
                    count[1] += 1

                # display detected and recognized
                # cv.imshow('copy', copy)
                # cv.waitKey(0)
                # cv.destroyAllWindows()

        # report
        print("Detected: {}\nRecognized: {}\nNew: {}\n".format(count[0], count[1], count[2]))
        print("Min: {:.0f}\nMax: {:.0f}\n".format(min(distance), max(distance)))

    def count(self):
        """ update file count """
        count = 0
        count = len(os.listdir(self.outdir))

        return count

    # @staticmethod
    # def suppress():
    #     """ suppress an output """

    #     with open(os.devnull, "w") as devnull:
    #         old_stdout = sys.stdout
    #         sys.stdout = devnull
    #         try:
    #             yield
    #         finally:
    #             sys.stdout = old_stdout

class Tools():
    """ logic aux class """
    def __init__(self, fort, casa, total, view, data, window):
        self.fort = fort
        self.casa = casa
        self.total = total
        self.view = view
        self.data = data
        self.window = window
        self.timer = threading.Timer(30.0, self.check)
        self.timer.start()
        self.end = 2100

    def check(self):
        """ check every interval """
        self.timer = threading.Timer(30.0, self.check)
        self.timer.start()

        if int(datetime.now().strftime("%H%M")) >= self.end:
            self.clean()
            for monitor in [self.fort, self.casa, self.total]:
                self.reset(monitor)
            return

        # report and execute
        print("Checking Fort Santiago\n")
        count = self.execute(self.fort)
        self.view.fortLabel.setText("<html><head/><body><p><span style=\" font-weight:600;\">{}</span></p></body></html>".format(count))

        # report and execute
        print("Checking Casa Manila\n")
        count = self.execute(self.casa)
        self.view.casaLabel.setText("<html><head/><body><p><span style=\" font-weight:600;\">{}</span></p></body></html>".format(count))

        # report and execute
        print("Checking Total\n")
        count = self.execute(self.total)
        self.view.totalLabel.setText("<html><head/><body><p><span style=\" font-weight:600;\">{}</span></p></body></html>".format(count))

    @staticmethod
    def execute(monitor):
        """ start monitoring """
        monitor.train()
        if monitor.indir == "tourist/total/input/":
            monitor.total()
        else:
            if os.listdir(monitor.indir):
                for file in os.listdir(monitor.indir):
                    photo, gray, copy, count, distance, faces = monitor.detect("{}{}".format(monitor.indir, file))
                    monitor.recognize(photo, gray, copy, count, distance, faces)

        return monitor.count()

    def open_log(self):
        """ open log """
        if int(datetime.now().strftime("%H%M")) < self.end:
            self.update_data()
        if os.listdir("log/"):
            os.remove("log/log.csv")
        self.data.export_log()
        os.startfile("log\\log.csv")

    def update_data(self):
        """ update data """
        date = datetime.now().strftime("%B %d, %Y")
        table = self.data.check_entry(date)

        fort = self.fort.count()
        casa = self.casa.count()
        total = self.total.count()

        if not table:
            self.data.add_entry(date, fort, casa, total)
        else:
            self.data.edit_entry(date, fort, casa, total)

    def clean(self):
        """ clean exit """
        self.timer.cancel()
        print("END")

    @staticmethod
    def reset(monitor):
        """ reset data """
        if os.listdir(monitor.outdir):
            for file in os.listdir(monitor.outdir):
                os.remove("{}{}".format(monitor.outdir, file))
