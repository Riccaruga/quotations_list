from django.db import models

class Quote(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)  # Making it nullable temporarily
    manager = models.CharField(max_length=200)
    client = models.CharField(max_length=200)

    MACHINE_CHOICES = [
        ('laser_cutting', 'Laser Cutting Machine'),
        ('press_brake', 'Press Brake'), 
        ('tube_laser', 'Tube Laser Cutting Machine'),
    ]

    machine_type = models.CharField(max_length=50, choices=MACHINE_CHOICES)

    # Laser cutting
    working_area = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3000x1500"
    laser_source_power = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3000W"
    compressor = models.BooleanField(default=False)
    stabilizer = models.BooleanField(default=False)
    bevel_laser_head = models.BooleanField(default=False)
    

    # Press brake
    bending_capacity = models.CharField(max_length=200, blank=True, null=True)  # e.g. "125 t"
    working_length = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3200 mm"
    
    CNC_CHOICES = [
        ('DA_53T', 'Delem DA-53T'),
        ('DA_69T', 'Delem DA-69T'),
        ('DA_66T', 'Delem DA-66T'),
    ]
    CNC_type = models.CharField(max_length=200, blank=True, null=True, choices=CNC_CHOICES)  # e.g. "Delem DA-53T"
    
    AXIS_CHOICES = [
        ('6_1', '6+1 Axis'),
        ('4_1', '4+1 Axis'),
    ]
    axis_type = models.CharField(max_length=200, blank=True, null=True, choices=AXIS_CHOICES)  # e.g. "6+1 Axis"

    # Tube laser cutting
    tube_length = models.CharField(max_length=200, blank=True, null=True)  # e.g. "6000 mm"
    tube_diameter = models.CharField(max_length=200, blank=True, null=True)  # e.g. "300 mm"
    length_of_unloading_table = models.CharField(max_length=200, blank=True, null=True)  # e.g. "3000 mm"

    LOADING_CHOICES = [
       ('automatic', 'Automatic'),
       ('semi_automatic', 'Semi-Automatic'),
       ('manual', 'Manual'),
   ]
    loading_type = models.CharField(max_length=20, choices=LOADING_CHOICES, blank=True)
    
    two_chucks = models.BooleanField(default=False)
    three_chucks = models.BooleanField(default=False)


    completed = models.BooleanField(default=False)
    additional_requirements = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='quote_attachments/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_machine_type_display()}"

    #class Meta:
    #    ordering = ['completed']
    