from sklearn.model_selection import train_test_split
import pickle
import numpy as np


class PreProcessor:
    def split_train_test(self, dataset, test_percentage, random_seed=7):
        """ Handles all preprocessing steps. """

        # Clean data and eliminate outliers
        dataset = self.clean_data(dataset)

        # Feature selection
        dataset = self.select_features(dataset)

        # Split into train and test
        X_train, X_test, Y_train, Y_test = self.__prepare_holdout(dataset, test_percentage, random_seed)

        # Normalize/standardize
        X_train, X_test = self.scale_data(X_train, X_test)

        return X_train, X_test, Y_train, Y_test

    def clean_data(self, dataset):
        # Implement data cleaning logic here
        return dataset

    def select_features(self, dataset):
        # Implement feature selection logic here
        return dataset

    def scale_data(self, X_train, X_test):
        """ data normalization/standardization. """
        scaler = pickle.load(open('./MachineLearning/scalers/minmax_scaler_diabetes.pkl', 'rb'))
        reescaled_X_train = scaler.transform(X_train)
        return reescaled_X_train

    def __prepare_holdout(self, dataset, test_percentage, random_seed):
        """ data splitting for model training. """
        dados = dataset.values
        X = dados[:, 0:-1]
        Y = dados[:, -1]
        return train_test_split(X, Y, test_size=test_percentage, random_state=random_seed)



    def prepare_from_form(form):
        """ prepare data received from front """
        X_input = np.array([form.age,
                            form.sex,
                            form.cp,
                            form.trestbps,
                            form.chol,
                            form.fbs,
                            form.restecg,
                            form.thalach,
                            form.exang,
                            form.oldpeak,
                            form.slope,
                            form.ca,
                            form.thal
                            ])
        # Faremos o reshape para que o modelo entenda que estamos passando
        X_input = X_input.reshape(1, -1)
        return X_input
