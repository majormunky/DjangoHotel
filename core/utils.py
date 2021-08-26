from django.db import models

def get_object_or_none(model_class, pk):
	try:
		return model_class.objects.get(pk=pk)
	except model_class.DoesNotExist:
		return None
