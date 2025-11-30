"""
Skills Manager - Manages skill inventory and intelligent skill selection.
"""

from pathlib import Path
from typing import Dict, List, Set
import yaml
from dataclasses import dataclass
import re


@dataclass
class SkillMatch:
    """Represents a matched skill."""
    skill: str
    category: str
    relevance_score: float  # 0-1 based on JD match
    match_type: str  # "exact", "partial", "variant"


class SkillsManager:
    """Manages skills inventory and selection for resume customization."""
    
    def __init__(self, skills_file: Path = None):
        """
        Initialize skills manager.
        
        Args:
            skills_file: Path to skills inventory YAML
        """
        if skills_file is None:
            # Default location
            config_dir = Path(__file__).parent.parent.parent / "config"
            skills_file = config_dir / "skills_inventory.yaml"
        
        self.skills_file = Path(skills_file)
        self.skills_inventory = self._load_skills()
    
    def _load_skills(self) -> Dict[str, List[str]]:
        """Load skills from YAML file."""
        if not self.skills_file.exists():
            raise FileNotFoundError(
                f"Skills inventory not found: {self.skills_file}\n"
                "Create config/skills_inventory.yaml with your skills."
            )
        
        with open(self.skills_file) as f:
            data = yaml.safe_load(f)
            
            # Filter out comments and ensure all values are lists
            skills = {}
            for key, value in data.items():
                if isinstance(value, list):
                    skills[key] = value
            
            return skills
    
    def get_all_skills(self) -> Dict[str, List[str]]:
        """Get all skills by category."""
        return self.skills_inventory
    
    def get_skills_flat(self) -> Set[str]:
        """Get all skills as flat set."""
        all_skills = set()
        for category_skills in self.skills_inventory.values():
            all_skills.update(category_skills)
        return all_skills
    
    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill name for comparison."""
        return skill.lower().strip()
    
    def _create_skill_variants(self, skill: str) -> Set[str]:
        """Create variants of a skill for better matching."""
        variants = {self._normalize_skill(skill)}
        
        # Add common variants
        skill_lower = skill.lower()
        
        # Remove common suffixes
        for suffix in ['.js', ' api', ' framework']:
            if skill_lower.endswith(suffix):
                base = skill_lower[:-len(suffix)].strip()
                variants.add(base)
        
        # Add acronym variants
        if skill_lower == 'natural language processing':
            variants.add('nlp')
        elif skill_lower == 'nlp':
            variants.add('natural language processing')
        elif skill_lower == 'large language models':
            variants.add('llms')
            variants.add('llm')
        elif skill_lower in ['llms', 'llm']:
            variants.add('large language models')
        elif skill_lower == 'continuous integration':
            variants.add('ci')
        elif skill_lower == 'continuous deployment':
            variants.add('cd')
        elif skill_lower == 'ci/cd':
            variants.add('continuous integration')
            variants.add('continuous deployment')
        
        return variants
    
    def find_matching_skills(
        self,
        job_description: str,
        current_resume_skills: Dict[str, List[str]],
        max_new_skills: int = 5
    ) -> List[SkillMatch]:
        """
        Find skills from inventory that match job description.
        
        Args:
            job_description: Job posting text
            current_resume_skills: Skills already in resume
            max_new_skills: Maximum new skills to suggest
            
        Returns:
            List of SkillMatch objects for relevant missing skills
        """
        job_text_lower = job_description.lower()
        
        # Get current skills (normalized)
        current_skills_normalized = set()
        for skills_list in current_resume_skills.values():
            for skill in skills_list:
                current_skills_normalized.update(self._create_skill_variants(skill))
        
        # Find matching skills not in current resume
        matches = []
        
        for category, skills in self.skills_inventory.items():
            for skill in skills:
                skill_normalized = self._normalize_skill(skill)
                
                # Skip if already in resume
                if skill_normalized in current_skills_normalized:
                    continue
                
                # Check all variants
                variants = self._create_skill_variants(skill)
                
                # Find best match
                best_score = 0.0
                match_type = None
                
                for variant in variants:
                    # Exact word boundary match
                    pattern = r'\b' + re.escape(variant) + r'\b'
                    matches_found = re.findall(pattern, job_text_lower)
                    
                    if matches_found:
                        count = len(matches_found)
                        # Weight: exact match is better, multiple mentions increase score
                        score = min(count * 0.4, 1.0)
                        
                        if variant == skill_normalized:
                            score *= 1.2  # Bonus for exact match
                            match_type = "exact"
                        else:
                            match_type = "variant"
                        
                        if score > best_score:
                            best_score = score
                
                # If skill appears in JD, add to matches
                if best_score > 0:
                    matches.append(SkillMatch(
                        skill=skill,
                        category=category,
                        relevance_score=min(best_score, 1.0),
                        match_type=match_type or "partial"
                    ))
        
        # Sort by relevance and limit
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        return matches[:max_new_skills]
    
    def merge_skills(
        self,
        current_skills: Dict[str, List[str]],
        new_matches: List[SkillMatch]
    ) -> Dict[str, List[str]]:
        """
        Merge new skills into current skills by category.
        
        Args:
            current_skills: Existing resume skills
            new_matches: New skills to add
            
        Returns:
            Updated skills dictionary
        """
        merged = {k: list(v) for k, v in current_skills.items()}
        
        for match in new_matches:
            # Map inventory category to resume category
            # Try to find best matching category in resume
            category_to_use = self._map_category_to_resume(
                match.category, 
                current_skills.keys()
            )
            
            if category_to_use in merged:
                merged[category_to_use].append(match.skill)
            else:
                # Create new category with formatted name
                display_category = self._format_category_name(match.category)
                merged[display_category] = [match.skill]
        
        return merged
    
    def _map_category_to_resume(
        self,
        inventory_category: str,
        resume_categories: List[str]
    ) -> str:
        """
        Map inventory category to existing resume category.
        
        Args:
            inventory_category: Category from skills inventory
            resume_categories: Existing categories in resume
            
        Returns:
            Best matching resume category or formatted inventory category
        """
        # Common mappings
        category_map = {
            "programming_languages": ["Languages", "Programming Languages", "Core Languages"],
            "web_frameworks": ["Frameworks", "Web Technologies", "Backend"],
            "cloud_platforms": ["Cloud", "Cloud & Infrastructure", "Infrastructure"],
            "containers_orchestration": ["DevOps", "Infrastructure", "Cloud"],
            "databases": ["Databases", "Data Storage"],
            "ai_machine_learning": ["AI/ML", "Machine Learning", "AI & ML"],
            "devops_ci_cd": ["DevOps", "CI/CD", "Development Tools"],
            "version_control": ["Tools", "Development Tools"],
            "testing": ["Testing", "Quality Assurance"],
            "api_development": ["Backend", "API Development"],
        }
        
        # Try to find matching category
        possible_categories = category_map.get(inventory_category, [])
        
        for resume_cat in resume_categories:
            if resume_cat in possible_categories:
                return resume_cat
            # Check for partial matches
            for possible in possible_categories:
                if possible.lower() in resume_cat.lower() or resume_cat.lower() in possible.lower():
                    return resume_cat
        
        # Return formatted inventory category
        return self._format_category_name(inventory_category)
    
    def _format_category_name(self, category: str) -> str:
        """Format category name for display."""
        # Convert snake_case to Title Case
        return category.replace('_', ' ').title()
    
    def format_suggestions_for_prompt(
        self,
        matches: List[SkillMatch],
        include_scores: bool = True
    ) -> str:
        """
        Format skill matches for inclusion in AI prompt.
        
        Args:
            matches: List of skill matches
            include_scores: Whether to include relevance scores
            
        Returns:
            Formatted string for prompt
        """
        if not matches:
            return "No additional skills from inventory found matching this job description."
        
        lines = []
        
        # Group by category
        by_category = {}
        for match in matches:
            if match.category not in by_category:
                by_category[match.category] = []
            by_category[match.category].append(match)
        
        for category, category_matches in by_category.items():
            category_display = self._format_category_name(category)
            lines.append(f"\n**{category_display}:**")
            
            for match in category_matches:
                if include_scores:
                    score_pct = int(match.relevance_score * 100)
                    lines.append(f"  - {match.skill} (relevance: {score_pct}%)")
                else:
                    lines.append(f"  - {match.skill}")
        
        return "\n".join(lines)
    
    def add_skill(self, category: str, skill: str) -> None:
        """
        Add a new skill to the inventory.
        
        Args:
            category: Category to add skill to
            skill: Skill name to add
        """
        if category not in self.skills_inventory:
            self.skills_inventory[category] = []
        
        if skill not in self.skills_inventory[category]:
            self.skills_inventory[category].append(skill)
            self._save_skills()
    
    def _save_skills(self) -> None:
        """Save skills inventory back to YAML file."""
        with open(self.skills_file, 'w') as f:
            yaml.safe_dump(
                self.skills_inventory,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True
            )

