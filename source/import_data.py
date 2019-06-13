import pandas as pd
from sqlalchemy import create_engine, DATE
from dateutil.parser import parse

def string_to_date(date_str: str):
    if not date_str:
        return None
    return parse(date_str).date()


def import_source_data():

    path = "/Users/parthbhatt/Parth_Dev/adjusttask/source/performance_metrics.csv"
    engine = create_engine('sqlite:////Users/parthbhatt/Parth_Dev/adjusttask/db.sqlite3', echo=False)

    db_cols = ['recorded_date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue']

    df = pd.read_csv(path, parse_dates=[0], date_parser=string_to_date)#dtype={"recorded_date": Date}

    # print(df)
    (df.rename(columns=dict(zip(df.columns, db_cols))).to_sql('adjust_app_performancemetrics', con=engine, if_exists='append', index=False, index_label=None, dtype={"recorded_date": DATE}))
