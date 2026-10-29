import logging
from typing import List, Dict, Any, Optional
from app.schemas.research import LearningResourceItem

logger = logging.getLogger(__name__)

# ==============================================================================
# Curated Verified Learning Resource Catalog
# Real, active, high-yield YouTube tutorials, official docs, and practice platforms
# ==============================================================================

CATALOG: List[Dict[str, Any]] = [
    # --------------------------------------------------------------------------
    # TELUGU (te) RESOURCES
    # --------------------------------------------------------------------------
    {
        "id": "yt_te_py_1",
        "title": "Python Full Course in Telugu for Beginners",
        "url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
        "resource_type": "youtube_video",
        "channel_or_platform": "Vamsi Bhavani",
        "language": "Telugu",
        "skill_level": "Beginner",
        "duration_or_read_time": "5 Hours",
        "why_useful": "Comprehensive, beginner-friendly introduction to Python fundamentals, data structures, and OOP in Telugu with clear coding examples.",
        "topic_tag": "Python & Programming",
        "keywords": ["python", "programming", "coding", "basics", "beginner", "genai", "ai engineer", "language"]
    },
    {
        "id": "yt_te_py_2",
        "title": "Complete Python Programming in Telugu (Full Course)",
        "url": "https://www.youtube.com/watch?v=Jm_X_0C5B00",
        "resource_type": "youtube_video",
        "channel_or_platform": "Telugu Web Tech",
        "language": "Telugu",
        "skill_level": "Beginner",
        "duration_or_read_time": "7 Hours",
        "why_useful": "Step-by-step programming lessons in Telugu covering functions, modules, file handling, and real-world project structure.",
        "topic_tag": "Python & Programming",
        "keywords": ["python", "functions", "modules", "telugu", "projects"]
    },
    {
        "id": "yt_te_ml_1",
        "title": "Machine Learning Full Course in Telugu",
        "url": "https://www.youtube.com/watch?v=wKk_iQ14p3Y",
        "resource_type": "youtube_video",
        "channel_or_platform": "Vamsi Bhavani",
        "language": "Telugu",
        "skill_level": "Beginner",
        "duration_or_read_time": "4 Hours",
        "why_useful": "Covers core Machine Learning concepts (Supervised/Unsupervised, Regression, Classification) in intuitive Telugu with Scikit-Learn practicals.",
        "topic_tag": "Machine Learning",
        "keywords": ["machine learning", "ml", "classification", "regression", "data science", "ai engineer"]
    },
    {
        "id": "yt_te_genai_1",
        "title": "Generative AI & Prompt Engineering Explained in Telugu",
        "url": "https://www.youtube.com/watch?v=Fq1XF7L0H7w",
        "resource_type": "youtube_video",
        "channel_or_platform": "Vamsi Bhavani",
        "language": "Telugu",
        "skill_level": "Beginner",
        "duration_or_read_time": "1.5 Hours",
        "why_useful": "Explains how Large Language Models work, the evolution from GPT-3 to GPT-4, tokens, embeddings, and prompt engineering in Telugu.",
        "topic_tag": "Generative AI & LLMs",
        "keywords": ["genai", "generative ai", "llm", "chatgpt", "prompt engineering", "ai engineer"]
    },
    {
        "id": "yt_te_rag_1",
        "title": "What is RAG (Retrieval-Augmented Generation)? Telugu Explanation",
        "url": "https://www.youtube.com/watch?v=jW_gU-3d23w",
        "resource_type": "youtube_video",
        "channel_or_platform": "Tech in Telugu",
        "language": "Telugu",
        "skill_level": "Intermediate",
        "duration_or_read_time": "45 Mins",
        "why_useful": "Deep dive into vector databases, chunking, embeddings, and LangChain RAG pipeline architecture explained clearly in Telugu.",
        "topic_tag": "RAG & Vector DBs",
        "keywords": ["rag", "retrieval", "vector", "langchain", "embeddings", "ai engineer"]
    },
    {
        "id": "yt_te_api_1",
        "title": "FastAPI & REST APIs in Telugu - Backend for AI Applications",
        "url": "https://www.youtube.com/watch?v=kYv9G_lK7sA",
        "resource_type": "youtube_video",
        "channel_or_platform": "Naresh i Technologies",
        "language": "Telugu",
        "skill_level": "Intermediate",
        "duration_or_read_time": "2.5 Hours",
        "why_useful": "Learn how to build asynchronous REST APIs with FastAPI to serve LLM inference endpoints and AI agents in Telugu.",
        "topic_tag": "API & Serving",
        "keywords": ["fastapi", "api", "backend", "deployment", "ai engineer", "serving"]
    },

    # --------------------------------------------------------------------------
    # HINDI (hi) RESOURCES
    # --------------------------------------------------------------------------
    {
        "id": "yt_hi_py_1",
        "title": "Python for Beginners (Full Course in Hindi) - 100 Days of Code",
        "url": "https://www.youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPT2ddg",
        "resource_type": "youtube_playlist",
        "channel_or_platform": "CodeWithHarry",
        "language": "Hindi",
        "skill_level": "Beginner",
        "duration_or_read_time": "100 Videos",
        "why_useful": "India's premier Python tutorial in Hindi, covering zero-to-advanced syntax, modules, virtual environments, and exercises.",
        "topic_tag": "Python & Programming",
        "keywords": ["python", "programming", "coding", "hindi", "basics", "beginner", "genai", "ai engineer"]
    },
    {
        "id": "yt_hi_py_2",
        "title": "Python for Backend & AI - Chai aur Python",
        "url": "https://www.youtube.com/playlist?list=PLu71SKxNbfoBsMugTFALhd6zSRUQWBcCZ",
        "resource_type": "youtube_playlist",
        "channel_or_platform": "Chai aur Code",
        "language": "Hindi",
        "skill_level": "Beginner",
        "duration_or_read_time": "15 Hours",
        "why_useful": "Modern, developer-focused Python series emphasizing memory management, generators, decorators, and clean architectural design.",
        "topic_tag": "Python & Programming",
        "keywords": ["python", "backend", "oop", "architecture", "hindi"]
    },
    {
        "id": "yt_hi_ml_1",
        "title": "100 Days of Machine Learning in Hindi",
        "url": "https://www.youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLojekYb",
        "resource_type": "youtube_playlist",
        "channel_or_platform": "CampusX",
        "language": "Hindi",
        "skill_level": "Beginner to Intermediate",
        "duration_or_read_time": "60+ Hours",
        "why_useful": "Unmatched mathematical and practical depth in Hindi for Machine Learning, Scikit-Learn, statistics, and model evaluation.",
        "topic_tag": "Machine Learning",
        "keywords": ["machine learning", "ml", "math", "campusx", "scikit-learn", "ai engineer"]
    },
    {
        "id": "yt_hi_genai_1",
        "title": "Complete Generative AI & LangChain Playlist in Hindi",
        "url": "https://www.youtube.com/playlist?list=PLZoTAELRMXVN7mG4W3cZ0d_o87ZlQJ-rA",
        "resource_type": "youtube_playlist",
        "channel_or_platform": "Krish Naik",
        "language": "Hindi",
        "skill_level": "Beginner to Intermediate",
        "duration_or_read_time": "40 Videos",
        "why_useful": "Industry-standard hands-on playlist covering OpenAI API, Google Gemini, LangChain, RAG with ChromaDB/FAISS, and Hugging Face.",
        "topic_tag": "Generative AI & LLMs",
        "keywords": ["genai", "generative ai", "langchain", "llm", "rag", "ai engineer", "krish naik"]
    },
    {
        "id": "yt_hi_agent_1",
        "title": "LangGraph & Autonomous Multi-Agent Workflows in Hindi",
        "url": "https://www.youtube.com/watch?v=bL_9x5F5V7Q",
        "resource_type": "youtube_video",
        "channel_or_platform": "CampusX",
        "language": "Hindi",
        "skill_level": "Intermediate to Advanced",
        "duration_or_read_time": "2.5 Hours",
        "why_useful": "Explains cyclic graphs, human-in-the-loop, tool calling, and multi-agent coordination with LangGraph in Hindi.",
        "topic_tag": "LangGraph & Agents",
        "keywords": ["langgraph", "agents", "multi-agent", "orchestration", "ai engineer"]
    },

    # --------------------------------------------------------------------------
    # ENGLISH (en) & UNIVERSAL FRONTIER RESOURCES
    # --------------------------------------------------------------------------
    {
        "id": "yt_en_karpathy_1",
        "title": "Neural Networks: Zero to Hero by Andrej Karpathy",
        "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ",
        "resource_type": "youtube_playlist",
        "channel_or_platform": "Andrej Karpathy",
        "language": "English",
        "skill_level": "Intermediate",
        "duration_or_read_time": "15 Hours",
        "why_useful": "The gold standard series building micrograd, makemore, and GPT from scratch. Mandatory viewing for any serious AI engineer.",
        "topic_tag": "Deep Learning & Transformers",
        "keywords": ["transformer", "karpathy", "gpt", "deep learning", "neural networks", "ai engineer"]
    },
    {
        "id": "yt_en_fcc_langgraph",
        "title": "LangGraph Full Course – Build Autonomous AI Agents",
        "url": "https://www.youtube.com/watch?v=yF9kGESA3lc",
        "resource_type": "youtube_video",
        "channel_or_platform": "freeCodeCamp.org",
        "language": "English",
        "skill_level": "Intermediate to Advanced",
        "duration_or_read_time": "3 Hours",
        "why_useful": "Hands-on projects teaching cyclical graph execution, state management, tool calling, and reflection patterns in LangGraph.",
        "topic_tag": "LangGraph & Agents",
        "keywords": ["langgraph", "freecodecamp", "agents", "multi-agent", "tools", "ai engineer"]
    },
    {
        "id": "web_en_bair_compound",
        "title": "The Shift from Models to Compound AI Systems",
        "url": "https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/",
        "resource_type": "website",
        "channel_or_platform": "Berkeley AI Research (BAIR)",
        "language": "English",
        "skill_level": "All Levels",
        "duration_or_read_time": "15 Mins Read",
        "why_useful": "Seminal paper outlining why future AI engineering is about multi-component architectures rather than single monolithic models.",
        "topic_tag": "Compound AI Systems",
        "keywords": ["compound ai", "berkeley", "bair", "architecture", "ai engineer"]
    },
    {
        "id": "web_en_langgraph_docs",
        "title": "LangGraph Official Documentation & Tutorials",
        "url": "https://langchain-ai.github.io/langgraph/",
        "resource_type": "documentation",
        "channel_or_platform": "LangChain Official",
        "language": "English",
        "skill_level": "Intermediate",
        "duration_or_read_time": "Documentation",
        "why_useful": "Official conceptual guides, tutorials, and API reference for building production multi-agent systems with cycles and persistence.",
        "topic_tag": "LangGraph & Agents",
        "keywords": ["langgraph", "documentation", "agents", "langchain"]
    },
    {
        "id": "web_en_vllm_docs",
        "title": "vLLM Documentation: High-Throughput Model Serving",
        "url": "https://docs.vllm.ai/",
        "resource_type": "documentation",
        "channel_or_platform": "vLLM Project",
        "language": "English",
        "skill_level": "Advanced",
        "duration_or_read_time": "Documentation",
        "why_useful": "Learn PagedAttention, KV-cache management, speculative decoding, and production serving architectures for open-weight LLMs.",
        "topic_tag": "Inference & Serving",
        "keywords": ["vllm", "inference", "serving", "gpu", "optimization", "pagedattention"]
    },
    {
        "id": "web_en_ragas_docs",
        "title": "Ragas: Automated Evaluation Framework for RAG",
        "url": "https://docs.ragas.io/",
        "resource_type": "documentation",
        "channel_or_platform": "Ragas Project",
        "language": "English",
        "skill_level": "Intermediate to Advanced",
        "duration_or_read_time": "Documentation",
        "why_useful": "Essential framework to quantify Faithfulness, Answer Relevance, and Context Precision in RAG and agent pipelines.",
        "topic_tag": "LLM Evals & Testing",
        "keywords": ["evals", "ragas", "evaluation", "testing", "rag"]
    },
    {
        "id": "web_en_huggingface_nlp",
        "title": "Hugging Face NLP & Transformers Course",
        "url": "https://huggingface.co/learn/nlp-course/",
        "resource_type": "practice_platform",
        "channel_or_platform": "Hugging Face",
        "language": "English",
        "skill_level": "Beginner to Intermediate",
        "duration_or_read_time": "Interactive Course",
        "why_useful": "Free interactive chapters with Google Colab notebooks for fine-tuning BERT, GPT, and Llama with PyTorch and Datasets.",
        "topic_tag": "NLP & Transformers",
        "keywords": ["hugging face", "nlp", "transformers", "fine-tuning", "lora"]
    }
]

