import pickle
import os 

class CalibrationParameters():
    def __init__(self, chessboard_dimensions, square_size, S, timer_time):
        self.chessboard_dimensions=chessboard_dimensions
        self.square_size=square_size
        self.S=S
        self.timer_time=timer_time

    def save(self, full_path):
        with open(os.path.join(full_path, *["chessboard_dimensions.pickle"]), 'wb') as file:
            pickle.dump(self.chessboard_dimensions, file)
        with open(os.path.join(full_path, *["square_size.pickle"]), 'wb') as file:
            pickle.dump(self.square_size, file)
        with open(os.path.join(full_path, *["S.pickle"]), 'wb') as file:
            pickle.dump(self.S, file)
        with open(os.path.join(full_path, *["timer_time.pickle"]), 'wb') as file:
            pickle.dump(self.timer_time, file)

    @staticmethod
    def load(full_path):
        chessboard_dimensions=None 
        square_size=None
        S=None
        timer_time=None
        with open(os.path.join(full_path, *["chessboard_dimensions.pickle"]), 'rb') as file:
            chessboard_dimensions=pickle.load(file)
        with open(os.path.join(full_path, *["square_size.pickle"]), 'rb') as file:
            square_size=pickle.load(file)
        with open(os.path.join(full_path, *["S.pickle"]), 'rb') as file:
            S=pickle.load(file)
        with open(os.path.join(full_path, *["timer_time.pickle"]), 'rb') as file:
            timer_time=pickle.load(file)
        return CalibrationParameters(chessboard_dimensions=chessboard_dimensions, square_size=square_size, S=S, timer_time=timer_time)
    
    def __str__(self):
        return "Chessboard dimensions: {}\nSquare size: {}\nS: {}\nTimer time: {}".format(self.chessboard_dimensions, self.square_size, self.S, self.timer_time)