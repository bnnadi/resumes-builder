# Skills Inventory Feature

## Overview

The Skills Inventory feature allows you to maintain a central database of all your skills. When customizing resumes for specific jobs, the AI will intelligently suggest relevant skills from your inventory based on the job description.

## Key Benefits

1. **Centralized Management**: Maintain all your skills in one place
2. **Intelligent Matching**: AI suggests skills that match the job description
3. **Evidence-Based Adding**: Skills are only added if there's proof in your work experience
4. **Maintains Accuracy**: Never fabricates skills - only uses what you've verified

## Setup

### 1. Configure Your Skills Inventory

Edit `config/skills_inventory.yaml` with all your genuine skills:

```yaml
programming_languages:
  - Python
  - JavaScript
  - TypeScript

web_frameworks:
  - React
  - Node.js
  - Django
  - FastAPI

cloud_platforms:
  - AWS
  - Google Cloud Platform

# ... add more categories and skills
```

**Important**: Only add skills you genuinely have experience with. The system trusts that everything in this file is accurate.

### 2. Verify Installation

```bash
# Check that the CLI is available
resume-skills --help

# List all your skills
resume-skills list

# See total count
resume-skills categories
```

## Usage

### Managing Your Skills Inventory

#### List All Skills
```bash
resume-skills list
```

This shows all skills organized by category with counts.

#### View Specific Category
```bash
resume-skills show programming_languages
resume-skills show cloud_platforms
```

#### Add New Skill
```bash
resume-skills add programming_languages "Rust"
resume-skills add cloud_platforms "Digital Ocean"
```

#### Find a Skill
```bash
resume-skills find "Docker"
resume-skills find "React"
```

#### List Categories
```bash
resume-skills categories
```

### Testing Job Matches

Before customizing a resume, check which skills match a job:

```bash
resume-skills match /path/to/job_posting.txt
```

Example output:
```
✅ Found 10 matching skills from your inventory:

Cloud Platforms:
  • AWS (relevance: 96%)

Programming Languages:
  • Python (relevance: 48%)

Web Frameworks:
  • React (relevance: 48%)
  • Django (relevance: 48%)
```

### Resume Customization with Skills

When you run resume customization, the system automatically:

1. **Extracts** current skills from your base resume
2. **Analyzes** the job description
3. **Matches** skills from your inventory to the job
4. **Suggests** relevant skills to the AI
5. **AI decides** whether to add each skill based on work experience evidence

#### Example Workflow

```bash
# 1. Check what skills match
resume-skills match job_posting.txt

# 2. Run customization (assuming you have the AI workflow set up)
# The skills suggestions are automatically included
resume-customize job_posting.txt --company "TechCorp"

# 3. Review the customized resume
# Skills were added ONLY if there was evidence in your experience
```

## How It Works

### Matching Algorithm

The system uses intelligent matching to find relevant skills:

1. **Exact Matching**: Direct keyword matches (e.g., "Python" in job → "Python" in inventory)
2. **Variant Matching**: Handles common variations (e.g., "NLP" ↔ "Natural Language Processing")
3. **Relevance Scoring**: Scores based on frequency in job description
4. **Prioritization**: Most relevant skills are suggested first (up to 8)

### AI Integration

When customizing a resume, the AI sees:

```
### Skills from Your Inventory (Available to Add)

**Web Frameworks:**
  - Django (relevance: 48%)
  - FastAPI (relevance: 48%)

**Cloud Platforms:**
  - AWS (relevance: 48%)

INSTRUCTIONS FOR SKILL ENHANCEMENT:
- You MAY add these skills ONLY if you can find clear evidence in Professional Experience
- Review each experience bullet to confirm skill usage before adding
- If uncertain or no evidence exists, do NOT add the skill
```

The AI then:
- ✅ Reviews your work experience
- ✅ Adds skills ONLY if there's proof you used them
- ❌ Documents skills as gaps if no evidence exists
- ❌ Never fabricates or assumes skills

## Example Scenarios

### Scenario 1: Skills with Evidence

**Job requires**: Docker, Kubernetes  
**Your inventory**: Has both  
**Your experience**: "Deployed containerized apps using Docker and Kubernetes"  
**Result**: ✅ Both skills added to Core Skills section

### Scenario 2: Skills without Evidence

