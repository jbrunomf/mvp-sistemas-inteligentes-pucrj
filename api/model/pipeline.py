import numpy as np
import pickle


class Pipeline:

    def load(path):
        """
        load pipelines
        """
        with open(path, 'rb') as file:
            pipeline = pickle.load(file)
        return pipeline
