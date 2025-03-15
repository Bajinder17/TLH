# Vercel Deployment Instructions

To deploy this project on Vercel, follow these steps to properly set up environment variables:

## 1. Push your code to a Git repository

Make sure your code is pushed to a GitHub, GitLab, or Bitbucket repository.

## 2. Import your project in Vercel

- Go to [Vercel Dashboard](https://vercel.com/dashboard)
- Click "Add New" → "Project"
- Import your Git repository
- Select the project

## 3. Configure Environment Variables

Before you deploy, you must add the following environment variables in the Vercel project settings:

1. In the project configuration page, find the "Environment Variables" section
2. Add the following variables one by one:

| Name | Value | Description |
|------|-------|-------------|
| `REACT_APP_SUPABASE_URL` | `your_supabase_url` | Your Supabase project URL |
| `REACT_APP_SUPABASE_ANON_KEY` | `your_supabase_anon_key` | Your Supabase anonymous key |
| `REACT_APP_VIRUSTOTAL_API_KEY` | `your_virustotal_api_key` | Your VirusTotal API key |

## 4. Deploy your project

- Complete the project import and deploy
- Vercel will build and deploy your application
- Your environment variables will be available to both the frontend and API

## 5. Verify the deployment

After deployment, check that:
- Your application loads correctly
- API endpoints work as expected
- The scanners can connect to external services

## Troubleshooting

If you encounter "Environment Variable references Secret, which does not exist" errors:
- Make sure you've added the environment variables directly in the Vercel UI
- Do not use the `env` section in `vercel.json` to reference non-existent secrets
- For sensitive data, use the "Encrypted" option in the environment variable settings
