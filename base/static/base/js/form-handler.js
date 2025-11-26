document.addEventListener('DOMContentLoaded', function() {
    const machineTypeSelect = document.getElementById('id_machine_type');
    const specSections = {
        'laser_cutting': document.getElementById('laser_cutting_specs'),
        'press_brake': document.getElementById('press_brake_specs'),
        'tube_laser': document.getElementById('tube_laser_specs'),
    };

    // Function to toggle tube module fields based on checkbox state
    function toggleTubeModuleFields(show) {
        // Get all tube module fields by their name attributes
        const tubeLengthField = document.querySelector('input[name$="tube_module_length"]');
        const tubeDiameterField = document.querySelector('input[name$="tube_module_diameter"]');
        
        // Toggle tube_module_length field and its container
        if (tubeLengthField) {
            const lengthContainer = tubeLengthField.closest('.form-group');
            if (lengthContainer) {
                lengthContainer.style.display = show ? 'block' : 'none';
                // Make sure the input and its label are visible
                if (show) {
                    const coolInput = lengthContainer.querySelector('.coolinput');
                    if (coolInput) coolInput.style.display = 'block';
                    const label = lengthContainer.querySelector('label');
                    if (label) label.style.display = 'block';
                    tubeLengthField.style.display = 'block';
                }
            }
        }
        
        // Toggle tube_module_diameter field and its container
        if (tubeDiameterField) {
            const diameterContainer = tubeDiameterField.closest('.form-group');
            if (diameterContainer) {
                diameterContainer.style.display = show ? 'block' : 'none';
                // Make sure the input and its label are visible
                if (show) {
                    const coolInput = diameterContainer.querySelector('.coolinput');
                    if (coolInput) coolInput.style.display = 'block';
                    const label = diameterContainer.querySelector('label');
                    if (label) label.style.display = 'block';
                    tubeDiameterField.style.display = 'block';
                }
            }
        }
    }

    // Setup tube module fields visibility on page load
    function setupTubeModuleFields() {
        const tubeCuttingCheckbox = document.querySelector('input[name$="tube_cutting_module"]');
        if (tubeCuttingCheckbox) {
            // Initial state - hide tube module fields by default
            toggleTubeModuleFields(false);
            
            // Show them if the checkbox is checked
            if (tubeCuttingCheckbox.checked) {
                toggleTubeModuleFields(true);
            }
            
            // Update on change
            tubeCuttingCheckbox.addEventListener('change', function() {
                toggleTubeModuleFields(this.checked);
            });
        }
    }

    function toggleSpecSection(selectedType) {
        // Hide all sections first
        Object.values(specSections).forEach(section => {
            if (section) {
                section.classList.add('spec-form-hidden');
            }
        });

        // Show the relevant section
        const relevantSection = specSections[selectedType];
        if (relevantSection) {
            relevantSection.classList.remove('spec-form-hidden');
            
            // If this is the laser cutting section, set up the tube module fields
            if (selectedType === 'laser_cutting') {
                // Use setTimeout to ensure the DOM is updated before setting up the fields
                setTimeout(setupTubeModuleFields, 0);
            }
        }
    }

    // Initial check on load
    if (machineTypeSelect) {
        toggleSpecSection(machineTypeSelect.value);

        // Update on change
        machineTypeSelect.addEventListener('change', function() {
            toggleSpecSection(this.value);
        });
        
        // Also set up tube module fields if laser cutting is the initial selection
        if (machineTypeSelect.value === 'laser_cutting') {
            setupTubeModuleFields();
        }
    }

    // File validation on form submit
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('id_attachment');
            if (fileInput && fileInput.files.length > 0) {
                if (!validateAndShowFile(fileInput)) {
                    e.preventDefault();
                    return false;
                }
            }
        });
    }
});

function validateAndShowFile(input) {
    const fileInfo = document.getElementById('file-info');
    const errorElement = document.getElementById('file-error');
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    const allowedTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image/jpeg',
        'image/png'
    ];
        
    // Reset previous messages
    if (errorElement) errorElement.style.display = 'none';
    if (fileInfo) fileInfo.textContent = '';
        
    if (input.files.length > 0) {
        const file = input.files[0];
            
        // Check file size
        if (file.size > maxSize) {
            if (errorElement) {
                errorElement.textContent = 'Error: File size exceeds 5MB limit.';
                errorElement.style.display = 'block';
            }
            input.value = '';
            return false;
        }
            
        // Check file type
        if (!allowedTypes.includes(file.type)) {
            if (errorElement) {
                errorElement.textContent = 'Error: Invalid file type. Please upload PDF, Word, Excel, or image files.';
                errorElement.style.display = 'block';
            }
            input.value = '';
            return false;
        }
            
        // Show file info
        if (fileInfo) {
            const fileSize = (file.size / (1024 * 1024)).toFixed(2);
            fileInfo.innerHTML = `
                <strong>Selected file:</strong> ${file.name}<br>
                <small>Size: ${fileSize} MB</small>
            `;
        }
    }
        
    return true;
}