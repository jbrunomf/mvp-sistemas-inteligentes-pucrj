class ModelAccuracyAssertion:
    def __init__(self, model, X_test, y_test, threshold=0.8):
        """
        Initialize the ModelAccuracyAssertion class.
        
        :param model: Trained machine learning model
        :param X_test: Test features
        :param y_test: True labels for test data
        :param threshold: Minimum acceptable accuracy
        """
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.threshold = threshold

    def assert_accuracy(self):
        """
        Check if the model's accuracy meets the threshold.
        
        :raises AssertionError: If model accuracy is below the threshold
        """
        accuracy = self.model.score(self.X_test, self.y_test)
        assert accuracy >= self.threshold, f"Model accuracy {accuracy} is below the threshold of {self.threshold}"
        print(f"Model accuracy {accuracy} meets the threshold of {self.threshold}")
