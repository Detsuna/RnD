import datetime
import json
import logging
import traceback

from .Encoders import ClassJsonEncoder

class JsonFormatter(logging.Formatter) :
    def format(self, record) :
        data = {
            "timestamp": datetime.datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "callsite": f"{record.module}.{record.funcName}({record.lineno})",
            "message": (record.msg + "\n" + "".join(traceback.format_exception(*record.exc_info))) if record.exc_info else record.msg,
            "properties": record.args if record.args else None
        }
        return json.dumps(data, cls=ClassJsonEncoder)
