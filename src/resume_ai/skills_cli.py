"""CLI for managing skills inventory."""

import click
from pathlib import Path
from .skills_manager import SkillsManager


@click.group()
def skills():
    """Manage your skills inventory."""
    pass


@skills.command()
def list():
    """List all skills in inventory."""
    try:
        manager = SkillsManager()
    except FileNotFoundError as e:
        click.echo(f"\n❌ Error: {e}")
        click.echo("\nCreate config/skills_inventory.yaml to get started.")
        return
    
    click.echo("\n📋 Your Skills Inventory\n")
    click.echo("=" * 70)
    
    all_skills = manager.get_all_skills()
    total_count = 0
    
    for category, skills_list in all_skills.items():
        # Format category name
        category_display = category.replace('_', ' ').title()
        click.echo(f"\n{category_display} ({len(skills_list)} skills):")
        
        for skill in skills_list:
            click.echo(f"  • {skill}")
            total_count += 1
    
    click.echo("\n" + "=" * 70)
    click.echo(f"Total: {total_count} skills across {len(all_skills)} categories\n")


@skills.command()
@click.argument('category')
@click.argument('skill')
def add(category: str, skill: str):
    """
    Add a skill to inventory.
    
    Examples:
        skills add programming_languages "Rust"
        skills add cloud_platforms "Digital Ocean"
    """
    try:
        manager = SkillsManager()
    except FileNotFoundError as e:
        click.echo(f"\n❌ Error: {e}")
        return
    
    try:
        manager.add_skill(category, skill)
        click.echo(f"\n✅ Added '{skill}' to '{category}'\n")
    except Exception as e:
        click.echo(f"\n❌ Error adding skill: {e}\n")


@skills.command()
@click.argument('job_description_file', type=click.Path(exists=True))
@click.option('--max-skills', '-n', default=10, help='Maximum skills to show')
def match(job_description_file: str, max_skills: int):
    """
    Show which skills from your inventory match a job description.
    
    Example:
        skills match /path/to/job_posting.txt
    """
    try:
        manager = SkillsManager()
    except FileNotFoundError as e:
        click.echo(f"\n❌ Error: {e}")
        return
    
    # Read job description
    job_text = Path(job_description_file).read_text()
    
    click.echo("\n🔍 Analyzing job description against your skills inventory...\n")
    
    # Find matching skills
    matches = manager.find_matching_skills(
        job_text,
        {},  # Empty dict = no current resume skills
        max_new_skills=max_skills
    )
    
    if matches:
        click.echo(f"✅ Found {len(matches)} matching skills from your inventory:\n")
        click.echo("=" * 70)
        
        # Group by category
        by_category = {}
        for match in matches:
            if match.category not in by_category:
                by_category[match.category] = []
            by_category[match.category].append(match)
        
        for category, category_matches in by_category.items():
            category_display = category.replace('_', ' ').title()
            click.echo(f"\n{category_display}:")
            
            for match in category_matches:
                relevance_pct = int(match.relevance_score * 100)
                click.echo(f"  • {match.skill} (relevance: {relevance_pct}%)")
        
        click.echo("\n" + "=" * 70)
        click.echo("\n💡 These skills appear in the job description and are in your inventory.")
        click.echo("   They will be suggested during resume customization.\n")
    else:
        click.echo("❌ No skills from your inventory found in this job description.")
        click.echo("\n💡 Consider:")
        click.echo("   1. Adding relevant skills to your inventory")
        click.echo("   2. Using different skill names (e.g., 'React' vs 'React.js')")
        click.echo("   3. The job may use different terminology\n")


@skills.command()
def categories():
    """List all skill categories."""
    try:
        manager = SkillsManager()
    except FileNotFoundError as e:
        click.echo(f"\n❌ Error: {e}")
        return
    
    click.echo("\n📂 Skill Categories\n")
    click.echo("=" * 70)
    
    all_skills = manager.get_all_skills()
    
    for category, skills_list in all_skills.items():
        category_display = category.replace('_', ' ').title()
        click.echo(f"  {category:<30} ({len(skills_list)} skills)")
    
    click.echo("\n" + "=" * 70)
    click.echo(f"Total: {len(all_skills)} categories\n")


@skills.command()
@click.argument('category')
def show(category: str):
    """
    Show all skills in a specific category.
    
    Example:
        skills show programming_languages
    """
    try:
        manager = SkillsManager()
    except FileNotFoundError as e:
        click.echo(f"\n❌ Error: {e}")
        return
    
    all_skills = manager.get_all_skills()
    
    if category not in all_skills:
        click.echo(f"\n❌ Category '{category}' not found.")
        click.echo("\nAvailable categories:")
        for cat in all_skills.keys():
            click.echo(f"  • {cat}")
        click.echo()
        return
    
    skills_list = all_skills[category]
    category_display = category.replace('_', ' ').title()
    
    click.echo(f"\n{category_display} ({len(skills_list)} skills)\n")
    click.echo("=" * 70)
    
    for skill in skills_list:
        click.echo(f"  • {skill}")
    
    click.echo()


@skills.command()
@click.argument('skill_name')
def find(skill_name: str):
    """
    Search for a skill across all categories.
    
    Example:
        skills find Python
    """
    try:
        manager = SkillsManager()
    except FileNotFoundError as e:
        click.echo(f"\n❌ Error: {e}")
        return
    
    skill_lower = skill_name.lower()
    found = []
    
    for category, skills_list in manager.get_all_skills().items():
        for skill in skills_list:
            if skill_lower in skill.lower():
                found.append((category, skill))
    
    if found:
        click.echo(f"\n🔍 Found {len(found)} match(es) for '{skill_name}':\n")
        
        for category, skill in found:
            category_display = category.replace('_', ' ').title()
            click.echo(f"  • {skill} ({category_display})")
        
        click.echo()
    else:
        click.echo(f"\n❌ No skills found matching '{skill_name}'")
        click.echo("\n💡 Try adding it with: skills add <category> \"{skill_name}\"\n")


if __name__ == '__main__':
    skills()

