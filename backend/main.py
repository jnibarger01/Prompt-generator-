"""
Prompt Generator API
Production-ready FastAPI backend for generating and optimizing prompts
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum
import random
import re
from dataclasses import dataclass

app = FastAPI(
    title="Prompt Generator API",
    description="Generate and optimize prompts for images, workflows, code, and automation",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums and Models
class PromptTypeEnum(str, Enum):
    IMAGE = "image"
    WORKFLOW = "workflow"
    AUTOMATION = "automation"
    CODE = "code"
    ANALYSIS = "analysis"

class SpecificityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

class GenerateRequest(BaseModel):
    prompt_type: PromptTypeEnum
    count: int = Field(default=10, ge=1, le=1000, description="Number of prompts to generate")
    specificity: SpecificityLevel = Field(default=SpecificityLevel.MEDIUM)

class OptimizeRequest(BaseModel):
    vague_prompt: str = Field(..., min_length=1, max_length=500)
    context: Optional[str] = Field(None, max_length=500)

class GenerateResponse(BaseModel):
    prompts: List[str]
    count: int
    prompt_type: str
    specificity: str

class OptimizeResponse(BaseModel):
    original: str
    optimized: str
    detected_type: str

# Core Generator Engine
@dataclass
class PromptTemplate:
    type: str
    base_structure: str
    modifiers: List[str]
    constraints: List[str]
    quality_tokens: List[str]

class PromptGeneratorEngine:
    """Core engine for prompt generation and optimization"""
    
    def __init__(self):
        self.templates = self._init_templates()
    
    def _init_templates(self):
        """Initialize prompt templates for different types"""
        return {
            PromptTypeEnum.IMAGE: [
                PromptTemplate(
                    type="image",
                    base_structure="{subject} {action} {style} {technical}",
                    modifiers=[
                        "photorealistic", "artistic", "abstract", "hyper-detailed",
                        "minimalist", "dramatic", "cinematic", "editorial",
                        "vibrant", "muted tones", "high contrast", "soft lighting"
                    ],
                    constraints=[
                        "maintain exact facial features and proportions",
                        "preserve original identity and likeness",
                        "keep consistent lighting and shadows",
                        "match existing color palette and temperature",
                        "ensure natural blending and transitions",
                        "avoid distortion or warping",
                        "maintain background integrity",
                        "preserve skin texture and tone"
                    ],
                    quality_tokens=[
                        "8k resolution", "professional photography", "studio lighting",
                        "bokeh", "shallow depth of field", "golden hour",
                        "sharp focus", "HDR", "award-winning", "magazine quality"
                    ]
                )
            ],
            PromptTypeEnum.WORKFLOW: [
                PromptTemplate(
                    type="workflow",
                    base_structure="Create a {workflow_type} that {action} with {requirements}",
                    modifiers=[
                        "automated pipeline", "approval process", "data transformation",
                        "notification system", "scheduled task", "event-driven workflow",
                        "multi-stage process", "conditional routing", "parallel execution"
                    ],
                    constraints=[
                        "error handling for each step",
                        "rollback mechanism on failure",
                        "logging and audit trail",
                        "idempotent operations",
                        "timeout handling",
                        "retry logic with exponential backoff",
                        "state persistence",
                        "concurrency control"
                    ],
                    quality_tokens=[
                        "production-ready", "scalable", "maintainable",
                        "well-documented", "testable", "monitored", "resilient"
                    ]
                )
            ],
            PromptTypeEnum.AUTOMATION: [
                PromptTemplate(
                    type="automation",
                    base_structure="Automate {task} that {condition} and {output}",
                    modifiers=[
                        "triggers when", "runs daily at", "monitors continuously",
                        "responds to events", "processes batch", "streams data",
                        "executes on schedule", "reacts to changes"
                    ],
                    constraints=[
                        "handle edge cases and null values",
                        "validate input data",
                        "graceful degradation",
                        "rate limiting and throttling",
                        "concurrent execution safety",
                        "data consistency guarantees",
                        "transaction management",
                        "resource cleanup"
                    ],
                    quality_tokens=[
                        "reliable", "fault-tolerant", "observable",
                        "recoverable", "performant", "secure"
                    ]
                )
            ],
            PromptTypeEnum.CODE: [
                PromptTemplate(
                    type="code",
                    base_structure="Write {language} code that {functionality} with {requirements}",
                    modifiers=[
                        "class implementation", "API endpoint", "data processor",
                        "utility function", "CLI tool", "background service",
                        "database layer", "service integration", "message handler"
                    ],
                    constraints=[
                        "type hints/annotations",
                        "error handling with specific exceptions",
                        "input validation",
                        "unit tests included",
                        "docstrings/comments for complex logic",
                        "no hardcoded values",
                        "configuration externalized",
                        "logging instrumentation"
                    ],
                    quality_tokens=[
                        "production-grade", "efficient", "readable",
                        "maintainable", "well-tested", "documented", "SOLID principles"
                    ]
                )
            ]
        }
    
    def generate(self, prompt_type: PromptTypeEnum, count: int, specificity: SpecificityLevel) -> List[str]:
        """Generate multiple random prompts"""
        templates = self.templates.get(prompt_type, [])
        if not templates:
            raise ValueError(f"No templates for {prompt_type}")
        
        prompts = []
        specificity_levels = {
            SpecificityLevel.LOW: 0.2,
            SpecificityLevel.MEDIUM: 0.5,
            SpecificityLevel.HIGH: 0.8,
            SpecificityLevel.EXTREME: 1.0
        }
        
        constraint_ratio = specificity_levels[specificity]
        
        for _ in range(count):
            template = random.choice(templates)
            
            # Select components based on specificity
            num_modifiers = max(1, int(len(template.modifiers) * constraint_ratio * random.uniform(0.3, 0.7)))
            selected_modifiers = random.sample(template.modifiers, num_modifiers)
            
            num_constraints = int(len(template.constraints) * constraint_ratio)
            selected_constraints = random.sample(template.constraints, num_constraints) if num_constraints > 0 else []
            
            if random.random() < constraint_ratio:
                num_quality = max(1, int(len(template.quality_tokens) * 0.4))
                selected_quality = random.sample(template.quality_tokens, num_quality)
            else:
                selected_quality = []
            
            # Assemble prompt based on type
            if prompt_type == PromptTypeEnum.IMAGE:
                prompt = self._assemble_image_prompt(selected_modifiers, selected_constraints, selected_quality)
            elif prompt_type in [PromptTypeEnum.WORKFLOW, PromptTypeEnum.AUTOMATION]:
                prompt = self._assemble_workflow_prompt(template, selected_modifiers, selected_constraints, selected_quality)
            else:
                prompt = self._assemble_code_prompt(template, selected_modifiers, selected_constraints, selected_quality)
            
            prompts.append(prompt)
        
        return prompts
    
    def _assemble_image_prompt(self, modifiers, constraints, quality):
        """Assemble image generation prompt"""
        subjects = [
            "portrait", "landscape", "product shot", "architectural detail",
            "street photography", "macro photography", "wildlife", "fashion editorial",
            "food photography", "interior design", "nature scene", "urban exploration"
        ]
        
        actions = [
            "showcasing", "highlighting", "emphasizing", "capturing",
            "depicting", "illustrating", "featuring", "presenting"
        ]
        
        subject = random.choice(subjects)
        action = random.choice(actions)
        style = ", ".join(modifiers[:2]) if len(modifiers) >= 2 else modifiers[0] if modifiers else "realistic"
        
        prompt = f"{style.capitalize()} {subject} {action} the subject"
        
        if constraints:
            prompt += f". Must preserve: {', '.join(constraints[:3])}"
        
        if quality:
            prompt += f". Quality requirements: {', '.join(quality)}"
        
        return prompt
    
    def _assemble_workflow_prompt(self, template, modifiers, constraints, quality):
        """Assemble workflow/automation prompt"""
        tasks = [
            "data ingestion", "report generation", "approval routing",
            "notification dispatch", "backup process", "sync operation",
            "data validation", "record processing", "file transformation"
        ]
        
        task = random.choice(tasks)
        condition = random.choice(modifiers) if modifiers else "on trigger"
        
        prompt = f"Create {task} workflow that {condition}"
        
        if constraints:
            prompt += f". Requirements: {', '.join(constraints[:4])}"
        
        if quality:
            prompt += f". Standards: {', '.join(quality)}"
        
        return prompt
    
    def _assemble_code_prompt(self, template, modifiers, constraints, quality):
        """Assemble code generation prompt"""
        languages = ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java"]
        functionality = [
            "parses CSV files", "makes HTTP requests", "processes queue messages",
            "validates user input", "generates reports", "manages database connections",
            "handles file uploads", "implements caching", "processes webhooks"
        ]
        
        lang = random.choice(languages)
        func = random.choice(functionality)
        modifier = random.choice(modifiers) if modifiers else "function"
        
        prompt = f"Write {lang} {modifier} that {func}"
        
        if constraints:
            prompt += f". Must include: {', '.join(constraints[:4])}"
        
        if quality:
            prompt += f". Quality: {', '.join(quality)}"
        
        return prompt
    
    def optimize(self, vague_prompt: str, context: Optional[str] = None) -> tuple[str, str]:
        """Optimize a vague prompt into a specific one"""
        prompt_type = self._detect_prompt_type(vague_prompt)
        
        if context:
            optimized = f"{context}. "
        else:
            optimized = ""
        
        intent = self._extract_intent(vague_prompt)
        
        if prompt_type == PromptTypeEnum.IMAGE:
            optimized += self._optimize_image_prompt(vague_prompt, intent)
        elif prompt_type == PromptTypeEnum.WORKFLOW:
            optimized += self._optimize_workflow_prompt(vague_prompt, intent)
        elif prompt_type == PromptTypeEnum.CODE:
            optimized += self._optimize_code_prompt(vague_prompt, intent)
        else:
            optimized += self._optimize_generic_prompt(vague_prompt, intent)
        
        return optimized.strip(), prompt_type.value
    
    def _detect_prompt_type(self, prompt: str) -> PromptTypeEnum:
        """Detect prompt type from content"""
        prompt_lower = prompt.lower()
        
        image_keywords = ["photo", "image", "picture", "hair", "face", "look", "style", "portrait", "background"]
        workflow_keywords = ["workflow", "process", "pipeline", "approval", "automate"]
        code_keywords = ["code", "function", "script", "program", "write", "implement", "algorithm"]
        
        if any(kw in prompt_lower for kw in image_keywords):
            return PromptTypeEnum.IMAGE
        elif any(kw in prompt_lower for kw in workflow_keywords):
            return PromptTypeEnum.WORKFLOW
        elif any(kw in prompt_lower for kw in code_keywords):
            return PromptTypeEnum.CODE
        else:
            return PromptTypeEnum.IMAGE
    
    def _extract_intent(self, prompt: str):
        """Extract user intent from prompt"""
        return {
            "action": self._find_action(prompt),
            "target": self._find_target(prompt)
        }
    
    def _find_action(self, prompt: str):
        actions = ["give", "make", "create", "change", "modify", "show", "generate", "build"]
        for action in actions:
            if action in prompt.lower():
                return action
        return "create"
    
    def _find_target(self, prompt: str):
        targets = ["hair", "hairstyle", "haircut", "photo", "image", "code", "workflow", "background"]
        for target in targets:
            if target in prompt.lower():
                return target
        return "item"
    
    def _optimize_image_prompt(self, vague: str, intent):
        """Optimize image prompts with precision"""
        base = []
        
        if "photo" in vague.lower() or "image" in vague.lower():
            base.append("Using the uploaded photo, keep the person or subject's face, identity, and proportions exactly the same")
        
        if "hair" in vague.lower() or "haircut" in vague.lower():
            style = self._extract_hair_style(vague)
            base.append(f"Change only their hairstyle to {style}")
            base.append("The haircut should look realistic and naturally blended with the existing hair texture, color, lighting, and head shape")
        elif "background" in vague.lower():
            base.append("Change only the background while preserving the subject completely")
            base.append("Ensure seamless integration with proper lighting, shadows, and depth matching")
        else:
            base.append(f"Modify the {intent['target']} while preserving all other aspects")
        
        base.append("Do not alter facial features, expression, age, or any unspecified elements")
        
        return ". ".join(base)
    
    def _extract_hair_style(self, prompt: str):
        """Extract and describe hair style"""
        style_map = {
            "bowl cut": "a classic bowl cut: straight, even fringe across the forehead, rounded silhouette around the head, clean and symmetrical",
            "pixie": "a modern pixie cut: short on sides and back, slightly longer on top, textured and layered",
            "bob": "a sleek bob: chin-length, blunt cut, straight and polished",
            "mullet": "a mullet: short in front and on top, long in the back, with clear distinction between lengths",
            "undercut": "an undercut: shaved or very short sides and back, longer hair on top with clear contrast",
            "fade": "a fade: gradual transition from short to longer hair, clean taper on sides and back",
            "buzz": "a buzz cut: uniform short length all around, clean and low-maintenance",
            "crew cut": "a crew cut: short on sides, slightly longer on top, classic military style"
        }
        
        for style, description in style_map.items():
            if style in prompt.lower():
                return description
        
        return "the requested hairstyle with appropriate length, shape, and styling details"
    
    def _optimize_workflow_prompt(self, vague: str, intent):
        """Optimize workflow prompts"""
        base = []
        base.append(f"Create a production-ready workflow that {intent['action']}s {intent['target']}")
        base.append("Include: error handling for each step, rollback mechanism on failure, logging and audit trail, retry logic with exponential backoff")
        base.append("Ensure idempotent operations, timeout handling, monitoring hooks, and state persistence")
        return ". ".join(base)
    
    def _optimize_code_prompt(self, vague: str, intent):
        """Optimize code prompts"""
        base = []
        base.append(f"Write production-grade code that {intent['action']}s {intent['target']}")
        base.append("Must include: type hints/annotations, comprehensive error handling with specific exceptions, input validation, unit tests, docstrings for complex logic")
        base.append("No hardcoded values, configuration externalized, efficient algorithm choices, clear variable names, logging instrumentation")
        return ". ".join(base)
    
    def _optimize_generic_prompt(self, vague: str, intent):
        """Fallback optimizer"""
        return f"Please provide a detailed, specific implementation of: {vague}. Include all necessary constraints, requirements, and quality standards for production use."

# Initialize engine
engine = PromptGeneratorEngine()

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Prompt Generator API",
        "version": "1.0.0"
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate_prompts(request: GenerateRequest):
    """Generate multiple random prompts"""
    try:
        prompts = engine.generate(
            prompt_type=request.prompt_type,
            count=request.count,
            specificity=request.specificity
        )
        
        return GenerateResponse(
            prompts=prompts,
            count=len(prompts),
            prompt_type=request.prompt_type.value,
            specificity=request.specificity.value
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_prompt(request: OptimizeRequest):
    """Optimize a vague prompt into a specific one"""
    try:
        optimized, detected_type = engine.optimize(
            vague_prompt=request.vague_prompt,
            context=request.context
        )
        
        return OptimizeResponse(
            original=request.vague_prompt,
            optimized=optimized,
            detected_type=detected_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/types")
async def get_prompt_types():
    """Get available prompt types"""
    return {
        "types": [t.value for t in PromptTypeEnum],
        "specificity_levels": [s.value for s in SpecificityLevel]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
