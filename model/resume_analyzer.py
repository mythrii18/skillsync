import re
import json
from datetime import datetime

# =============================================================================
# RESUME FORMAT & STRUCTURE GUIDELINES
# =============================================================================

RESUME_FORMAT_GUIDELINES = {
    "fonts": {
        "recommended": ["Arial", "Calibri", "Helvetica", "Garamond", "Georgia", "Times New Roman"],
        "avoid": ["Comic Sans", "Papyrus", "Brush Script", "Impact", "Courier New"],
        "professional_score": {
            "excellent": ["Arial", "Calibri", "Helvetica"],
            "good": ["Garamond", "Georgia", "Times New Roman"],
            "poor": ["Comic Sans", "Papyrus", "Brush Script", "Impact"]
        }
    },
    "font_sizes": {
        "name": {"min": 20, "max": 28, "ideal": 24},
        "headers": {"min": 12, "max": 16, "ideal": 14},
        "body": {"min": 10, "max": 12, "ideal": 11},
        "contact": {"min": 10, "max": 12, "ideal": 11}
    },
    "structure": {
        "ideal_order": [
            "Header/Contact",
            "Summary/Objective", 
            "Education",
            "Skills",
            "Experience/Projects",
            "Certifications",
            "Achievements"
        ],
        "max_pages": {
            "fresher": 1,
            "mid": 1,
            "senior": 2
        }
    },
    "sections": {
        "essential": ["Contact Information", "Education", "Skills", "Experience/Projects"],
        "recommended": ["Summary", "Certifications", "Achievements", "Technical Skills", "Soft Skills"],
        "optional": ["Hobbies", "Languages", "References", "Personal Details"]
    },
    "formatting": {
        "margins": {"min": 0.5, "max": 1.0, "unit": "inches"},
        "line_spacing": {"recommended": 1.15, "min": 1.0, "max": 1.5},
        "bullet_style": ["•", "-", "→"],
        "date_format": "MM/YYYY or Month YYYY"
    }
}

RESUME_TEMPLATES = {
    "modern_professional": {
        "name": "Modern Professional",
        "best_for": ["Software Engineers", "Product Managers", "Designers"],
        "structure": [
            {"section": "Header", "content": "Name (24pt bold), Contact info (11pt), LinkedIn/GitHub links"},
            {"section": "Professional Summary", "content": "2-3 lines, 11pt, highlighting key achievements"},
            {"section": "Skills", "content": "Categorized: Technical | Tools | Soft Skills, 2 columns"},
            {"section": "Experience", "content": "Reverse chronological, Company | Role | Dates, 3-4 bullets each"},
            {"section": "Education", "content": "Degree | Institution | CGPA | Year"},
            {"section": "Projects", "content": "Name | Tech Stack | Link | 2-3 impact bullets"},
            {"section": "Certifications", "content": "Name | Platform | Year"}
        ],
        "font": "Calibri or Arial",
        "color_scheme": "Black text, Blue accents for headers",
        "page_count": 1
    },
    "technical_cyclone": {
        "name": "Technical (Optimized for Cyclone)",
        "best_for": ["Flutter Developers", "Mobile Developers", "Full Stack Developers"],
        "structure": [
            {"section": "Header", "content": "Name (26pt), Phone, Email, LinkedIn, GitHub, Location"},
            {"section": "Technical Skills", "content": "Languages, Frameworks, Tools, Databases - Group by category"},
            {"section": "Projects", "content": "PROJECT NAME (bold) | Tech Stack | GitHub Link"},
            {"section": "  Details", "content": "• Action verb + Result + Numbers/metrics\n• 3-4 bullets per project"},
            {"section": "Experience", "content": "Company | Role | Duration | 3-4 achievement bullets"},
            {"section": "Education", "content": "Degree (B.Tech/MCA) | College | CGPA | Year"},
            {"section": "Certifications", "content": "Relevant tech certifications with dates"}
        ],
        "font": "Arial 11pt body, 14pt headers",
        "must_include": ["Flutter/Dart", "Firebase", "REST API", "Git", "Projects with links"],
        "page_count": 1
    },
    "ats_friendly": {
        "name": "ATS-Friendly (For Automated Screening)",
        "best_for": ["All Applicants", "First Screening"],
        "structure": [
            {"section": "Contact", "content": "Plain text, no tables, standard section headers"},
            {"section": "Summary", "content": "Keywords from job description, 3-4 lines"},
            {"section": "Skills", "content": "Comma-separated list, include all keywords from JD"},
            {"section": "Experience", "content": "Standard format: Title | Company | Dates"},
            {"section": "Education", "content": "Degree, Institution, CGPA/Percentage, Year"},
            {"section": "Keywords Section", "content": "Technologies, Tools, Methodologies used"}
        ],
        "font": "Arial or Times New Roman 11pt",
        "rules": [
            "No tables, text boxes, or graphics",
            "Use standard section names",
            "Include keywords from job description",
            "Save as .docx or .pdf (text-based)",
            "No headers/footers with contact info"
        ],
        "page_count": 1
    }
}

# =============================================================================
# COMPANY REQUIREMENTS DATABASE
# =============================================================================

