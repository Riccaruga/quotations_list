document.addEventListener('DOMContentLoaded', function() {
    const machineTypeSelect = document.getElementById('id_machine_type');
    const specSections = {
        'laser_cutting': document.getElementById('laser_cutting_specs'),
        'press_brake': document.getElementById('press_brake_specs'),
        'tube_laser': document.getElementById('tube_laser_specs'),
    };

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
        }
    }

    // Initial check on load
    if (machineTypeSelect) {
        toggleSpecSection(machineTypeSelect.value);

        // Update on change
        machineTypeSelect.addEventListener('change', function() {
            toggleSpecSection(this.value);
        });
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