**Job requires**: TensorFlow, PyTorch  
**Your inventory**: Has both  
**Your experience**: No mention of either  
**Result**: ❌ Not added to resume, marked as gaps in analysis

### Scenario 3: Partial Evidence

**Job requires**: React, Vue.js, Angular  
**Your inventory**: Has all three  
**Your experience**: "Built frontend with React"  
**Result**: ✅ React added, ❌ Vue.js and Angular marked as gaps

### Scenario 4: Conditional Skills (React Native Example)

**Job requires**: Backend engineer, no mobile mentioned  
**Your inventory**: Has React Native with conditional note  
**Your experience**: "Built 3 React Native mobile apps"  
**Result**: ❌ Not added - mobile not relevant to this role, marked as gap

**Job requires**: Full-stack engineer with mobile experience  
**Your inventory**: Has React Native with conditional note  
**Your experience**: "Built 3 React Native mobile apps"  
**Result**: ✅ React Native added - mobile explicitly required AND you have experience

**Job requires**: Engineering Manager  
**Your inventory**: Has React Native with conditional note  
**Your experience**: "Led team of 5 mobile engineers using React Native"  
**Result**: ✅ React Native added - management experience counts even if not IC work

## Conditional Skills

Some skills should only appear on your resume in specific contexts, even if you have experience with them.

### What Are Conditional Skills?

Conditional skills are skills that:
- You genuinely have experience with
- But aren't relevant to every role
- Should only be added when specific conditions are met

### When to Use Conditional Notes

Add conditional notes in your `skills_inventory.yaml` for skills that:

1. **Niche or specialized**: Mobile development, blockchain, embedded systems
2. **Management context**: You've managed teams using the technology but don't do IC work
3. **Outdated but occasionally relevant**: Legacy technologies
4. **Domain-specific**: Only relevant in certain industries

### How to Add Conditional Notes

In your `skills_inventory.yaml`:

```yaml
mobile_development:
  - React Native  # Add only if mobile dev mentioned in JD or managing mobile teams
  - iOS Development  # Add only if iOS specifically mentioned
  - Android Development  # Add only if Android specifically mentioned
```

The AI will read these comments and apply the conditions automatically.

### Example Conditions

**Mobile Development:**
```yaml
# Add only if mobile development mentioned in JD OR managing mobile teams
```

**Legacy Technologies:**
```yaml
# Add only if explicitly mentioned in JD (legacy system maintenance)
```

**Management Skills:**
```yaml
# Add if managing teams OR job is management role
```

**Domain-Specific:**
```yaml
# Add only if fintech/finance industry mentioned
```

### Why Use Conditional Skills?

1. **Relevance**: Don't clutter resume with irrelevant skills
2. **Focus**: Keep resume focused on the specific role
3. **Honesty**: Acknowledge you have the skill without overstating
4. **Flexibility**: Same inventory works for different role types

### Real-World Example

You've built React Native apps but are applying for a backend-focused role:

**Without conditional note**: React Native gets added because you have experience
→ Resume looks unfocused, interviewer asks mobile questions

**With conditional note**: React Native not added because JD doesn't mention mobile
→ Resume stays focused on backend, better impression

Later, you apply for a full-stack role with mobile:

**Same inventory, different JD**: React Native now gets added because JD mentions mobile
→ Skill is relevant and demonstrated

### Detailed React Native Example

Let's walk through a complete real-world scenario with React Native.

#### Your Background
- Built 3 production React Native apps
- Published apps to iOS App Store and Google Play
- Led mobile team of 2 developers for 6 months

#### Case 1: Backend Engineer Role (No Mobile)

**Job Description:**
```
Senior Backend Engineer
- Build scalable APIs with Python/Node.js
- Design microservices architecture
- Work with PostgreSQL, Redis
- Deploy on AWS
```

**Result:** ❌ React Native NOT Added

**Why?**
- Job doesn't mention mobile development
- Role is backend-focused
- Even though you have React Native experience, it's not relevant

**Resume Output:**
```markdown
## Core Skills
**Backend**: Python, Node.js, Microservices
**Databases**: PostgreSQL, Redis
**Cloud**: AWS
```

#### Case 2: Full-Stack Engineer Role (With Mobile)

**Job Description:**
```
Full-Stack Engineer
- Build web and mobile applications
- React for web, React Native for mobile
- Node.js backend
```

**Result:** ✅ React Native ADDED