# Company requirements database
COMPANY_REQUIREMENTS = {
    "Cyclone": {
        "required_sections": [
            "Contact Information",
            "Education",
            "Skills",
            "Work Experience",
            "Projects"
        ],
        "technical_skills": {
            "must_have": ["Flutter", "Dart", "React Native", "Firebase", "REST API", "Git"],
            "good_to_have": [
                "React", "TypeScript", "Node.js", "Python", "AWS", "Docker",
                "Kubernetes", "PostgreSQL", "MongoDB", "Figma", "SQL"
            ]
        },
        "soft_skills": [
            "Communication", "Teamwork", "Problem Solving", "Time Management",
            "Adaptability", "Ownership", "Attention to Detail"
        ],
        "education_criteria": {
            "preferred": ["B.Tech", "BCA", "B.Sc", "MCA", "M.Tech"],
            "min_cgpa": 0,  # No minimum
            "backlog_policy": "Active backlogs not preferred"
        },
        "experience_levels": {
            "fresher": "0-2 years",
            "mid": "1-3 years",
            "senior": "2-5 years"
        },
        "format_requirements": {
            "font_preferred": "Professional (Arial, Calibri, Times New Roman)",
            "font_size": {
                "name": "24-28",
                "headers": "14-16",
                "body": "11-12"
            },
            "max_pages": 2,
            "file_formats": ["PDF", "DOCX"]
        }
    }
}


def extract_contact_info(text):
    """Extract contact information from resume"""
    result = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "location": None
    }
    
    # Email pattern
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        result["email"] = email_match.group()
    
    # Phone pattern (Indian format)
    phone_match = re.search(r'(\+91[\s-]?)?[6-9]\d{9}', text)
    if phone_match:
        result["phone"] = phone_match.group()
    
    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/[a-zA-Z0-9-]+', text, re.IGNORECASE)
    if linkedin_match:
        result["linkedin"] = linkedin_match.group()
    
    # GitHub
    github_match = re.search(r'github\.com/[a-zA-Z0-9-]+', text, re.IGNORECASE)
    if github_match:
        result["github"] = github_match.group()
    
    # Location
    location_match = re.search(r'(Bangalore|Mumbai|Delhi|Chennai|Hyderabad|Pune|Chandigarh|Kolkata)[,\s-]?\d{6}', text, re.IGNORECASE)
    if not location_match:
        location_match = re.search(r'(Bangalore|Mumbai|Delhi|Chennai|Hyderabad|Pune|Chandigarh|Kolkata)', text, re.IGNORECASE)
    if location_match:
        result["location"] = location_match.group()
    
    return result


def extract_education(text):
    """Extract education details"""
    education = []
    
    # B.Tech/B.E. pattern
    btech_pattern = r'(B\.Tech|B\.E\.|B\.Sc\.|BCA|M\.Tech|M\.Sc\.|MCA)[,\s]*(?:in)?\s*([A-Za-z\s]+)?[,\s]*(\d{4})[,\s]*(?:CGPA|GPA)?[:\s]*([\d.]+)'
    for match in re.finditer(btech_pattern, text, re.IGNORECASE):
        education.append({
            "degree": match.group(1),
            "branch": match.group(2).strip() if match.group(2) else "Unknown",
            "year": match.group(3),
            "cgpa": match.group(4)
        })
    
    # 12th/10th pattern
    school_pattern = r'(Class\s*(?:XII|12)|Class\s*(?:X|10))[,\s]*(?:Board)?[,\s]*([A-Za-z\s]+)?[,\s]*(\d{4})[,\s]*[:\s]*([\d.]+)'
    for match in re.finditer(school_pattern, text, re.IGNORECASE):
        education.append({
            "degree": match.group(1),
            "institution": match.group(2).strip() if match.group(2) else "Unknown",
            "year": match.group(3),
            "percentage": match.group(4)
        })
    
    return education


def extract_skills(text):
    """Extract technical and soft skills"""
    text_lower = text.lower()
    
    technical_skills = []
    soft_skills = []
    
    # Technical skills database
    tech_skill_list = [
        "flutter", "dart", "react native", "react", "typescript", "javascript",
        "firebase", "firestore", "rest api", "restful api", "git", "github",
        "html", "css", "html5", "css3", "sql", "mysql", "postgresql", "sqlite",
        "python", "django", "flask", "nodejs", "node.js", "express", "java",
        "android", "ios", "kotlin", "swift", "docker", "kubernetes", "aws",
        "gcp", "azure", "figma", "redux", "mongodb", "redis", "graphql",
        "websocket", "ci/cd", "devops", "testing", "selenium", "jest",
        "tableau", "power bi", "google analytics", "excel", "pandas", "numpy"
    ]
    
    soft_skill_list = [
        "communication", "teamwork", "leadership", "problem solving",
        "time management", "adaptability", "ownership", "analytical",
        "presentation", "project management", "agile", "scrum"
    ]
    
    for skill in tech_skill_list:
        if skill in text_lower:
            technical_skills.append(skill.title())
    
    for skill in soft_skill_list:
        if skill in text_lower:
            soft_skills.append(skill.title())
    
    return {
        "technical": list(set(technical_skills)),
        "soft": list(set(soft_skills))
    }


def extract_experience(text):
    """Extract work experience and projects"""
    experience = []
    projects = []
    
    # Experience patterns
    exp_pattern = r'(Internship|Training|Software Engineer|Developer|Engineer|Analyst|Designer)[,\s]*(?:at)?\s*([A-Za-z\s]+)?[,\s]*(\d{1,2})[+\s]*(?:months?|years?)'
    for match in re.finditer(exp_pattern, text, re.IGNORECASE):
        experience.append({
            "role": match.group(1),
            "company": match.group(2).strip() if match.group(2) else "Not specified",
            "duration": match.group(3)
        })
    
    # Project patterns
    project_pattern = r'(Project|Project Name)[:\s]*([A-Za-z\s]+)'
    for match in re.finditer(project_pattern, text, re.IGNORECASE):
        projects.append({
            "name": match.group(2).strip()[:50]
        })
    
    return {
        "experience": experience[:5],
        "projects": projects[:5]
    }