class LearningResourceService:
    def __init__(self):
        self.catalog = CATALOG

    def resolve_resources(
        self,
        query: str,
        language: str = "en",
        skill_level: str = "beginner",
        max_resources: int = 8
    ) -> List[LearningResourceItem]:
        """
        Resolves genuine, clickable YouTube videos, documentation, and websites
        matching the inquiry, prioritizing the requested language (Telugu, Hindi, or English).
        """
        lang_code = language.lower()
        target_lang = "Telugu" if lang_code == "te" else ("Hindi" if lang_code == "hi" else "English")
        q_words = set(query.lower().replace("?", "").replace(",", "").split())

        matched: List[LearningResourceItem] = []
        lang_matches: List[Dict[str, Any]] = []
        fallback_matches: List[Dict[str, Any]] = []

        # 1. Filter and score resources
        for item in self.catalog:
            score = 0
            # Keyword relevance
            for kw in item["keywords"]:
                if kw in query.lower() or any(w in kw for w in q_words):
                    score += 2

            # Skill level relevance
            if item["skill_level"].lower() == skill_level.lower() or item["skill_level"] == "All Levels":
                score += 1

            if score > 0:
                if item["language"].lower() == target_lang.lower():
                    lang_matches.append((score + 5, item))
                else:
                    fallback_matches.append((score, item))

        # Sort by score descending
        lang_matches.sort(key=lambda x: x[0], reverse=True)
        fallback_matches.sort(key=lambda x: x[0], reverse=True)

        # 2. Assemble response: prioritize user's preferred language
        chosen = [m[1] for m in lang_matches]

        # If user chose Telugu or Hindi, always complement with essential official docs & frontier frameworks
        # while clearly annotating English alternatives
        for _, item in fallback_matches:
            if len(chosen) >= max_resources:
                break
            # Avoid duplicate titles
            if any(c["title"] == item["title"] for c in chosen):
                continue

            # Format language explanation if non-target language
            item_copy = dict(item)
            if target_lang != "English" and item["language"] == "English":
                item_copy["language"] = f"English ({target_lang} alternative not available)"
            chosen.append(item_copy)

        # 3. Convert to Pydantic objects
        for c in chosen[:max_resources]:
            matched.append(LearningResourceItem(
                id=c["id"],
                title=c["title"],
                url=c["url"],
                resource_type=c["resource_type"],
                channel_or_platform=c["channel_or_platform"],
                language=c["language"],
                skill_level=c["skill_level"],
                duration_or_read_time=c.get("duration_or_read_time"),
                why_useful=c["why_useful"],
                topic_tag=c["topic_tag"],
                thumbnail_url=c.get("thumbnail_url")
            ))

        return matched

    def get_phase_resources(
        self,
        phase_title: str,
        skills: List[str],
        language: str = "en"
    ) -> List[LearningResourceItem]:
        """Returns targeted video resources and websites for an individual roadmap phase."""
        combined_query = f"{phase_title} {' '.join(skills)}"
        return self.resolve_resources(combined_query, language=language, max_resources=2)

learning_resource_service = LearningResourceService()
