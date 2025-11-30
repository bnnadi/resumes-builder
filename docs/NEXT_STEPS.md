# Next Steps: Using Your New AI-Powered Resume Builder

## ✅ What's Been Implemented

Your resume builder now has complete AI-powered features:

1. **Job Match Analysis** - AI scores resume fit (0-100)
2. **Smart Threshold Gate** - Auto-stops on poor matches (< 70%)
3. **AI Customization** - Tailors resumes to specific jobs
4. **Resume Evaluation** - Compares multiple resumes
5. **Complete Workflow** - Single command from job posting to .docx

## 🚀 Installation (Do These Now)

### Step 1: Install Ollama

```bash
# Install Ollama
brew install ollama

# Start Ollama server (keep this running in a separate terminal)
ollama serve
```

### Step 2: Pull AI Model

```bash
# Download Llama 3.1 model (~4GB)
ollama pull llama3.1

# Verify it worked
ollama list
```

### Step 3: Install Resume Builder

```bash
# Go to project directory
cd /Users/bisikennadi/Projects/resumes-builder

# Activate virtual environment
source venv/bin/activate

# Install updated dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Verify installation
resume-builder --version
# Should show: resume-builder 0.2.0
```

### Step 4: Test Installation

```bash
# Run test script
./test_installation.sh

# Should show all checks passing
```

## 🧪 Test with Sample Job

Create a test job posting:

```bash
cat > ~/Desktop/test-job.txt << 'EOF'
Senior Backend Engineer

We're seeking an experienced Backend Engineer to join our platform team.

Requirements:
- 5+ years Python development
- Django or Flask framework experience
- PostgreSQL database expertise
- AWS experience (EC2, S3, Lambda)
- RESTful API design
- Strong problem-solving skills

Nice to have:
- Docker/Kubernetes
- GraphQL
- Team leadership experience

Responsibilities:
- Design and build scalable APIs
- Optimize database performance
- Mentor junior engineers
- Collaborate with frontend team

Salary: $140K-$180K
Location: Remote
EOF
```

Test the complete workflow:

```bash
resume-builder workflow ~/Desktop/test-job.txt
```

**What happens:**
1. AI analyzes job match (~60 seconds)
2. Shows match score and interview probability
3. If score ≥ 70%, continues to customization
4. AI customizes resume (~3 minutes)
5. Exports to .docx (~3 seconds)
6. Creates complete application package

## 📋 Command Reference

### Complete Workflow (Recommended)
```bash
# Basic usage
resume-builder workflow job-posting.txt

# Custom threshold
resume-builder workflow job-posting.txt --min-score 80

# Force through regardless of score
resume-builder workflow job-posting.txt --force

# Stop after customization (don't export)
resume-builder workflow job-posting.txt --no-export

# Use different model
resume-builder workflow job-posting.txt --model mistral
```

### Individual Commands

**Analyze job match:**
```bash
resume-builder job-match job-posting.txt
resume-builder job-match job-posting.txt --resume path/to/resume.md
resume-builder job-match job-posting.txt --save analysis.md
```

**Customize resume:**
```bash
resume-builder customize job-posting.txt
resume-builder customize job-posting.txt --company Google --base-resume master.md
```

**Evaluate resumes:**
```bash
resume-builder eval
resume-builder eval --search ~/Documents/resumes
```

**Export only (no AI):**
```bash
resume-builder export resume.md --validate --package

# Or use legacy command
export-resume resume.md --validate --package
```

### Help
```bash
# General help
resume-builder --help

# Command-specific help
resume-builder workflow --help
resume-builder job-match --help
resume-builder customize --help
```

## 🎯 Real-World Usage

### Your Typical Workflow

**Before (Manual - 28 minutes):**
1. Read job description (5 min)
2. Assess fit mentally (2 min)
3. Copy resume to Word (1 min)
4. Manually reorder sections (5 min)
5. Rewrite bullets (10 min)
6. Format for ATS (3 min)
7. Create checklist (2 min)

**After (AI-Powered - 5 minutes):**
1. Save job posting to file
2. Run: `resume-builder workflow job-posting.txt`
3. Review output and submit

**Time Saved: 23 minutes per application!**

### Batch Processing Multiple Jobs

