from .DeepModel import DeepModel
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM
from tensorflow.keras.layers import Dense


class LSTMC(DeepModel):

    def __init__(self, *args, **kwargs):
        super(LSTMC, self).__init__(*args, **kwargs)

    @property
    def model_name(self):
        return str(self.__class__.__name__)

    def build_model(self):
        self.model = None

        self.model = Sequential()
        self.model.add(Embedding(len(self.vocab) + 1, self.word_embed_dim,
                                 input_length=self.max_seq_length, weights=[self.get_embedding_matrix()], trainable=False))
        self.model.add(LSTM(self.word_embed_dim))

        self.model.add(Dense(self.num_classes, activation='sigmoid'))
