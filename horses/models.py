from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

# This is the model for the Jockey (name, age)
class Jockey(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

# This is the model for the Racehorse (name, age, breed)
class Racehorse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    breed = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
# This is the model for the Race (name, date, location, 
# track_configuration, track_condition, classification, season, track_length, track_surface)
class Race(models.Model):
    class TrackSurface(models.TextChoices):
        DIRT = 'D', 'Dirt'
        TURF = 'T', 'Turf'
        SYNTHETIC = 'S', 'Synthetic'
        OTHER = 'O', 'Other'
    
    class TrackConfiguration(models.TextChoices):
        LEFT_HANDED = 'L', 'Left Handed'
        RIGHT_HANDED = 'R', 'Right Handed'
        STRAIGHT = 'S', 'Straight'

    class TrackCondition(models.TextChoices):
        FAST = 'F', 'Fast'
        FROZEN = 'Z', 'Frozen'
        GOOD = 'G', 'Good'
        HEAVY = 'H', 'Heavy'
        MUDDY = 'M', 'Muddy'
        SLOPPY = 'S', 'Sloppy'
        SLOW = 'L', 'Slow'
        WET_FAST = 'W', 'Wet Fast'
        FIRM = 'FM', 'Firm'
        HARD = 'HD', 'Hard'
        SOFT = 'SF', 'Soft'
        YIELDING = 'YL', 'Yielding'
        STANDARD = 'ST', 'Standard'
        HARSH = 'HR', 'Harsh'
    
    class Classification(models.TextChoices):
        GRADE_1 = 'G1', 'Grade 1'
        GRADE_2 = 'G2', 'Grade 2'
        GRADE_3 = 'G3', 'Grade 3'
        LISTED = 'L', 'Listed'
        HANDICAP = 'H', 'Handicap'
        MAIDEN = 'M', 'Maiden'
        OTHER = 'O', 'Other'

    class Season(models.TextChoices):
        SPRING = 'SP', 'Spring'
        SUMMER = 'SU', 'Summer'
        FALL = 'FA', 'Fall'
        WINTER = 'WI', 'Winter'

    DIRT_CONDITIONS = {'F', 'Z', 'G', 'H', 'M', 'S', 'L', 'W'}
    TURF_CONDITIONS = {'FM', 'G', 'HD', 'SF', 'YL'}
    SYNTHETIC_CONDITIONS = {'ST', 'W', 'S', 'Z', 'HR'}
    
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    track_configuration = models.CharField(max_length=1, choices=TrackConfiguration.choices)
    track_condition = models.CharField(max_length=2, choices=TrackCondition.choices)
    classification = models.CharField(max_length=2, choices=Classification.choices)
    season = models.CharField(max_length=2, choices=Season.choices)
    track_length = models.PositiveIntegerField(help_text="Length in meters")

    track_surface = models.CharField(max_length=1, choices=TrackSurface.choices)

    def __str__(self):
        return f"{self.name} on {self.date}"
    
    def clean(self):
        super().clean()
        if self.track_surface == self.TrackSurface.DIRT and self.track_condition not in self.DIRT_CONDITIONS:
            raise ValidationError({'track_condition': 'Invalid track condition for dirt surface.'})
        elif self.track_surface == self.TrackSurface.TURF and self.track_condition not in self.TURF_CONDITIONS:
            raise ValidationError({'track_condition': 'Invalid track condition for turf surface.'})
        elif self.track_surface == self.TrackSurface.SYNTHETIC and self.track_condition not in self.SYNTHETIC_CONDITIONS:
            raise ValidationError({'track_condition': 'Invalid track condition for synthetic surface.'})
    
# This is the model for the race entry (racehorse, race, jockey, position, is_winner)
class Participation(models.Model):
    racehorse = models.ForeignKey(Racehorse, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    jockey = models.ForeignKey(Jockey, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.PositiveIntegerField()
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.racehorse.name} in {self.race.name} - Position: {self.position} {'(Winner)' if self.is_winner else ''}"
    
    def save(self, *args, **kwargs):
        self.is_winner = self.position == 1
        super().save(*args, **kwargs)
    