def calculate_skill_score(user_skills, company_req):
    """Calculate skill match score"""
    must_have = set(s.lower() for s in company_req.get("must_have", []))
    good_to_have = set(s.lower() for s in company_req.get("good_to_have", []))
    user_skills_set = set(s.lower() for s in user_skills)
    
    # Must have skills (60% weight)
    must_match = len(user_skills_set & must_have)
    must_score = (must_match / len(must_have)) * 60 if must_have else 0
    
    # Good to have skills (40% weight)
    good_match = len(user_skills_set & good_to_have)
    good_score = (good_match / len(good_to_have)) * 40 if good_to_have else 0
    
    return round(must_score + good_score, 1)


def analyze_font_and_formatting(resume_text):
    """Analyze font choices and formatting from resume text"""
    issues = []
    recommendations = []
    score = 100
    
    # Check for common formatting issues
    text_upper = resume_text.upper()
    
    # Font detection (indirect through patterns)
    detected_font_hints = []
    
    # Check for monospaced font indicators
    if re.search(r'Courier|Consolas|Monospace', resume_text, re.IGNORECASE):
        detected_font_hints.append("Monospace (Courier-like)")
        issues.append("❌ Using monospaced font - looks outdated")
        recommendations.append("🔤 Switch to modern font: Arial, Calibri, or Helvetica")
        score -= 20
    
    # Check for decorative fonts
    decorative_patterns = ['Comic', 'Papyrus', 'Brush', 'Impact']
    for pattern in decorative_patterns:
        if pattern.lower() in resume_text.lower():
            detected_font_hints.append(pattern)
            issues.append(f"❌ Unprofessional font detected: {pattern}")
            recommendations.append("🔤 Use professional font: Arial (11pt), Calibri (11pt), or Times New Roman (12pt)")
            score -= 25
    
    # Check font size consistency
    lines = resume_text.split('\n')
    name_line = lines[0] if lines else ""
    
    # Analyze first line (usually name) for size
    if len(name_line) < 20:
        # Likely a name line
        if len(name_line) > 30:
            issues.append("⚠️ Name font size may be too small")
            recommendations.append("📏 Name should be 24-28pt (bold)")
            score -= 10
    
    # Check for ALL CAPS overuse (indicates poor formatting)
    caps_lines = [l for l in lines if l.isupper() and len(l) > 10]
    if len(caps_lines) > 3:
        issues.append("⚠️ Excessive use of ALL CAPS - reduces readability")
        recommendations.append("📏 Use Title Case for headers (14pt bold), Sentence case for body (11pt)")
        score -= 15
    
    # Check for bullet point consistency
    bullet_styles = []
    for line in lines:
        if line.strip().startswith(('•', '-', '→', '*', '·', '○')):
            bullet_styles.append(line.strip()[0])
    
    if bullet_styles:
        unique_bullets = set(bullet_styles)
        if len(unique_bullets) > 1:
            issues.append("⚠️ Inconsistent bullet styles used")
            recommendations.append("📋 Use consistent bullets throughout (recommend: • )")
            score -= 10
    
    # Check line spacing (inferred from text density)
    avg_line_length = sum(len(l) for l in lines) / len(lines) if lines else 0
    if avg_line_length > 80:
        issues.append("⚠️ Text appears too dense - increase line spacing to 1.15")
        recommendations.append("📏 Set line spacing to 1.15 for better readability")
        score -= 10
    
    # Check for proper margins (indirect)
    long_lines = [l for l in lines if len(l) > 100]
    if len(long_lines) > len(lines) * 0.3:
        issues.append("⚠️ Text extends too wide - margins may be too small")
        recommendations.append("📄 Set margins to 0.75-1 inch on all sides")
        score -= 10
    
    return {
        "score": max(score, 0),
        "detected_hints": detected_font_hints,
        "issues": issues,
        "recommendations": recommendations,
        "optimal_fonts": RESUME_FORMAT_GUIDELINES["fonts"]["recommended"],
        "font_sizes": RESUME_FORMAT_GUIDELINES["font_sizes"]
    }


