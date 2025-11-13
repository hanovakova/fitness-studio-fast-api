from functools import wraps


# Define the decorator to handle connection and cursor creation
def run_in_transaction(session_local):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = session_local(expire_on_commit=False)
            try:
                result = func(*args, session=session, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        return wrapper

    return decorator
