from models import Survey
from dbindexer.lookups import StandardLookup
from dbindexer.api import register_index

register_index(Survey, {'user__username': StandardLookup()})