def analyze_section_structure(resume_text):
    """Analyze resume section structure and order"""
    text_lower = resume_text.lower()
    lines = resume_text.split('\n')
    
    # Detect sections
    section_patterns = {
        "Contact/Header": [r'(?i)^(name|contact|email|phone|\+91)'],
        "Summary/Objective": [r'(?i)(summary|objective|profile|about me)'],
        "Education": [r'(?i)(education|academic|qualification|b\.tech|b\.e\.|m\.tech|mca)'],
        "Skills": [r'(?i)(skills|technical skills|technologies|expertise)'],
        "Experience": [r'(?i)(experience|work experience|employment|internship)'],
        "Projects": [r'(?i)(projects|project work|key projects)'],
        "Certifications": [r'(?i)(certifications|certificates|certified)'],
        "Achievements": [r'(?i)(achievements|accomplishments|awards|honors)'],
        "Publications": [r'(?i)(publications|papers|research)'],
        "Languages": [r'(?i)(languages|language proficiency)'],
        "Hobbies": [r'(?i)(hobbies|interests|extra-curricular)'],
        "References": [r'(?i)(references|referees)']
    }
    
    detected_sections = []
    section_positions = {}
    
    for section_name, patterns in section_patterns.items():
        for pattern in patterns:
            for i, line in enumerate(lines):
                if re.search(pattern, line):
                    if section_name not in section_positions:
                        section_positions[section_name] = i
                        detected_sections.append(section_name)
                    break
    
    # Order analysis
    essential = RESUME_FORMAT_GUIDELINES["sections"]["essential"]
    recommended = RESUME_FORMAT_GUIDELINES["sections"]["recommended"]
    
    missing_essential = []
    missing_recommended = []
    
    for section in essential:
        section_lower = section.lower()
        found = False
        for detected in detected_sections:
            if any(word in detected.lower() for word in section_lower.split()):
                found = True
                break
        if not found:
            missing_essential.append(section)
    
    for section in recommended:
        section_lower = section.lower()
        found = False
        for detected in detected_sections:
            if any(word in detected.lower() for word in section_lower.split()):
                found = True
                break
        if not found:
            missing_recommended.append(section)
    
    # Check section order
    order_issues = []
    ideal_order = RESUME_FORMAT_GUIDELINES["structure"]["ideal_order"]
    
    # Simple order check
    section_scores = {}
    for section in detected_sections:
        for i, ideal in enumerate(ideal_order):
            if ideal.lower() in section.lower() or section.lower() in ideal.lower():
                section_scores[section] = i
                break
    
    sorted_sections = sorted(section_scores.items(), key=lambda x: section_positions.get(x[0], 999))
    expected_order = sorted(section_scores.items(), key=lambda x: x[1])
    
    actual_order_indices = [section_positions.get(s[0], 999) for s in sorted_sections]
    if actual_order_indices != sorted(actual_order_indices):
        order_issues.append("⚠️ Sections are not in optimal order")
    
    # Calculate structure score
    score = 100
    score -= len(missing_essential) * 20
    score -= len(missing_recommended) * 5
    score -= len(order_issues) * 10
    
    recommendations = []
    if missing_essential:
        recommendations.append(f"📋 Add missing essential sections: {', '.join(missing_essential)}")
    if missing_recommended:
        recommendations.append(f"💡 Consider adding: {', '.join(missing_recommended[:3])}")
    if order_issues:
        recommendations.append("📊 Reorder sections: Contact → Summary → Education → Skills → Experience → Projects → Certifications")
    
    # Check for ATS-unfriendly elements
    ats_issues = []
    if re.search(r'\t+', resume_text) and len(re.findall(r'\t+', resume_text)) > 10:
        ats_issues.append("⚠️ Excessive tabs detected - may cause ATS parsing issues")
        recommendations.append("📄 Replace tabs with spaces for ATS compatibility")
        score -= 10
    
    # Check for tables (simplified detection)
    if '|' in resume_text and resume_text.count('|') > 5:
        ats_issues.append("⚠️ Table-like structure detected - may not parse correctly in ATS")
        recommendations.append("📄 Avoid tables; use simple text layout for ATS")
        score -= 10
    
    return {
        "score": max(score, 0),
        "detected_sections": detected_sections,
        "missing_essential": missing_essential,
        "missing_recommended": missing_recommended,
        "order_issues": order_issues,
        "ats_issues": ats_issues,
        "recommendations": recommendations,
        "ideal_structure": ideal_order
    }


def calculate_format_score(resume_text, format_req):
    """Calculate comprehensive resume format score"""
    # Get detailed analyses
    font_analysis = analyze_font_and_formatting(resume_text)
    structure_analysis = analyze_section_structure(resume_text)
    
    score = 0
    issues = []
    recommendations = []
    
    # Check length
    lines = resume_text.split('\n')
    if len(lines) <= 40:
        score += 15
        recommendations.append("✅ Resume length is optimal (1 page)")
    elif len(lines) <= 80:
        score += 10
        recommendations.append("📄 Resume is good (1-2 pages)")
    else:
        score += 5
        issues.append("⚠️ Resume is too long. Keep it to 1-2 pages max.")
        recommendations.append("📄 Consider trimming to 2 pages")
    
    # Check for contact info
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
        score += 10
    else:
        issues.append("❌ Missing email address")
        recommendations.append("📧 Add a professional email address")
    
    # Check for phone
    if re.search(r'(\+91[\s-]?)?[6-9]\d{9}', resume_text):
        score += 8
    else:
        issues.append("⚠️ Phone number not found")
        recommendations.append("📱 Add phone number with country code")
    
    # Check for LinkedIn/GitHub
    if re.search(r'linkedin\.com|github\.com', resume_text, re.IGNORECASE):
        score += 7
    else:
        issues.append("⚠️ Missing LinkedIn/GitHub links")
        recommendations.append("🔗 Add LinkedIn and GitHub profiles")
    
    # Check for skills section
    if re.search(r'skills|technical|technologies', resume_text, re.IGNORECASE):
        score += 10
    else:
        issues.append("❌ No dedicated skills section")
        recommendations.append("💡 Add a clear 'Skills' section with technologies")
    
    # Check for projects
    if re.search(r'project', resume_text, re.IGNORECASE):
        score += 8
    else:
        issues.append("⚠️ No projects mentioned")
        recommendations.append("🚀 Add 2-3 relevant projects with links")
    
    # Check for education
    if re.search(r'(b\.tech|b\.e\.|b\.sc|bca|m\.tech|m\.sc|mca)', resume_text, re.IGNORECASE):
        score += 7
    else:
        issues.append("⚠️ Education details not clear")
        recommendations.append("🎓 Add education with CGPA/percentage")
    
    # Check for action verbs
    action_verbs = ['developed', 'built', 'created', 'implemented', 'designed', 'managed', 'led', 'engineered', 'architected']
    has_actions = any(verb in resume_text.lower() for verb in action_verbs)
    if has_actions:
        score += 8
    else:
        issues.append("⚠️ Use action verbs for achievements")
        recommendations.append("✏️ Use strong action verbs: Developed, Built, Created, Led, Engineered")
    
    # Check for quantified achievements
    quantified = re.search(r'\d+%|\d+ users|\$\d+|\d+\+|\d+ projects|\d+ months?', resume_text)
    if quantified:
        score += 7
        recommendations.append("✅ Good! Using numbers to show impact")
    else:
        issues.append("⚠️ No quantified achievements (numbers/metrics)")
        recommendations.append("📊 Add metrics: 'Increased X by 50%', 'Built for 1000+ users'")
    
    # Combine with font and structure scores
    font_weight = 0.15
    structure_weight = 0.20
    base_weight = 0.65
    
    final_score = (
        (score * base_weight) +
        (font_analysis["score"] * font_weight) +
        (structure_analysis["score"] * structure_weight)
    )
    
    # Combine all issues and recommendations
    all_issues = issues + font_analysis["issues"] + structure_analysis["order_issues"] + structure_analysis["ats_issues"]
    all_recommendations = list(dict.fromkeys(
        recommendations + font_analysis["recommendations"] + structure_analysis["recommendations"]
    ))
    
    return {
        "score": round(min(final_score, 100), 1),
        "breakdown": {
            "base_format": score,
            "font_formatting": font_analysis["score"],
            "structure": structure_analysis["score"]
        },
        "font_analysis": font_analysis,
        "structure_analysis": structure_analysis,
        "issues": all_issues,
        "recommendations": all_recommendations
    }


