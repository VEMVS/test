import models
from .db import engine

models.Base.metadata.create_all(bind=engine)