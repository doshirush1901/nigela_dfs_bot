# 🚀 Nigela AI Landing Page - Deployment Guide

## 📋 **What You Have Ready**

✅ **Enhanced Landing Page** (`minimal-landing.html`)  
✅ **Google Sheets Integration** (`google-sheets-integration.js`)  
✅ **Google Apps Script** (`google-apps-script.js`)  
✅ **Complete Features & Contact Info**  

## 🌐 **Step 1: Deploy Your Website**

### Option A: Netlify (Recommended - Free)
1. Go to [netlify.com](https://netlify.com)
2. Create account and click "Add new site"
3. Drag and drop your `minimal-landing.html` file
4. Your site will be live at: `https://random-name.netlify.app`
5. **Custom domain:** Go to Domain settings → Add custom domain

### Option B: Vercel (Also Free)
1. Go to [vercel.com](https://vercel.com)
2. Import your project or upload file
3. Deploy instantly
4. Custom domain available

### Option C: GitHub Pages (Free)
1. Create GitHub repository
2. Upload `minimal-landing.html` (rename to `index.html`)
3. Enable GitHub Pages in settings
4. Live at: `https://yourusername.github.io/repository-name`

## 📊 **Step 2: Set Up Google Sheets Integration**

### Create Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com)
2. Create new spreadsheet
3. Name it "Nigela AI Beta Signups"
4. Copy the Spreadsheet ID from URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

### Set Up Google Apps Script
1. Go to [script.google.com](https://script.google.com)
2. Create new project
3. Replace default code with content from `google-apps-script.js`
4. **Update line 30:** Replace `YOUR_SPREADSHEET_ID` with your actual ID
5. **Deploy as Web App:**
   - Click Deploy → New deployment
   - Type: Web app
   - Execute as: Me
   - Who has access: Anyone
   - Copy the Web App URL

### Connect Website to Google Sheets
1. Open your `minimal-landing.html`
2. Find line with `GOOGLE_SHEETS_URL`
3. Replace with your Web App URL
4. Re-upload to your hosting service

## 🎯 **Step 3: Test Your Setup**

### Test Email Collection
1. Visit your live website
2. Enter a test email
3. Check your Google Sheet - new row should appear
4. Check if confirmation email was sent

### Test Responsiveness
- Desktop: Full layout with MacBook + phone + watch
- Tablet: Stacked layout
- Mobile: Optimized single column

## 📧 **Step 4: Email System Setup**

### For Beta Testing
Your Google Sheet now collects:
- Email addresses
- Timestamps
- Source tracking
- User location
- Browser info

### To Start Sending Emails
1. Export emails from Google Sheets
2. Import into your existing Nigela email system
3. Or use Gmail/Mailchimp for manual sending

## 🔧 **Step 5: Domain & SSL**

### Get Custom Domain
1. **Recommended:** `nigela.ai` or `nigelaai.com`
2. Purchase from Namecheap, GoDaddy, or Google Domains
3. Point domain to your hosting service
4. SSL certificate automatically provided

### Email Setup
1. Set up `hello@yourdomain.com` 
2. Forward to `rushabh@machinecraft.org`
3. Update contact info in website if needed

## 📈 **Step 6: Analytics (Optional)**

### Google Analytics
Add this before `</head>` in your HTML:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🎉 **Your Website Features**

✅ **MacBook mockup** showing real Nigela email  
✅ **Phone mockup** with detailed email content  
✅ **Smartwatch notification** from Nigela  
✅ **Key features** section explaining value  
✅ **Why choose Nigela** with benefits  
✅ **Contact information** with your email  
✅ **Google Sheets** email collection  
✅ **Mobile responsive** design  
✅ **Clean black/white** aesthetic  

## 🔗 **Quick Launch Checklist**

- [ ] Deploy website to hosting service
- [ ] Set up Google Sheets integration
- [ ] Test email collection
- [ ] Get custom domain (optional)
- [ ] Set up email forwarding
- [ ] Test on all devices
- [ ] Share beta signup link!

## 🚀 **Ready to Launch!**

Your Nigela AI landing page is production-ready with:
- Professional design showing actual product
- Working email collection system
- Complete feature descriptions
- Contact information
- Mobile optimization

**Example URLs after deployment:**
- Netlify: `https://nigela-ai.netlify.app`
- Vercel: `https://nigela-ai.vercel.app`
- Custom: `https://nigela.ai`

**Start collecting beta signups immediately!** 🎯✨