def determine_best_template(resume_text, skill_score, format_score):
    """Determine the best resume template based on analysis"""
    
    # Check for ATS issues
    ats_friendly = True
    if '|' in resume_text and resume_text.count('|') > 5:
        ats_friendly = False
    if re.search(r'\t+', resume_text) and len(re.findall(r'\t+', resume_text)) > 10:
        ats_friendly = False
    
    # Check for technical depth
    technical_depth = len(re.findall(r'(Flutter|Dart|Firebase|React|API|Git|Database|Cloud|AWS|Docker)', resume_text, re.IGNORECASE))
    
    # Determine recommendation
    if not ats_friendly or format_score < 50:
        return {
            "recommended": RESUME_TEMPLATES["ats_friendly"],
            "reason": "Your resume needs better ATS compatibility. This template ensures parsing systems can read your resume correctly.",
            "priority": "high"
        }
    elif technical_depth >= 4 and skill_score >= 60:
        return {
            "recommended": RESUME_TEMPLATES["technical_cyclone"],
            "reason": "Your technical skills profile matches Cyclone's requirements. This template highlights technical depth effectively.",
            "priority": "high"
        }
    else:
        return {
            "recommended": RESUME_TEMPLATES["modern_professional"],
            "reason": "This is a versatile template that works well for most positions and presents your profile professionally.",
            "priority": "medium"
        }


def generate_analysis_report(resume_text, company_name="Cyclone"):
    """Generate complete resume analysis report"""
    
    # Get company requirements
    company_req = COMPANY_REQUIREMENTS.get(company_name, COMPANY_REQUIREMENTS["Cyclone"])
    
    # Extract resume components
    contact = extract_contact_info(resume_text)
    education = extract_education(resume_text)
    skills = extract_skills(resume_text)
    experience = extract_experience(resume_text)
    
    # Calculate scores
    all_skills = skills["technical"] + skills["soft"]
    skill_score = calculate_skill_score(all_skills, company_req["technical_skills"])
    format_score_result = calculate_format_score(resume_text, company_req.get("format_requirements", {}))
    format_score = format_score_result["score"]
    
    # Education score
    edu_score = 0
    if education:
        edu_score = 80  # Has education
        if any(e.get("cgpa", "0") > "7" for e in education if e.get("cgpa")):
            edu_score = 95
    else:
        edu_score = 50
    
    # Experience score
    exp_score = min(len(experience["experience"]) * 20 + len(experience["projects"]) * 10, 100)
    
    # Overall score
    overall_score = round((skill_score * 0.35 + format_score * 0.30 + edu_score * 0.15 + exp_score * 0.20), 1)
    
    # Generate recommendations
    recommendations = []
    
    # Skill recommendations
    user_skill_set = set(s.lower() for s in all_skills)
    must_have = set(s.lower() for s in company_req["technical_skills"]["must_have"])
    missing_must = must_have - user_skill_set
    good_to_have = set(s.lower() for s in company_req["technical_skills"]["good_to_have"])
    missing_good = good_to_have - user_skill_set
    
    if missing_must:
        recommendations.append(f"🔴 Must add: {', '.join(missing_must)}")
    if missing_good:
        recommendations.append(f"🟡 Consider adding: {', '.join(list(missing_good)[:5])}")
    
    # Add format recommendations
    recommendations.extend(format_score_result["recommendations"])
    
    # Section recommendations
    missing_sections = []
    for section in company_req.get("required_sections", []):
        section_lower = section.lower()
        if section_lower not in resume_text.lower():
            missing_sections.append(section)
    
    if missing_sections:
        recommendations.append(f"📋 Add missing sections: {', '.join(missing_sections)}")
    
    # Determine best template
    template_recommendation = determine_best_template(resume_text, skill_score, format_score)
    
    # Build the report
    report = {
        "timestamp": datetime.now().isoformat(),
        "company": company_name,
        "overall_score": overall_score,
        "scores": {
            "skill_match": {
                "score": skill_score,
                "label": get_score_label(skill_score),
                "weight": "35%",
                "details": {
                    "technical": skills["technical"],
                    "soft": skills["soft"],
                    "matched": list(user_skill_set & must_have),
                    "missing_must_have": list(missing_must),
                    "missing_good_to_have": list(missing_good)[:5]
                }
            },
            "format": {
                "score": format_score,
                "label": get_score_label(format_score),
                "weight": "30%",
                "breakdown": format_score_result.get("breakdown", {}),
                "font_analysis": format_score_result.get("font_analysis", {}),
                "structure_analysis": format_score_result.get("structure_analysis", {}),
                "issues": format_score_result["issues"],
                "recommendations": format_score_result["recommendations"]
            },
            "education": {
                "score": edu_score,
                "label": get_score_label(edu_score),
                "weight": "15%",
                "details": education
            },
            "experience": {
                "score": exp_score,
                "label": get_score_label(exp_score),
                "weight": "20%",
                "details": experience
            }
        },
        "contact": contact,
        "recommendations": recommendations,
        "template_recommendation": template_recommendation,
        "font_guidelines": RESUME_FORMAT_GUIDELINES["fonts"],
        "ideal_structure": RESUME_FORMAT_GUIDELINES["structure"]["ideal_order"],
        "resume_parsing": {
            "word_count": len(resume_text.split()),
            "line_count": len(resume_text.split('\n')),
            "has_contact": bool(contact["email"] and contact["phone"]),
            "has_skills": bool(skills["technical"]),
            "has_education": bool(education),
            "has_experience": bool(experience["experience"] or experience["projects"])
        }
    }
    
    return report


