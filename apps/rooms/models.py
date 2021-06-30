from django.db import models


class Floor(models.Model):
	"""
	Floor represents a hotel floor.

	number: The floor number of the hotel

	"""

	number = models.IntegerField()

	def __str__(self):
		return self.name


class Room(models.Model):
	"""
	Room represents a hotel room.

	number: The room number
	floor: The floor the room is on
	bed_count: How many beds this room has

	"""

	number = models.CharField(max_length=6)
	floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
	bed_count = models.IntegerField()

	def __str__(self):
		return "{}: {}".format(self.floor.number, self.number)


class Bed(models.Model):
	"""
	Bed reprensents a bed type that would be in a room.

	name: Description of the bed
	"""

	bed_choices = (
		('single', 'Single'),
		('twin', 'Twin'),
		('queen', 'Queen'),
		('king', 'King'),
	)
	name = models.CharField(max_length=64, choices=bed_choices)

	def __str__(self):
		return self.get_name_display()
