from typing import Tuple
from pandas import DataFrame, Series
from scipy.sparse._csr import csr_matrix
from sklearn.base import BaseEstimator

from mlops.utils.data_preparation.encoders import vectorize_features
from mlops.utils.data_preparation.feature_selector import select_features

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_exporter
def export(
    data: Tuple[DataFrame, DataFrame, DataFrame], 
    **kwargs
) -> Tuple[
    csr_matrix, 
    csr_matrix, 
    csr_matrix, 
    Series, 
    Series, 
    Series, 
    BaseEstimator
]:
    ## On Full dataset
    
    # Obtains data frames from given data
    df, df_train, df_val = data
    # Gets target value for the training
    target = kwargs.get('target', 'duration')
    # Gets dicts of data for specified features
    X, _, _ = vectorize_features(select_features(df))
    # Gets target data
    y: Series = df[target]

    ## On splitted data

    # Transform the splitted data
    X_train, X_val, dv = vectorize_features(
        select_features(df_train), 
        select_features(df_val)
    )
    # Gets targets for the splitted data
    y_train = df_train[target]
    y_val = df_val[target]

    return X, X_train, X_val, y, y_train, y_val, dv


@test
def test_dataset(
    X: csr_matrix,
    X_train: csr_matrix,
    X_val: csr_matrix,
    y: Series,
    y_train: Series,
    y_val: Series,
    *args
) -> None:
    assert (
        X.shape[0] == 105870
    ), f"Entire dataset should have 105870 examples, but has {X.shape[0]}"
    assert (
        X.shape[1] == 7027
    ), f"Entire dataset should have 7027 features, but has {X.shape[1]}"
    assert (
        len(y.index) == X.shape[0]
    ), f"Entire dataset should have {X.shape[0]} examples, but has {len(y.index)}"

@test
def test_training_set(
    X: csr_matrix,
    X_train: csr_matrix,
    X_val: csr_matrix,
    y: Series,
    y_train: Series,
    y_val: Series,
    *args
) -> None:
    assert (
        X_train.shape[0] == 54378
    ), f"Train dataset should have 54378 examples, but has {X_train.shape[0]}"
    assert (
        X_train.shape[1] == 5094
    ), f"Train dataset should have 5094 features, but has {X_train.shape[1]}"
    assert (
        len(y_train.index) == X_train.shape[0]
    ), f"Train dataset should have {X_train.shape[0]} examples, but has {len(y_train.index)}"


@test
def test_validation_set(
    X: csr_matrix,
    X_train: csr_matrix,
    X_val: csr_matrix,
    y: Series,
    y_train: Series,
    y_val: Series,
    *args
) -> None:
    assert (
        X_val.shape[0] == 51492
    ), f"Validation dataset should have 51492 examples, but has {X_val.shape[0]}"
    assert (
        X_val.shape[1] == 5094
    ), f"Validation dataset should have 5094 features, but has {X_val.shape[1]}"
    assert (
        len(y_val.index) == X_val.shape[0]
    ), f"Validation dataset should have {X_val.shape[0]} examples, but has {len(y_val.index)}"