from model import db

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import concat
from sqlalchemy.dialects.postgresql import INTERVAL

from ..tables import Reading

r = aliased(Reading)

def get_solarpanel_value_stmt(window: int):
    where_condition = (
        (r.device_name == 'SolarMan')
        & (r.reading_timestamp < db.func.now())
        & (r.reading_timestamp > db.func.now() - db.func.cast(concat(window, 'minutes'), INTERVAL))
    )

    select_stmt = (
        select([
            db.func.avg(r.reading_value).label('value')
        ])
        .filter(where_condition)
    )

    return [select_stmt]
