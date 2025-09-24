from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import re

app = Flask(__name__)

class CareerNavigator:
    def __init__(self):
        # Industry skills database (simplified for demo)
        self.industry_skills = {
            "software_engineer": {
                "core": ["Python", "JavaScript", "Git", "SQL", "Data Structures", "Algorithms"],
                "frameworks": ["React", "Node.js", "Django", "Flask", "Express"],
                "tools": ["Docker", "AWS", "Jenkins", "Kubernetes"],
                "soft_skills": ["Problem Solving", "Communication", "Teamwork", "Time Management"]
            },
            "data_scientist": {
                "core": ["Python", "R", "Statistics", "Machine Learning", "SQL", "Mathematics"],
                "frameworks": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch"],
                "tools": ["Jupyter", "Tableau", "Power BI", "Apache Spark"],
                "soft_skills": ["Analytical Thinking", "Communication", "Business Acumen", "Curiosity"]
            },
            "product_manager": {
                "core": ["Product Strategy", "Market Research", "User Experience", "Analytics"],
                "frameworks": ["Agile", "Scrum", "Design Thinking", "Lean Startup"],
                "tools": ["Jira", "Figma", "Google Analytics", "A/B Testing"],
                "soft_skills": ["Leadership", "Communication", "Strategic Thinking", "Stakeholder Management"]
            },
            "digital_marketer": {
                "core": ["SEO", "SEM", "Content Marketing", "Social Media", "Analytics"],
                "frameworks": ["Growth Hacking", "Inbound Marketing", "Customer Journey Mapping"],
                "tools": ["Google Ads", "Facebook Ads", "HubSpot", "Mailchimp", "Google Analytics"],
                "soft_skills": ["Creativity", "Communication", "Data Analysis", "Adaptability"]
            }
        }
        
        self.learning_resources = {
            "Python": ["Codecademy Python Course", "Python.org Tutorial", "Automate the Boring Stuff"],
            "JavaScript": ["MDN Web Docs", "JavaScript.info", "FreeCodeCamp"],
            "Machine Learning": ["Coursera ML Course", "Kaggle Learn", "Fast.ai"],
            "Product Strategy": ["Product School", "Coursera Product Management", "Mind the Product"],
            "SEO": ["Moz Beginner's Guide", "Google SEO Starter Guide", "SEMrush Academy"]
        }

    def analyze_skills_gap(self, current_skills, target_role):
        """Analyze the gap between current skills and target role requirements"""
        target_role_key = target_role.lower().replace(" ", "_")
        
        if target_role_key not in self.industry_skills:
            return {"error": "Target role not found in our database"}
        
        required_skills = self.industry_skills[target_role_key]
        current_skills_lower = [skill.lower() for skill in current_skills]
        
        gaps = {
            "core": [],
            "frameworks": [],
            "tools": [],
            "soft_skills": []
        }
        
        for category, skills in required_skills.items():
            for skill in skills:
                if skill.lower() not in current_skills_lower:
                    gaps[category].append(skill)
        
        return gaps

    def generate_learning_path(self, skills_gap, time_available, learning_style):
        """Generate a personalized learning path"""
        path = {
            "immediate": [],
            "medium_term": [],
            "long_term": []
        }
        
        # Prioritize core skills first
        core_gaps = skills_gap.get("core", [])
        framework_gaps = skills_gap.get("frameworks", [])
        tool_gaps = skills_gap.get("tools", [])
        soft_skill_gaps = skills_gap.get("soft_skills", [])
        
        # Immediate (1-2 weeks)
        if core_gaps:
            path["immediate"].extend(core_gaps[:2])
        
        # Medium term (3-6 months)
        if len(core_gaps) > 2:
            path["medium_term"].extend(core_gaps[2:])
        path["medium_term"].extend(framework_gaps[:2])
        path["medium_term"].extend(soft_skill_gaps[:2])
        
        # Long term (1-3 years)
        path["long_term"].extend(framework_gaps[2:])
        path["long_term"].extend(tool_gaps)
        path["long_term"].extend(soft_skill_gaps[2:])
        
        return path

    def get_learning_resources(self, skills):
        """Get learning resources for specific skills"""
        resources = {}
        for skill in skills:
            if skill in self.learning_resources:
                resources[skill] = self.learning_resources[skill]
            else:
                resources[skill] = [f"Search for '{skill}' courses on Coursera, Udemy, or YouTube"]
        return resources

    def create_smart_goals(self, learning_path, time_available):
        """Create SMART goals based on learning path"""
        goals = []
        
        # Immediate goals
        for skill in learning_path["immediate"]:
            goal = {
                "skill": skill,
                "specific": f"Learn {skill} fundamentals",
                "measurable": "Complete beginner course and build 1 project",
                "achievable": "Yes, with dedicated study time",
                "relevant": f"Essential for target role",
                "time_bound": "2 weeks",
                "theme": "Skill Accelerator Path"
            }
            goals.append(goal)
        
        # Medium term goals
        for skill in learning_path["medium_term"][:3]:  # Limit to 3 for focus
            goal = {
                "skill": skill,
                "specific": f"Gain intermediate proficiency in {skill}",
                "measurable": "Complete intermediate course and 2-3 projects",
                "achievable": "Yes, with consistent practice",
                "relevant": f"Important for career advancement",
                "time_bound": "3-6 months",
                "theme": "Real-world Projects"
            }
            goals.append(goal)
        
        return goals

    def generate_career_roadmap(self, user_data):
        """Generate complete career roadmap"""
        current_skills = user_data.get("current_skills", [])
        target_role = user_data.get("target_role", "")
        time_available = user_data.get("time_available", 5)
        learning_style = user_data.get("learning_style", "courses")
        current_role = user_data.get("current_role", "")
        experience = user_data.get("experience", "")
        
        # Analyze skills gap
        skills_gap = self.analyze_skills_gap(current_skills, target_role)
        
        if "error" in skills_gap:
            return skills_gap
        
        # Generate learning path
        learning_path = self.generate_learning_path(skills_gap, time_available, learning_style)
        
        # Get learning resources
        all_skills = learning_path["immediate"] + learning_path["medium_term"] + learning_path["long_term"]
        resources = self.get_learning_resources(all_skills[:10])  # Limit to top 10
        
        # Create SMART goals
        smart_goals = self.create_smart_goals(learning_path, time_available)
        
        # Generate structured response
        response = {
            "solution_summary": f"Based on your current role as {current_role} and goal to become a {target_role}, I've created a personalized roadmap focusing on {len(all_skills)} key skills. Your next milestone is mastering {', '.join(learning_path['immediate'][:2])} within the next 2 weeks.",
            
            "problem_statement": f"The gap between your current skills and {target_role} requirements includes {len(all_skills)} skills across technical and soft skill areas. Key missing competencies are in {', '.join(skills_gap.get('core', [])[:3])}.",
            
            "techniques": {
                "skill_analysis": "AI-powered comparison of your skills against industry standards",
                "skill_mapping": "Intelligent mapping of required skills for your target role",
                "resource_recommendation": "Curated learning resources based on your learning style",
                "project_suggestions": "Practical projects to build real-world experience"
            },
            
            "frameworks": {
                "blooms_taxonomy": "Learning progression from remembering → understanding → applying → analyzing",
                "t_shaped_skills": f"Broad foundation in {len(skills_gap.get('soft_skills', []))} soft skills + deep expertise in {', '.join(skills_gap.get('core', [])[:2])}",
                "smart_goals": smart_goals
            },
            
            "steps": {
                "immediate": {
                    "timeframe": "Next 1-2 weeks",
                    "focus": learning_path["immediate"],
                    "actions": [f"Start learning {skill}" for skill in learning_path["immediate"]]
                },
                "medium_term": {
                    "timeframe": "Next 3-6 months", 
                    "focus": learning_path["medium_term"],
                    "actions": [f"Build projects using {skill}" for skill in learning_path["medium_term"][:3]]
                },
                "long_term": {
                    "timeframe": "1-3 years",
                    "focus": learning_path["long_term"],
                    "actions": [f"Master advanced {skill} concepts" for skill in learning_path["long_term"][:3]]
                }
            },
            
            "data_requirements": {
                "current_role": current_role,
                "target_role": target_role,
                "experience": experience,
                "time_available": f"{time_available} hours/week",
                "learning_style": learning_style,
                "additional_needed": ["Portfolio projects", "Certifications earned", "Preferred industries"]
            },
            
            "themes": {
                "skill_accelerator": learning_path["immediate"],
                "real_world_projects": [f"Build a {skill} project" for skill in learning_path["medium_term"][:3]],
                "learning_by_doing": "Hands-on practice with real datasets and scenarios",
                "career_milestones": ["Complete beginner courses", "Build portfolio", "Apply for target roles"]
            },
            
            "learning_resources": resources,
            "skills_gap": skills_gap,
            "personalization_score": min(100, len(current_skills) * 10 + (10 if current_role else 0) + (10 if experience else 0))
        }
        
        return response

# Initialize the career navigator
navigator = CareerNavigator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_career():
    try:
        user_data = request.json
        result = navigator.generate_career_roadmap(user_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/skills/<role>')
def get_role_skills(role):
    role_key = role.lower().replace(" ", "_")
    if role_key in navigator.industry_skills:
        return jsonify(navigator.industry_skills[role_key])
    return jsonify({"error": "Role not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
