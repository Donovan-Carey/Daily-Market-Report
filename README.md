# Pre-Market Analyst Report Generator

Automated daily pre-market analyst report delivered to your email at 7 AM.

## Features

- Comprehensive market analysis using OpenAI GPT-4
- Professional newsletter formatting with HTML/CSS
- Automated daily delivery via Gmail
- Scheduled execution using GitHub Actions
- Easy configuration and deployment

## Prerequisites

- GitHub account
- OpenAI API key
- Gmail account with App Password enabled

## Setup Instructions

### 1. Get Your API Keys

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key and save it

#### Gmail App Password
1. Go to your [Google Account](https://myaccount.google.com/)
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security → 2-Step Verification → App passwords
4. Generate an app password for "Mail"
5. Save the 16-character password

### 2. Fork/Clone This Repository

```bash
git clone https://github.com/yourusername/premarket-analyst-report.git
cd premarket-analyst-report
```

### 3. Configure GitHub Secrets

Go to your repository on GitHub:
1. Click Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GMAIL_USER`: Your Gmail address
   - `GMAIL_APP_PASSWORD`: Your Gmail app password
   - `RECIPIENT_EMAIL`: Email where you want to receive reports

### 4. Customize Schedule (Optional)

Edit `.github/workflows/daily-report.yml` to change the time:
```yaml
schedule:
  - cron: '0 12 * * 1-5'  # 7 AM EST (12 PM UTC), Monday-Friday
```

Adjust the cron expression for your timezone.

### 5. Enable GitHub Actions

1. Go to the Actions tab in your repository
2. Enable workflows if prompted
3. The workflow will run automatically at 7 AM daily

### 6. Test Manually

You can trigger a test run:
1. Go to Actions tab
2. Select "Daily Pre-Market Report"
3. Click "Run workflow"

## File Structure

```
premarket-analyst-report/
├── .github/
│   └── workflows/
│       └── daily-report.yml    # GitHub Actions workflow
├── src/
│   ├── generate_report.py      # Main report generation
│   ├── email_sender.py          # Email functionality
│   └── newsletter_template.html # HTML email template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Customization

### Change Report Content
Edit the prompt in `src/generate_report.py` in the `generate_report()` function.

### Modify Email Template
Edit `src/newsletter_template.html` to change the styling and layout.

### Adjust Timing
Modify the cron schedule in `.github/workflows/daily-report.yml`.

## Troubleshooting

### Email Not Sending
- Verify Gmail App Password is correct
- Check that 2FA is enabled on your Google account
- Ensure secrets are properly set in GitHub

### Report Generation Fails
- Verify OpenAI API key is valid
- Check your OpenAI account has credits
- Review workflow logs in GitHub Actions

### Wrong Timezone
- GitHub Actions uses UTC timezone
- Convert your desired time to UTC for cron schedule
- EST = UTC - 5, EDT = UTC - 4

## Cost Estimates

- OpenAI API: ~$0.10-0.30 per report (GPT-4)
- GitHub Actions: Free for public repos
- Gmail: Free

Monthly cost: ~$3-9 for 20 trading days

## License

MIT License - Feel free to modify and use as needed.

## Support

For issues or questions, please open a GitHub issue.