def get_score_label(score):
    """Get label for score"""
    if score >= 80:
        return "🔥 Excellent"
    elif score >= 60:
        return "✅ Good"
    elif score >= 40:
        return "📈 Average"
    else:
        return "⚠️ Needs Work"


def generate_svg_radar_chart(scores):
    """Generate SVG radar/spider chart for score visualization"""
    skill = scores['skill_match']['score']
    format_s = scores['format']['score']
    edu = scores['education']['score']
    exp = scores['experience']['score']
    
    # Calculate polygon points
    center = 60
    radius = 50
    
    # 4 axes at 90 degree intervals
    import math
    angles = [math.pi/2, math.pi, 3*math.pi/2, 0]  # Top, Left, Bottom, Right
    
    points = []
    values = [skill, format_s, edu, exp]
    for i, (angle, value) in enumerate(zip(angles, values)):
        r = (value / 100) * radius
        x = center + r * math.cos(angle)
        y = center - r * math.sin(angle)  # SVG y is inverted
        points.append(f"{x},{y}")
    
    polygon_points = " ".join(points)
    
    # Axis end points
    axis_points = []
    for angle in angles:
        x = center + radius * math.cos(angle)
        y = center - radius * math.sin(angle)
        axis_points.append((x, y))
    
    svg = f'''<!-- Radar Chart -->
<div class="radar-chart-container">
    <svg viewBox="0 0 120 120" class="radar-chart">
        <!-- Background grid -->
        <circle cx="60" cy="60" r="50" fill="none" stroke="#e5e7eb" stroke-width="1"/>
        <circle cx="60" cy="60" r="37.5" fill="none" stroke="#e5e7eb" stroke-width="1"/>
        <circle cx="60" cy="60" r="25" fill="none" stroke="#e5e7eb" stroke-width="1"/>
        <circle cx="60" cy="60" r="12.5" fill="none" stroke="#e5e7eb" stroke-width="1"/>
        
        <!-- Axes -->
        <line x1="60" y1="60" x2="{axis_points[0][0]}" y2="{axis_points[0][1]}" stroke="#e5e7eb" stroke-width="1"/>
        <line x1="60" y1="60" x2="{axis_points[1][0]}" y2="{axis_points[1][1]}" stroke="#e5e7eb" stroke-width="1"/>
        <line x1="60" y1="60" x2="{axis_points[2][0]}" y2="{axis_points[2][1]}" stroke="#e5e7eb" stroke-width="1"/>
        <line x1="60" y1="60" x2="{axis_points[3][0]}" y2="{axis_points[3][1]}" stroke="#e5e7eb" stroke-width="1"/>
        
        <!-- Data polygon -->
        <polygon points="{polygon_points}" fill="rgba(59, 130, 246, 0.3)" stroke="#3b82f6" stroke-width="2"/>
        
        <!-- Data points -->
        <circle cx="{points[0].split(',')[0]}" cy="{points[0].split(',')[1]}" r="3" fill="#3b82f6"/>
        <circle cx="{points[1].split(',')[0]}" cy="{points[1].split(',')[1]}" r="3" fill="#3b82f6"/>
        <circle cx="{points[2].split(',')[0]}" cy="{points[2].split(',')[1]}" r="3" fill="#3b82f6"/>
        <circle cx="{points[3].split(',')[0]}" cy="{points[3].split(',')[1]}" r="3" fill="#3b82f6"/>
        
        <!-- Labels -->
        <text x="60" y="8" text-anchor="middle" font-size="8" fill="#6b7280">Skills</text>
        <text x="10" y="62" text-anchor="middle" font-size="8" fill="#6b7280">Format</text>
        <text x="60" y="115" text-anchor="middle" font-size="8" fill="#6b7280">Edu</text>
        <text x="110" y="62" text-anchor="middle" font-size="8" fill="#6b7280">Exp</text>
    </svg>
</div>'''
    return svg


def generate_svg_donut_chart(score, label, color):
    """Generate SVG donut chart for overall score"""
    radius = 40
    circumference = 2 * 3.14159 * radius
    offset = circumference - (score / 100) * circumference
    
    svg = f'''<!-- Donut Chart -->
<div class="donut-chart-container">
    <svg viewBox="0 0 100 100" class="donut-chart">
        <!-- Background circle -->
        <circle cx="50" cy="50" r="{radius}" fill="none" stroke="#e5e7eb" stroke-width="8"/>
        <!-- Progress circle -->
        <circle cx="50" cy="50" r="{radius}" fill="none" stroke="{color}" stroke-width="8"
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                stroke-linecap="round"
                transform="rotate(-90 50 50)"/>
        <!-- Score text -->
        <text x="50" y="45" text-anchor="middle" font-size="18" font-weight="bold" fill="{color}">{score}%</text>
        <text x="50" y="60" text-anchor="middle" font-size="8" fill="#6b7280">{label}</text>
    </svg>
</div>'''
    return svg