**Why?**
- Job explicitly mentions "mobile" and "React Native"
- Your experience matches the requirement
- Conditional requirement is met

**Resume Output:**
```markdown
## Core Skills
**Frontend**: React, React Native
**Mobile**: Mobile Development, Cross-Platform Development
**Backend**: Node.js
```

#### Case 3: Engineering Manager Role

**Job Description:**
```
Engineering Manager
- Lead team of 8 engineers
- Oversee web and mobile development
- React, React Native preferred
```

**Result:** ✅ React Native ADDED

**Why?**
- You led a mobile team (management experience)
- Job is management role overseeing mobile teams
- Conditional requirement met (managing mobile teams)

**Resume Output:**
```markdown
## Core Skills
**Leadership**: Technical Leadership, Team Management
**Mobile Technologies**: React Native, Mobile Development
```

#### Decision Tree

```
Is React Native in your inventory?
├─ No → Skip
└─ Yes → Does JD mention mobile/React Native?
    ├─ Yes → Do you have work experience with it?
    │   ├─ Yes → ✅ ADD to resume
    │   └─ No → ❌ Mark as gap
    └─ No → Did you manage mobile teams?
        ├─ Yes → ✅ ADD to resume (management context)
        └─ No → ❌ Don't add (not relevant)
```

### Adding Your Own Conditional Skills

#### Step 1: Identify Conditional Skills

Ask yourself:
- Is this skill relevant to EVERY role I apply for?
- Should this only appear in specific contexts?

Examples:
- ✅ Python: Core skill, add to most roles
- ❌ React Native: Only for mobile/full-stack/management roles
- ❌ Blockchain: Only for Web3/crypto roles
- ❌ COBOL: Only for legacy system maintenance

#### Step 2: Add to Inventory with Note

```yaml
mobile_development:
  - React Native  # Add only if mobile dev mentioned in JD or managing mobile teams

blockchain:
  - Solidity  # Add only if Web3/blockchain explicitly mentioned
  - Ethereum  # Add only if blockchain role

legacy_systems:
  - COBOL  # Add only if legacy system maintenance mentioned
```

#### Step 3: Document Your Experience

Make sure your base resume has bullets proving you used these skills:

```markdown
## Professional Experience

### Software Engineer | TechCo | 2020-2024

- Built 3 production React Native apps with 100K+ downloads
- Led mobile team of 2 engineers through agile sprints
- Published apps to iOS App Store and Google Play
```

#### Step 4: Test It

```bash
# Test with a mobile-focused job
resume-skills match mobile_job.txt
# Should show React Native

# Test with a backend-focused job  
resume-skills match backend_job.txt
# May not show React Native depending on JD
```

### Common Conditional Skill Patterns

**Pattern 1: Niche Technologies**
```yaml
blockchain:
  - Solidity  # Add only if Web3/blockchain mentioned
  - Smart Contracts  # Add only if DeFi/blockchain mentioned
```

**Pattern 2: Platform-Specific**
```yaml
mobile_development:
  - iOS Development  # Add only if iOS specifically mentioned
  - Swift  # Add only if iOS role
  - Android Development  # Add only if Android specifically mentioned
  - Kotlin  # Add only if Android role
```

**Pattern 3: Management Context**
```yaml
leadership_technologies:
  - React Native  # Add if managing mobile teams
  - Kubernetes  # Add if managing DevOps teams
  - Machine Learning  # Add if managing ML teams
```

**Pattern 4: Legacy/Maintenance**
```yaml
legacy_systems:
  - COBOL  # Add only if legacy maintenance mentioned
  - Perl  # Add only if explicitly required
```

**Pattern 5: Domain-Specific**
```yaml
fintech:
  - Payment Processing  # Add only for fintech/payment roles
  - Financial Systems  # Add only for finance industry
```

### When NOT to Use Conditional Skills

Don't use conditional notes for:
- **Core skills** you want on every resume (Python, Git, etc.)
- **Universal skills** relevant to all roles (Communication, Problem Solving)
- **Foundational skills** in your field (JavaScript for web devs)

Use them for:
- **Specialized skills** not always relevant
- **Platform-specific** skills (iOS, Android)
- **Domain-specific** skills (Blockchain, FinTech)
- **Management-context** skills

## Best Practices

### 1. Keep Inventory Updated
```bash
# After learning new skills, add them
resume-skills add ai_machine_learning "LangChain"
resume-skills add devops_ci_cd "ArgoCD"
```

