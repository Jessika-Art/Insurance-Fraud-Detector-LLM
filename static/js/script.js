document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const loadingDiv = document.getElementById('loading');
    const resultsSection = document.getElementById('results-section');
    const scoreValue = document.getElementById('score-value');
    const summaryText = document.getElementById('summary-text');
    const detailedAnalysis = document.getElementById('detailed-analysis');
    const scoreDisplay = document.getElementById('score-display');
    
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading spinner
        loadingDiv.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        
        // Get the file
        const fileInput = document.getElementById('document');
        const file = fileInput.files[0];
        
        if (!file) {
            alert('Please select a file to analyze');
            loadingDiv.classList.add('hidden');
            return;
        }
        
        // Check file type
        const fileType = file.name.split('.').pop().toLowerCase();
        if (fileType !== 'pdf' && fileType !== 'txt') {
            alert('Only PDF and TXT files are supported');
            loadingDiv.classList.add('hidden');
            return;
        }
        
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            // Send the file to the server
            const response = await fetch('/analyze/', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Update the UI with the results
            scoreValue.textContent = result.trustworthiness_score;
            summaryText.textContent = result.summary;
            detailedAnalysis.textContent = result.detailed_analysis;
            
            // Set color based on score
            const score = result.trustworthiness_score;
            let color;
            
            if (score < 30) {
                color = '#e74c3c'; // Red for low scores
            } else if (score < 70) {
                color = '#f39c12'; // Orange for medium scores
            } else {
                color = '#2ecc71'; // Green for high scores
            }
            
            scoreDisplay.style.backgroundColor = color;
            
            // Show results
            resultsSection.classList.remove('hidden');
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing the document. Please try again.');
        } finally {
            // Hide loading spinner
            loadingDiv.classList.add('hidden');
        }
    });
});