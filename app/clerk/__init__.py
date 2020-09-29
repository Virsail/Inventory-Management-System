from flask import Blueprint

clerk = Blueprint('clerk',__name__)

from . import views,forms