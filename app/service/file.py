import pandas as pd
import json
import itertools
from common.error_manager import exception_mapper
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from common.config import Settings


class File:
    name: str
    columns_name: list
    path: str

    @classmethod
    @exception_mapper
    def get_data(cls, pg: int = 1):
        data = (chunk for chunk in pd.read_csv(cls.path, names=cls.columns_name, chunksize=10))
        df = next(itertools.islice(data, pg - 1, None))
        json_df = df.to_json(orient='records')
        return json.loads(json_df)

    @classmethod
    @exception_mapper
    def upload_data(cls):

        settings = Settings()

        url = URL.create(
            drivername="postgresql",
            username=settings.USER_NAME,
            password=settings.PASSWORD,
            host=settings.HOST,
            database=settings.DATABASE
        )

        engine = create_engine(url)

        with engine.connect() as conn:
            df = pd.read_csv(cls.path, names=cls.columns_name)
            rt = df.to_sql(name=cls.name, con=conn, if_exists='replace', schema='public', index=False)
            conn.close()
        return json.loads(f'{{"records inserted": {rt}}}')
