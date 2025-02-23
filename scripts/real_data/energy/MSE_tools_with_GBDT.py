import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from tqdm import tqdm

def load_datasets_for_GeneralizedLinearRegression(dim=2000):
    """
    加载数据，方便后续进行各类回归模型的建立：
    MSE时的线性模型、Lasso模型、Ridge模型、ElasticNet模型
    :return:
    """
    X_train = np.load('X_train.npy', allow_pickle=True)[:,0:dim]
    y_train = np.load('y_train.npy', allow_pickle=True)[0:dim]
    X_test = np.load('X_test.npy', allow_pickle=True)[:,0:dim]
    y_test = np.load('y_test.npy', allow_pickle=True)[0:dim]
    return X_train, y_train, X_test, y_test



def get_bestKfeatures_indices_as_list(K, list_of_bestK_indices_lists):
    """
    Get the index of the best K features according to list_of_bestK_indices_lists
    :param K:
    :param list_of_bestK_indices_lists:
    :return: bestKIndices as a array
    """
    bestKIndices = list_of_bestK_indices_lists[K - 1]
    return bestKIndices



def extract_certain_features_in_index_array(feature_indices_array, X_train, X_test):
    """
    Return feature matrix selected according to index array.
    :param feature_indices_array:
    :param X_train:
    :param X_test:
    :return:X_train_extracted, X_test_extracted
    """
    X_train_extracted = X_train[:, feature_indices_array]
    X_test_extracted = X_test[:, feature_indices_array]

    return X_train_extracted, X_test_extracted



def get_MSE_value_for_certain_features(indexArray):
    """
    使用变量索引内的各变量进行线性回归，检测效果
    :param indexArray:
    :return:mse值
    """
    # 获得所需变量
    X_train, y_train, X_test, y_test = load_datasets_for_GeneralizedLinearRegression()
    X_train_extracted, X_test_extracted = extract_certain_features_in_index_array(indexArray, X_train, X_test)

    gbdt = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    # 训练模型
    gbdt.fit(X_train_extracted, y_train)
    predictions = gbdt.predict(X_test_extracted)

    mse = mean_squared_error(y_test, predictions)

    return mse



def get_MSE_list_for_BestKFeatures(list_of_bestK_indices_lists):
    """
    calculate and return all MSE values for all index lists in list_of_bestK_indices_lists
    :return:MSE list
    """
    from parameters import data_dim

    MSE_list = []

    for K in tqdm(range(1, data_dim+1)):

        indexArray = get_bestKfeatures_indices_as_list(K, list_of_bestK_indices_lists)
        mse = get_MSE_value_for_certain_features(indexArray)
        MSE_list.append(mse)

    return MSE_list





