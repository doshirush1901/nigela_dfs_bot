// Google Apps Script Code
// Copy this code to Google Apps Script (script.google.com)
// This will receive form submissions and add them to Google Sheets

function doPost(e) {
  try {
    // Get the active spreadsheet (or create one)
    const sheet = getOrCreateSheet();
    
    // Extract form data
    const email = e.parameter.email;
    const timestamp = e.parameter.timestamp || new Date().toISOString();
    const source = e.parameter.source || 'unknown';
    const location = e.parameter.location || '';
    const userAgent = e.parameter.userAgent || '';
    const referrer = e.parameter.referrer || '';
    
    // Validate email
    if (!email || !isValidEmail(email)) {
      return ContentService
        .createTextOutput(JSON.stringify({ error: 'Invalid email' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Check if email already exists
    const existingEmails = sheet.getRange('A:A').getValues().flat();
    if (existingEmails.includes(email)) {
      return ContentService
        .createTextOutput(JSON.stringify({ message: 'Email already registered' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Add new row
    sheet.appendRow([
      email,
      timestamp,
      source,
      location,
      userAgent,
      referrer,
      new Date() // Server timestamp
    ]);
    
    // Send confirmation email (optional)
    sendConfirmationEmail(email);
    
    return ContentService
      .createTextOutput(JSON.stringify({ success: true, message: 'Email registered successfully' }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    console.error('Error in doPost:', error);
    return ContentService
      .createTextOutput(JSON.stringify({ error: 'Server error: ' + error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getOrCreateSheet() {
  const spreadsheetId = 'YOUR_SPREADSHEET_ID'; // Replace with your Google Sheets ID
  let spreadsheet;
  
  try {
    spreadsheet = SpreadsheetApp.openById(spreadsheetId);
  } catch (error) {
    // If spreadsheet doesn't exist, create a new one
    spreadsheet = SpreadsheetApp.create('Nigela AI Beta Signups');
    console.log('Created new spreadsheet:', spreadsheet.getId());
  }
  
  let sheet = spreadsheet.getSheetByName('Beta Signups');
  
  if (!sheet) {
    sheet = spreadsheet.insertSheet('Beta Signups');
    
    // Add headers
    sheet.getRange(1, 1, 1, 7).setValues([
      ['Email', 'Timestamp', 'Source', 'Location', 'User Agent', 'Referrer', 'Server Timestamp']
    ]);
    
    // Format headers
    const headerRange = sheet.getRange(1, 1, 1, 7);
    headerRange.setFontWeight('bold');
    headerRange.setBackground('#f0f0f0');
    
    // Set column widths
    sheet.setColumnWidth(1, 250); // Email
    sheet.setColumnWidth(2, 150); // Timestamp
    sheet.setColumnWidth(3, 120); // Source
    sheet.setColumnWidth(4, 100); // Location
    sheet.setColumnWidth(5, 200); // User Agent
    sheet.setColumnWidth(6, 200); // Referrer
    sheet.setColumnWidth(7, 150); // Server Timestamp
  }
  
  return sheet;
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function sendConfirmationEmail(email) {
  try {
    const subject = 'Welcome to Nigela AI Beta!';
    const body = `
Dear Food Lover,

Thank you for joining the Nigela AI Beta program!

You'll start receiving daily menu emails at 9 PM, featuring:
🎭 Cultural intelligence for festivals and traditions
🌿 Mumbai seasonal awareness and market wisdom  
✍️ Nigella Lawson's authentic voice and warmth
🍽️ Complete daily menus with cooking videos
📱 Screenshot-ready format for your cook

Your first email will arrive tonight at 9 PM.

Questions? Reply to this email or contact us at rushabh@machinecraft.org

Cook with love, eat with joy!

The Nigela AI Team
Mumbai, India

P.S. Add nigela@yourdomain.com to your contacts to ensure our emails reach your inbox.
    `;
    
    MailApp.sendEmail({
      to: email,
      subject: subject,
      body: body,
      name: 'Nigela AI'
    });
    
    console.log('Confirmation email sent to:', email);
  } catch (error) {
    console.error('Error sending confirmation email:', error);
  }
}

// Test function - you can run this to test the setup
function testSetup() {
  const testEmail = 'test@example.com';
  const mockEvent = {
    parameter: {
      email: testEmail,
      timestamp: new Date().toISOString(),
      source: 'test',
      location: 'Mumbai',
      userAgent: 'Test Browser',
      referrer: 'test.com'
    }
  };
  
  const result = doPost(mockEvent);
  console.log('Test result:', result.getContent());
}
