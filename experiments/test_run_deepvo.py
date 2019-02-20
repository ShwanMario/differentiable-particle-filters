import tensorflow as tf

from methods.deepvo_lstm import DeepVOLSTM
from utils.data_utils import load_data, noisyfy_data, make_batch_iterator, remove_state
from utils.exp_utils import get_default_hyperparams
from keras import backend as K

def train_deepvo():

    # load training data and add noise
    # train_data = load_data(data_path=data_path, filename=task + '_train')
    # noisy_train_data = noisyfy_data(train_data)

    # reset tensorflow graph
    tf.reset_default_graph()

    # instantiate method
    hyperparams = get_default_hyperparams()
    method = DeepVOLSTM(**hyperparams['global'])

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as session:
        # train method and save result in model_path
        K.set_session(session)

        method.fit(session,**hyperparams['train'])


def test_dpf(task='nav01', data_path='../data/100s', model_path='../models/tmp'):

    # load test data
    test_data = load_data(data_path=data_path, filename=task + '_test')
    noisy_test_data = noisyfy_data(test_data)
    test_batch_iterator = make_batch_iterator(noisy_test_data, seq_len=50)

    # reset tensorflow graph
    tf.reset_default_graph()

    # instantiate method
    hyperparams = get_default_hyperparams()
    method = DPF(**hyperparams['global'])

    with tf.Session() as session:
        # load method and apply to new data
        method.load(session, model_path)
        for i in range(10):
            test_batch = next(test_batch_iterator)
            test_batch_input = remove_state(test_batch, provide_initial_state=False)
            result = method.predict(session, test_batch_input, **hyperparams['test'])


if __name__ == '__main__':
    train_deepvo()