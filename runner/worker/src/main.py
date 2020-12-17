from utils import dataset_utils
from utils import trainer
from common.urlconstructor import URLConstructor
from common.rediswq import RedisWQ
from common.status import CmdStatus
import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import pickle


def main():
    base = automap_base()
    engine = create_engine(settings.CONNECTION_STR)
    base.prepare(engine, reflect=True)
    Series = base.classes.project_series
    Predictor = base.classes.project_predictor

    q = RedisWQ(name=settings.QUEUE, host=settings.REDIS_HOST)

    while not q.empty():
        item = q.lease(lease_secs=10, block=True, timeout=2)
        if item is not None:
            series_id = item

            with Session(engine) as session:
                series = session.query(Series).get(series_id)
                dataset = series.dataset
                job = series.project_job
                predictors = series.project_predictor_collection

            for predictor in predictors:
                if predictor.status != CmdStatus.COMITTED:
                    continue
                print(f'Working on predictor {predictor.id}')
                model_file = pickle.loads(predictor.model_file)
                try:
                    df = pickle.loads(dataset)
                    model = trainer.trainer(
                        model_name=model_file['model_name'],
                        config=model_file['hyper_params'],
                        metrics=model_file['eval_metrics'],
                        auto_tune_metric=model_file['auto_tune_metric'],
                        auto_tune=model_file['auto_tune'],
                        max_eval=model_file['max_eval'],
                    )

                    _, target_idx, ts_idx = dataset_utils.str2list(job)
                    metrics, config, tuned_model = model.train(
                        data_df=df,
                        target_idx=target_idx,
                        ts_idx=ts_idx,
                    )
                    predictions, timestamps = model.predict(model_file['next_k_prediction'])
                    model_file.update({
                        'predictions': predictions,
                        'timestamps': timestamps,
                        'metrics': metrics,
                        'config': config,
                    })
                except:
                    status = CmdStatus.EXCEPTION
                else:
                    status = CmdStatus.DONE
                finally:
                    with Session(engine) as session:
                        session.add(predictor)
                        predictor.model_file = pickle.dumps(model_file)
                        predictor.status = status
                        session.commit()

                q.complete(item)
            else:
                print("Waiting for work")

    print("Queue empty, exiting")


if __name__ == '__main__':
    main()