def format_report_as_html(report):
    """Format report as HTML for display with visual charts and detailed analysis"""
    scores = report["scores"]
    
    # Generate visual charts
    radar_chart = generate_svg_radar_chart(scores)
    donut_chart = generate_svg_donut_chart(
        report['overall_score'],
        "Overall",
        get_score_color(report['overall_score'])
    )
    
    # Get format analysis details
    format_analysis = scores["format"].get("font_analysis", {})
    structure_analysis = scores["format"].get("structure_analysis", {})
    breakdown = scores["format"].get("breakdown", {})
    template_rec = report.get("template_recommendation", {})
    recommended_template = template_rec.get("recommended", {})
    
    html = f"""
<div class="resume-report">
    <!-- Header with Overall Score -->
    <div class="report-header">
        <h3>📊 Resume Analysis Report</h3>
        <p class="report-subtitle">Analysis for {report['company']} | {report['resume_parsing']['word_count']} words</p>
    </div>
    
    <!-- Visual Score Dashboard -->
    <div class="score-dashboard">
        {donut_chart}
        {radar_chart}
    </div>
    
    <!-- Detailed Score Breakdown -->
    <div class="score-bars-detailed">
        <div class="score-category">
            <div class="score-header">
                <label>💻 Skill Match <span class="weight">{scores['skill_match']['weight']}</span></label>
                <span class="score-value">{scores['skill_match']['score']}%</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar">
                    <div class="progress" style="width: {scores['skill_match']['score']}%; background: {get_score_color(scores['skill_match']['score'])}"></div>
                </div>
                <span class="score-label">{scores['skill_match']['label']}</span>
            </div>
        </div>
        
        <div class="score-category">
            <div class="score-header">
                <label>📄 Format & Structure <span class="weight">{scores['format']['weight']}</span></label>
                <span class="score-value">{scores['format']['score']}%</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar">
                    <div class="progress" style="width: {scores['format']['score']}%; background: {get_score_color(scores['format']['score'])}"></div>
                </div>
                <span class="score-label">{scores['format']['label']}</span>
            </div>
            <!-- Format breakdown -->
            <div class="format-breakdown">
                <div class="breakdown-item">
                    <span>Base Format:</span>
                    <span>{breakdown.get('base_format', 'N/A')}/100</span>
                </div>
                <div class="breakdown-item">
                    <span>Font/Formatting:</span>
                    <span>{breakdown.get('font_formatting', 'N/A')}/100</span>
                </div>
                <div class="breakdown-item">
                    <span>Structure:</span>
                    <span>{breakdown.get('structure', 'N/A')}/100</span>
                </div>
            </div>
        </div>
        
        <div class="score-category">
            <div class="score-header">
                <label>🎓 Education <span class="weight">{scores['education']['weight']}</span></label>
                <span class="score-value">{scores['education']['score']}%</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar">
                    <div class="progress" style="width: {scores['education']['score']}%; background: {get_score_color(scores['education']['score'])}"></div>
                </div>
                <span class="score-label">{scores['education']['label']}</span>
            </div>
        </div>
        
        <div class="score-category">
            <div class="score-header">
                <label>💼 Experience <span class="weight">{scores['experience']['weight']}</span></label>
                <span class="score-value">{scores['experience']['score']}%</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar">
                    <div class="progress" style="width: {scores['experience']['score']}%; background: {get_score_color(scores['experience']['score'])}"></div>
                </div>
                <span class="score-label">{scores['experience']['label']}</span>
            </div>
        </div>
    </div>
"""
    
    # Font & Formatting Analysis Section
    if format_analysis:
        html += """
    <div class="report-section format-analysis">
        <h4>🔤 Font & Formatting Analysis</h4>
"""
        if format_analysis.get("detected_hints"):
            html += f"""
        <div class="detected-fonts">
            <p><strong>Detected Font Indicators:</strong> {', '.join(format_analysis['detected_hints'])}</p>
        </div>
"""
        
        html += """
        <div class="font-recommendations">
            <p><strong>Recommended Professional Fonts:</strong></p>
            <div class="font-list">
                <span class="font-item best">Arial 11pt</span>
                <span class="font-item best">Calibri 11pt</span>
                <span class="font-item good">Helvetica 11pt</span>
                <span class="font-item good">Garamond 12pt</span>
            </div>
        </div>
        
        <div class="font-size-guide">
            <p><strong>Font Size Guidelines:</strong></p>
            <ul>
                <li>Name: 24-28pt (Bold)</li>
                <li>Section Headers: 14-16pt (Bold)</li>
                <li>Body Text: 11-12pt</li>
                <li>Contact Info: 10-11pt</li>
            </ul>
        </div>
    </div>
"""
    
    # Structure Analysis Section
    if structure_analysis:
        detected = structure_analysis.get("detected_sections", [])
        missing_essential = structure_analysis.get("missing_essential", [])
        missing_recommended = structure_analysis.get("missing_recommended", [])
        
        html += f"""
    <div class="report-section structure-analysis">
        <h4>📋 Section Structure Analysis</h4>
        
        <div class="structure-grid">
            <div class="structure-col">
                <p><strong>✅ Detected Sections ({len(detected)}):</strong></p>
                <ul class="section-list">
                    {''.join(f'<li>{s}</li>' for s in detected[:6])}
                </ul>
            </div>
            
            <div class="structure-col">
                <p><strong>📍 Ideal Section Order:</strong></p>
                <ol class="section-list ordered">
                    <li>Contact/Header</li>
                    <li>Professional Summary</li>
                    <li>Skills</li>
                    <li>Experience/Projects</li>
                    <li>Education</li>
                    <li>Certifications</li>
                </ol>
            </div>
        </div>
"""
        if missing_essential:
            html += f"""
        <div class="missing-sections alert">
            <p><strong>❌ Missing Essential Sections:</strong></p>
            <ul>
                {''.join(f'<li>{s}</li>' for s in missing_essential)}
            </ul>
        </div>
"""
        
        if missing_recommended[:3]:
            html += f"""
        <div class="missing-sections tip">
            <p><strong>💡 Consider Adding:</strong></p>
            <ul>
                {''.join(f'<li>{s}</li>' for s in missing_recommended[:3])}
            </ul>
        </div>
"""
        html += "    </div>\n"
    
    # Template Recommendation Section
    if recommended_template:
        structure_html = ""
        for item in recommended_template.get("structure", [])[:5]:
            structure_html += f"""
            <div class="template-structure-item">
                <strong>{item['section']}</strong>
                <span>{item['content']}</span>
            </div>
"""
        
        html += f"""
    <div class="report-section template-recommendation">
        <h4>📄 Recommended Resume Template</h4>
        <div class="template-card">
            <div class="template-header">
                <h5>{recommended_template.get('name', 'Professional Template')}</h5>
                <span class="priority-badge {template_rec.get('priority', 'medium')}">{template_rec.get('priority', 'Recommended').upper()} PRIORITY</span>
            </div>
            <p class="template-reason">{template_rec.get('reason', '')}</p>
            
            <div class="template-details">
                <p><strong>Best For:</strong> {', '.join(recommended_template.get('best_for', ['All Positions']))}</p>
                <p><strong>Font:</strong> {recommended_template.get('font', 'Arial/Calibri')}</p>
                <p><strong>Page Count:</strong> {recommended_template.get('page_count', 1)} page(s)</p>
            </div>
            
            <div class="template-structure">
                <p><strong>Recommended Structure:</strong></p>
                {structure_html}
            </div>
        </div>
    </div>
"""
    
    # Skills Section
    skill_details = scores["skill_match"]["details"]
    if skill_details["technical"]:
        html += f"""
    <div class="report-section">
        <h4>💻 Technical Skills Found ({len(skill_details['technical'])})</h4>
        <div class="skill-tags">
            {''.join(f'<span class="skill-tag">{s}</span>' for s in skill_details['technical'][:12])}
        </div>
    </div>
"""
    
    if skill_details["missing_must_have"]:
        html += f"""
    <div class="report-section missing">
        <h4>🔴 Missing Must-Have Skills for {report['company']}</h4>
        <div class="skill-tags missing">
            {''.join(f'<span class="skill-tag">{s}</span>' for s in skill_details['missing_must_have'])}
        </div>
        <p class="tip-text">Adding these skills will significantly improve your match score!</p>
    </div>
"""
    
    # Recommendations Section
    if report["recommendations"]:
        html += """
    <div class="report-section recommendations">
        <h4>📋 Actionable Recommendations</h4>
        <ul class="recommendations-list">
"""
        for rec in report["recommendations"][:10]:
            html += f"            <li>{rec}</li>\n"
        html += """
        </ul>
    </div>
"""
    
    # Contact Info Status
    contact = report["contact"]
    html += """
    <div class="report-section contact-status">
        <h4>📇 Contact Information Status</h4>
        <div class="contact-grid">
"""
    html += f"""
            <div class="contact-item {'present' if contact['email'] else 'missing'}">
                <span class="icon">{'✅' if contact['email'] else '❌'}</span>
                <span class="label">Email</span>
                <span class="value">{contact['email'] if contact['email'] else 'Not found'}</span>
            </div>
            <div class="contact-item {'present' if contact['phone'] else 'missing'}">
                <span class="icon">{'✅' if contact['phone'] else '❌'}</span>
                <span class="label">Phone</span>
                <span class="value">{contact['phone'] if contact['phone'] else 'Not found'}</span>
            </div>
            <div class="contact-item {'present' if contact['linkedin'] else 'missing'}">
                <span class="icon">{'✅' if contact['linkedin'] else '⚠️'}</span>
                <span class="label">LinkedIn</span>
                <span class="value">{contact['linkedin'] if contact['linkedin'] else 'Recommended'}</span>
            </div>
            <div class="contact-item {'present' if contact['github'] else 'missing'}">
                <span class="icon">{'✅' if contact['github'] else '⚠️'}</span>
                <span class="label">GitHub</span>
                <span class="value">{contact['github'] if contact['github'] else 'Recommended'}</span>
            </div>
        </div>
    </div>
</div>
"""
    
    return html


