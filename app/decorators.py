import logging
from functools import wraps
from sqlalchemy.exc import IntegrityError

def commit_or_rollback(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        self = args[0]
        if not hasattr(self, "db"):
            raise AttributeError("Function decorated with @commit_or_rollback must be a method with a 'db' attribute.")
        result = func(*args, **kwargs)
        try: 
            self.db.commit()
        except Exception as e: 
            logging.error(f'Failed data insertion in {func.__name__} : {e}')
            self.db.rollback()
        except IntegrityError as ie:
            logging.error(f'Integrity error in {func.__name__} : {ie}')
            self.db.rollback()
        return result 
    return wrapper
