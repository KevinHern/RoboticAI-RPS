# https://rps-tfjs.netlify.app
from game.rps import RPS
import cv2
from tensorflow.python.keras.models import load_model
from os.path import join, dirname
import numpy as np
import time

if __name__ == '__main__':
    # Initialize Game
    rps = RPS(best_of=5)

    # Run Game
    rps.run()
    # ai_model = load_model(join(dirname(__file__), "game", "components", "best_model_0.75.h5"))
    # vid = cv2.VideoCapture(0)
    # rps_timer_max = 3
    # rps_timer = rps_timer_max
    # while True:
    #     print("Countdown: {}".format(rps_timer))
    #     if rps_timer == 0:
    #         # Capture the video frame
    #         # by frame
    #         ret, frame = vid.read()
    #         new_region = frame[0:300, 0:300]
    #         cropped_frame = cv2.cvtColor(new_region, cv2.COLOR_BGR2RGB)
    #
    #         # Display the resulting frame
    #         cv2.imshow('frame', cropped_frame)
    #
    #         print("Do something")
    #         x = cv2.resize(cropped_frame, (300, 300)) / 255
    #         img_arr = np.array(x).reshape((1, 300, 300, 3))
    #         print(img_arr.shape)
    #         y = ai_model.predict(img_arr)
    #         p_num = np.argmax(y, axis=1)[0]
    #
    #         rps_timer = rps_timer_max
    #
    #         # the 'q' button is set aqqs the
    #         # quitting button you may use any
    #         # desired button of your choice
    #         if cv2.waitKey(1000) & 0xFF == ord('q'):
    #             break
    #     else:
    #         time.sleep(1)
    #         rps_timer -= 1
    #
    # # After the loop release the cap object
    # vid.release()
    # # Destroy all the windows
    # cv2.destroyAllWindows()
