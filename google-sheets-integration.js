// Google Sheets Integration for Nigela AI Beta Signups
// This script sends form submissions directly to Google Sheets

// Replace this with your Google Sheets Web App URL
const GOOGLE_SHEETS_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';

// Enhanced form submission with Google Sheets integration
async function submitToGoogleSheets(email) {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('timestamp', new Date().toISOString());
    formData.append('source', 'nigela_beta_landing');
    formData.append('location', 'Mumbai');
    formData.append('userAgent', navigator.userAgent);
    formData.append('referrer', document.referrer);

    try {
        const response = await fetch(GOOGLE_SHEETS_URL, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            return { success: true };
        } else {
            throw new Error('Network response was not ok');
        }
    } catch (error) {
        console.error('Error submitting to Google Sheets:', error);
        return { success: false, error: error.message };
    }
}

// Replace the existing form handler in your HTML with this:
function setupGoogleSheetsIntegration() {
    document.getElementById('signupForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const emailInput = document.getElementById('emailInput');
        const submitButton = document.getElementById('signupButton');
        const statusMessage = document.getElementById('statusMessage');
        
        const email = emailInput.value.trim();
        
        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showStatus('Please enter a valid email address', 'error');
            return;
        }
        
        // Show loading
        submitButton.disabled = true;
        submitButton.textContent = 'Joining...';
        
        try {
            // Submit to Google Sheets
            const result = await submitToGoogleSheets(email);
            
            if (result.success) {
                // Success
                showStatus('Welcome to Nigela AI Beta! Check your email.', 'success');
                emailInput.value = '';
                
                // Also store locally as backup
                const signups = JSON.parse(localStorage.getItem('nigela_beta_signups') || '[]');
                if (!signups.includes(email)) {
                    signups.push({
                        email: email,
                        timestamp: new Date().toISOString(),
                        source: 'beta_landing'
                    });
                    localStorage.setItem('nigela_beta_signups', JSON.stringify(signups));
                }
            } else {
                throw new Error(result.error || 'Submission failed');
            }
            
        } catch (error) {
            console.error('Signup error:', error);
            showStatus('Something went wrong. Please try again.', 'error');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Join Beta';
        }
    });
}

function showStatus(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            statusMessage.style.display = 'none';
        }, 5000);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', setupGoogleSheetsIntegration);
