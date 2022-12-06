from .components.camera import Camera
import logging
from datetime import datetime
from os.path import join, dirname, exists
from os import mkdir
from random import choice
from tensorflow.python.keras.models import load_model
import cv2
import time


class RPS:
    ROCK = 0
    PAPER = 1
    SCISSORS = 2
    INDEX_TO_MOVE_MAP = {
        0: "Rock",
        1: "Paper",
        2: "Scissors",
    }

    def __init__(self, best_of, rps_timer=3):
        # Initialize Directories
        parent_directory = dirname(__file__)
        logs_directory = join(parent_directory, "logs")
        ai_directory = join(parent_directory, "components")

        # Creating Logs directory
        if not exists(logs_directory):
            mkdir(logs_directory)

        # Initialize logger
        today_date = datetime.today().strftime('%Y_%m_%d-%H_%M')
        logging.basicConfig(
            # filename=join(directory_path, 'rps_log_{}.log'.format(today_date)),
            # filemode='w',
            level=logging.INFO,
            format='\n%(asctime)s-%(levelname)s> %(message)s',
            datefmt='%d-%b-%y %H:%M:%S',
            handlers=[
                logging.FileHandler(join(logs_directory, 'rps_log_{}.log'.format(today_date))),
                logging.StreamHandler()
            ]
        )

        logging.info(msg="[SYSTEM] Iniciando el juego...")

        # Initialize Parameters
        self.best_of = best_of
        self.maximum_games = (self.best_of // 2) + 1
        self.rps_timer_max = rps_timer
        self.rps_timer = rps_timer

        logging.info(msg="[SYSTEM] Cargando modelo de AI...")
        # Initialize variables
        self.player_games = 0
        self.ai_games = 0
        self.ai_model = load_model(join(ai_directory, "best_model_0.75.h5"))
        logging.info(msg="[SYSTEM] Modelo de AI listo.")

        # Initialize components
        logging.info(msg="[SYSTEM] Cargando cámara...")
        self.webcam = Camera(x_axis_crop=(0, 300), y_axis_crop=(0, 300))
        logging.info(msg="[SYSTEM] Cámara lista.")

    @staticmethod
    def determine_ai_win(ai_option, player_option):
        if ai_option == player_option:
            # DRAW game
            return None
        elif ai_option == (player_option - 1) or ai_option == (player_option + 2):
            # Human wins
            return False
        else:
            return True

    def calibrate(self):
        logging.info(msg="[SYSTEM] Calibrando... (Presiona Q para terminar de calibrar).")
        while True:
            # Obtain frame and crop it
            frame = self.webcam.freeze_frame()

            # Display the frame
            cv2.imshow('frame', frame)

            # Wait for Key Press to finish calibration
            if cv2.waitKey(100) & 0xFF == ord('q'):
                logging.info(msg="[SYSTEM] Juego calibrado.")
                break

    def run(self):
        # Calibrate Camera and Game
        self.calibrate()

        # Initializing game
        logging.info(msg="[SYSTEM] Empezando el juego...")
        # Reset variables
        self.player_games = 0
        self.ai_games = 0
        game_round = 1

        while True:
            logging.info(msg="Ronda #{}".format(game_round))
            # Send signal to hand to show option
            # Do something()

            # Run timer
            while self.rps_timer > 0:
                logging.info(msg="{}...".format(self.rps_timer))
                # Wait for 1 second
                time.sleep(1)

                # Reduce timer
                self.rps_timer -= 1

            # Take screenshot and identify option
            player_option = choice([RPS.ROCK, RPS.SCISSORS, RPS.PAPER])
            ai_option = choice([RPS.ROCK, RPS.SCISSORS, RPS.PAPER])

            # Decide if it was a win or lose
            logging.info(
                msg="Movimientos escogidos:\nJugador: {}\nAI: {}".format(RPS.INDEX_TO_MOVE_MAP[player_option],
                                                                         RPS.INDEX_TO_MOVE_MAP[ai_option]))
            did_ai_win = RPS.determine_ai_win(ai_option=ai_option, player_option=player_option)

            # Determine the state of the game
            if did_ai_win is None:
                msg = "Empate!\n"
            elif did_ai_win:
                self.ai_games += 1
                msg = "AI gano!\n"
            else:
                self.player_games += 1
                msg = "Jugador gano!\n"

            msg += "Jugador {} - AI {}".format(self.player_games, self.ai_games)
            logging.info(msg=msg)

            # Increase Round
            game_round += 1

            if self.ai_games == self.maximum_games:
                # Send parameters to show win
                logging.info(msg="AI Gano el set!")
                break
            elif self.player_games == self.maximum_games:
                # Send parameters to show loss
                logging.info(msg="Jugador gano el set!")
                break
            else:
                # Reset Timer
                self.rps_timer = self.rps_timer_max
                continue

        logging.info(msg="Juego terminado")

        logging.info(msg="[SYSTEM] Liberando recursos...")
        self.webcam.release()
        logging.info(msg="[SYSTEM] Recursos liberados")