```bash
# Save all job postings in a directory
mkdir ~/jobs
# Save each job as: company-name.txt

# Process all jobs
for job in ~/jobs/*.txt; do
    echo "Processing: $job"
    resume-builder workflow "$job" --min-score 70
    echo "---"
done

# Review results directory by directory
```

## ⚙️ Configuration

Edit `config/settings.yaml` to customize:

```yaml
# Change model
ollama:
  model: "mistral"  # faster, smaller
  # or "mixtral"   # slower, more powerful

# Adjust threshold
thresholds:
  minimum_overall: 75  # raise to 75%
  ask_on_borderline: false  # auto-stop on borderline

# Change output location
output:
  base_dir: "~/Documents/job-applications"
```

## 📊 Understanding Match Scores

**Score ranges:**
- **85-100**: Excellent match - definitely apply
- **70-84**: Good match - strong candidate
- **60-69**: Borderline - worth trying for reach companies
- **50-59**: Poor match - low interview probability
- **< 50**: Very poor match - focus elsewhere

**The 70% threshold:**
- Based on typical hiring behavior
- Prevents wasting time on poor-fit roles
- You can override with `--force` flag
- Configurable in settings.yaml

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Check if running
ps aux | grep ollama

# Start if not running
ollama serve &
```

### "Model not found"
```bash
ollama pull llama3.1
```

### Slow generation
```bash
# Use smaller/faster model
resume-builder workflow job.txt --model llama3.1:8b

# Or increase timeout in config
```

### Out of memory
- Close other applications
- Use smaller model (llama3.1 vs mixtral)
- Ensure you have 8GB+ RAM

See `INSTALL_AI.md` for complete troubleshooting.

## 📈 Track Your Success

After using for 10+ applications, analyze:

**What scores led to interviews?**
- Keep a log: score → applied → interview (Y/N)
- Refine your threshold based on results
- Focus on score ranges that convert

**Example tracking:**
```
| Company | Score | Applied | Interview | Offer |
|---------|-------|---------|-----------|-------|
| Google  | 85    | Yes     | Yes       | No    |
| Amazon  | 78    | Yes     | Yes       | Yes   |
| Meta    | 65    | Yes     | No        | -     |
| Apple   | 55    | No      | -         | -     |
```

## 🔄 Updating

Stay up to date:

```bash
# Update Ollama
brew upgrade ollama

# Update models
ollama pull llama3.1

# Update resume-builder (if changes made)
cd /Users/bisikennadi/Projects/resumes-builder
git pull  # if using git
pip install -r requirements.txt
pip install -e .
```

## 📚 Documentation

**Quick reference:**
- `../README.md` - Complete feature overview
- `INSTALL.md` - Detailed installation guide
- `../memory-bank/` - Technical details
- `../config/settings.yaml` - Configuration options

**Get help:**
```bash
resume-builder --help
resume-builder workflow --help
```

## ✨ Tips & Best Practices

### For Best Results

1. **Save clear job postings** - Include requirements, responsibilities, and company info
2. **Trust the threshold** - If score < 70%, it's probably not a good fit
3. **Review AI output** - AI customizes well but always review before submitting
4. **Use --save flag** - Keep analysis for cover letter writing
5. **Batch similar jobs** - Process multiple jobs, then review all at once

### Optimize Your Time

**Use the workflow command** (not individual commands) for complete applications

**Skip poor matches** - Don't force through low scores

**Batch process** - Analyze multiple jobs, focus on high scores

**Keep Ollama running** - Faster subsequent runs

## 🎓 Learning Curve

**First time:** ~10 minutes (includes setup)
**Second time:** ~5 minutes (familiar with output)
**After 5 uses:** ~3 minutes (streamlined workflow)

## 🚀 You're Ready!

Your AI-powered resume builder is ready to use. Start with:

```bash
# 1. Ensure Ollama is running
ollama serve &

# 2. Test with sample job
resume-builder workflow ~/Desktop/test-job.txt

# 3. Use with real job postings
resume-builder workflow path/to/real-job.txt
```

**Questions?** Check:
1. `INSTALL_AI.md` for installation issues
2. `README_AI.md` for usage examples
3. `--help` flags for command options

**Good luck with your job search!** 🎯

---

**Status:** ✅ Ready to Use
**Version:** 0.2.0
**Date:** November 27, 2025

