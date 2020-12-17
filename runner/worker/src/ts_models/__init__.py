from .AdaptiveAverageNModel import AdaptiveAverageNModel
from .LinearFitModel import LinearFitModel
from .ARIMAModel import ARIMAModel
from .AdaptiveAverageNModel import AdaptiveAverageNModel
from .AdaptiveMaxNModel import AdaptiveMaxNModel
from .FbProphetModel import FbProphetModel
from .LinearFitModel import LinearFitModel
from .LstmLongModel import LstmLongModel
from .LstmModel import LstmModel
from .MaxNModel import MaxNModel
from .NewRandomArrivalModel import NewRandomArrivalModel
from .RandomArrivalModel import RandomArrivalModel
from .LightGBMModel import LightGBMModel
from .XGBoostModel import XGBoostModel

__all__ = [
    'ARIMAModel',
    'AdaptiveAverageNModel',
    'AdaptiveMaxNModel',
    'FbProphetModel',
    'LinearFitModel',
    'LstmLongModel',
    'LstmModel',
    'MaxNModel',
    'NewRandomArrivalModel',
    'RandomArrivalModel',
    'XGBoostModel',
    'LightGBMModel'
]

MODEL_DESCRIPTIONS = {
    "ARIMA": '=> ARIMA',
    'AdaptiveAverageNModel': '=> AdaptiveAverageNModel',
    'AdaptiveMaxNModel': '=> AdaptiveMaxNModel',
    'LinearFitModel': '=> LinearFitModel',
    'LstmLongModel': '=> LstmLongModel',
    'LstmModel': '=> LstmModel',
    'MaxNModel': '=> MaxNModel',
    'NewRandomArrivalModel': '=> NewRandomArrivalModel',
    'RandomArrivalModel': '=> RandomArrivalModel',
}

MODEL_HP_DESCRIPTIONS = {
    'MaxNModel': [
        {
            "name": "latest_n",
            "description": "use the lastest n samples of the sequence for prediction",
            "type": "int",
            "default": 3,
        },
    ]
}
