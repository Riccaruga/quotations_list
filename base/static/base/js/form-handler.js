document.addEventListener('DOMContentLoaded', function() {
    const machineSelect = document.getElementById('id_machine_type');
    const formGroups = document.querySelectorAll('.form-group');

    // Define which fields belong to which machine type
    const groups = {
        'laser_cutting': [
            'working_area', 'laser_source_power', 'compressor', 'stabilizer', 'bevel_laser_head', 'additional_requirements'
        ],
        'press_brake': [
            'bending_capacity', 'working_length', 'CNC_type', 'axis_type', 'additional_requirements'
        ],
        'tube_laser': [
            'tube_length', 'tube_diameter', 'length_of_unloading_table',
            'loading_type', 'additional_requirements', 'bevel_laser_head', 'two_chucks', 'three_chucks', 'laser_source_power'
        ]
    };

    // Always show these fields
    const alwaysShow = ['title', 'manager', 'client', 'machine_type'];
    
    alwaysShow.forEach(field => {
        const element = document.getElementById(`id_${field}`);
        if (element) {
            const wrapper = element.closest('.form-group');
            if (wrapper) wrapper.style.display = 'block';
        }
    });

    function updateFormFields() {
        const selectedType = machineSelect ? machineSelect.value : '';

        // Hide all dynamic fields first
        Object.values(groups).flat().forEach(field => {
            const element = document.getElementById(`id_${field}`);
            if (element) {
                const wrapper = element.closest('.form-group');
                if (wrapper) wrapper.style.display = 'none';
            }
        });

        // Show only fields for selected machine type
        if (selectedType && groups[selectedType]) {
            groups[selectedType].forEach(field => {
                const element = document.getElementById(`id_${field}`);
                if (element) {
                    const wrapper = element.closest('.form-group');
                    if (wrapper) wrapper.style.display = 'block';
                }
            });
        }
    }

    if (machineSelect) {
        machineSelect.addEventListener('change', updateFormFields);
        updateFormFields(); // Run once on load
    }
});