def get_score_color(score):
    """Get color for score"""
    if score >= 80:
        return "#22c55e"
    elif score >= 60:
        return "#3b82f6"
    elif score >= 40:
        return "#f59e0b"
    else:
        return "#ef4444"


def analyze_resume(resume_text, company_name="Cyclone"):
    """Main function to analyze resume"""
    report = generate_analysis_report(resume_text, company_name)
    return report


# Test function
if __name__ == "__main__":
    sample_resume = """
    John Doe
    Email: john.doe@email.com
    Phone: +91 9876543210
    LinkedIn: linkedin.com/in/johndoe
    GitHub: github.com/johndoe
    
    EDUCATION
    B.Tech in Computer Science
    ABC University, 2024
    CGPA: 8.5
    
    SKILLS
    Flutter, Dart, Firebase, REST API, Git, React, Python, SQL
    
    PROJECTS
    E-commerce App - Built a shopping app using Flutter and Firebase
    
    EXPERIENCE
    Software Intern at Tech Corp - 6 months
    """
    
    report = analyze_resume(sample_resume)
    print(f"Overall Score: {report['overall_score']}%")
    print(f"Skill Match: {report['scores']['skill_match']['score']}%")
    print(f"Format Score: {report['scores']['format']['score']}%")
    print("\nRecommendations:")
    for rec in report["recommendations"]:
        print(f"  {rec}")