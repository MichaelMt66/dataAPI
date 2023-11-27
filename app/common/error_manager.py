from fastapi import HTTPException


def exception_mapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except StopIteration:
            raise HTTPException(status_code=404, detail='out of index')
        except Exception as e:
            ex = f"Exception occurred: {e}"
            raise HTTPException(status_code=404, detail=ex)
    return wrapper