### 2. Use Consistent Names
- ✅ "JavaScript" (consistent)
- ❌ "JS", "Javascript", "java script" (variations)

The system handles some variants, but consistency helps.

### 3. Organize by Category
Group related skills in appropriate categories:
- `programming_languages`: Python, Java, Go
- `web_frameworks`: React, Django, Flask
- `cloud_platforms`: AWS, GCP, Azure

### 4. Be Honest
Only add skills you genuinely have. The system relies on accuracy.

### 5. Review Suggestions
Before submitting a customized resume:
1. Check which skills were added
2. Verify each has supporting evidence in your experience
3. Remove any that seem questionable

## Customizing Categories

You can add new categories to `config/skills_inventory.yaml`:

```yaml
blockchain:
  - Ethereum
  - Solidity
  - Web3.js

mobile_development:
  - React Native
  - Swift
  - Kotlin
```

The system automatically:
- Reads new categories
- Maps them to existing resume categories when possible
- Creates new categories in customized resumes when needed

## Troubleshooting

### "Skills inventory not found" Error

```bash
❌ Error: Skills inventory not found: config/skills_inventory.yaml
```

**Solution**: Create the file:
```bash
cp config/skills_inventory.yaml.example config/skills_inventory.yaml
# Edit with your skills
```

### No Skills Match Job Description

```bash
❌ No skills from your inventory found in this job description.
```

**Possible reasons**:
1. Job uses different terminology (e.g., "containerization" vs "Docker")
2. Your inventory needs more skills
3. The job requires skills you don't have

**Solutions**:
- Add relevant skills to inventory
- Use variations (system handles some automatically)
- Accept it's not a good match

### Skills Not Being Added to Resume

**Why**: AI couldn't find evidence in your work experience.

**What to do**:
1. Review your base resume
2. Add bullets showing you used those skills
3. Run customization again

## Advanced Usage

### Batch Testing Multiple Jobs

```bash
# Test all jobs in a directory
for job in jobs/*.txt; do
  echo "Testing $job"
  resume-skills match "$job"
  echo "---"
done
```

### Finding Skill Gaps

```bash
# Match against job
resume-skills match target_job.txt > matched_skills.txt

# Review what's missing
resume-skills list | diff - matched_skills.txt
```

### Skills Coverage Report

```bash
# See how many of your skills match
resume-skills match job.txt | grep "Total:" 
```

## Integration with Existing Workflow

The skills feature integrates seamlessly:

```
Old workflow:
1. resume-customize → AI reorders existing skills only

New workflow:
1. resume-skills match job.txt → See what can be added
2. resume-customize → AI reorders + adds verified skills
```

**Nothing breaks**: If skills inventory doesn't exist, the system works as before (reorder only).

## Technical Details

### Files Created
- `config/skills_inventory.yaml` - Your skills database
- `src/resume_ai/skills_manager.py` - Core logic
- `src/resume_ai/skills_cli.py` - CLI commands

### Modified Files
- `src/resume_ai/resume_customize.py` - Integrates skills manager
- `src/resume_ai/prompts/resume_customize.txt` - Updated prompt
- `requirements.txt` - Added click dependency

### Version
- Feature added in: v0.3.0
- Compatible with: Python 3.12+

## FAQ

**Q: Will this add skills I don't have?**  
A: No. Skills are only added if there's evidence in your work experience.

**Q: What if I forget to update my inventory?**  
A: The system works with what you have. Just keep it updated as you learn new skills.

**Q: Can I have multiple inventories?**  
A: Not currently, but you can maintain one comprehensive inventory.

**Q: Does this work with the export feature?**  
A: Yes! Customized resumes with added skills export perfectly to .docx.

**Q: What about false positives?**  
A: Review the customized resume before submitting. The AI is conservative but not perfect.

## Support

For issues or questions:
1. Check this documentation
2. Review `config/skills_inventory.yaml` format
3. Test with `resume-skills match` before customizing
4. Verify the AI's skill additions make sense

## What's Next?

Future enhancements could include:
- Skill proficiency levels (beginner, intermediate, expert)
- Years of experience per skill
- Skill endorsements or certifications
- Auto-sync with LinkedIn
- Skill trend analysis across job postings

---

**Remember**: This feature enhances resume customization while maintaining complete accuracy. It suggests skills but never fabricates experience.

