import pickle


class Model:
    def load_model(path):
        """loads model from path"""
        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                model = pickle.load(file)
        else:
            raise Exception('Formato de arquivo não suportado')
        return model

    def predict(model, X_input):
        """ predict from model
        """
        diagnosis = model.predict(X_input)
        return diagnosis
