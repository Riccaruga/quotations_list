from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Quote(models.Model):
    # Core Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    manager = models.CharField(max_length=200)
    client = models.CharField(max_length=200)

    # Machine Type Selector
    MACHINE_CHOICES = [
        ('laser_cutting', 'Laser Cutting'),
        ('press_brake', 'Press Brake'), 
        ('tube_laser', 'Tube Laser Cutting'),
        ('other', 'Other'),
    ]
    machine_type = models.CharField(max_length=50, choices=MACHINE_CHOICES)

    # Status and Other Fields
    completed = models.BooleanField(default=False)
    additional_requirements = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='quote_attachments/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_machine_type_display()}"

    def get_spec_model(self):
        """Returns the related specification object based on machine_type."""
        if self.machine_type == 'other':
            return None
        if self.machine_type == 'laser_cutting':
            # Note: This relies on the default related name (model_name.lower())
            return self.lasercuttingspec
        elif self.machine_type == 'press_brake':
            return self.pressbrakespec
        elif self.machine_type == 'tube_laser':
            return self.tubelaserspec
        return None

# Signal to delete file when Quote object is deleted
@receiver(post_delete, sender=Quote)
def quote_post_delete_handler(sender, instance, **kwargs):
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)


# --- Dedicated Specification Models ---

class LaserCuttingSpec(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    working_area = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3000x1500"
    laser_source_power = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3000W"
    compressor = models.BooleanField(default=False)
    stabilizer = models.BooleanField(default=False)
    bevel_laser_head = models.BooleanField(default=False)
    interchangeable_tables = models.BooleanField(default=False)
    cabinet_protection = models.BooleanField(default=False)
    tube_cutting_module = models.BooleanField(default=False)
    tube_module_length = models.CharField(max_length=200, blank=True, null=True)  
    tube_module_diameter = models.CharField(max_length=200, blank=True, null=True)

class PressBrakeSpec(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    bending_capacity = models.CharField(max_length=200, blank=True, null=True)  # e.g. "125 t"
    working_length = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3200 mm"
    
    CNC_CHOICES = [
        ('DA_53T', 'Delem DA-53T'),
        ('DA_69T', 'Delem DA-69T'),
        ('DA_66T', 'Delem DA-66T'),
    ]
    CNC_type = models.CharField(max_length=200, blank=True, null=True, choices=CNC_CHOICES)
    
    AXIS_CHOICES = [
        ('6_1', '6+1 Axis'),
        ('4_1', '4+1 Axis'),
    ]
    axis_type = models.CharField(max_length=200, blank=True, null=True, choices=AXIS_CHOICES)

class TubeLaserSpec(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    tube_length = models.CharField(max_length=200, blank=True, null=True)  # e.g. "6000 mm"
    tube_diameter = models.CharField(max_length=200, blank=True, null=True)  # e.g. "300 mm"
    length_of_unloading_table = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3000 mm"
    laser_source_power = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3000W"
    
    LOADING_CHOICES = [
       ('automatic', 'Automatic'),
       ('semi_automatic', 'Semi-Automatic'),
       ('manual', 'Manual'),
    ]
    loading_type = models.CharField(max_length=20, choices=LOADING_CHOICES, blank=True, null=True)
    
    two_chucks = models.BooleanField(default=False)
    three_chucks = models.BooleanField(default=False)
    bevel_laser_head = models.BooleanField(default=False)