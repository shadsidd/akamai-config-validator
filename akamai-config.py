import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
import json
from typing import List, Dict

DEFAULT_RULES = [
    "WAF_ENABLED: Ensure WAF is enabled for all endpoints",
    "RATE_LIMIT: Verify rate limiting is configured for API endpoints",
    "GEO_BLOCKING: Check geo-blocking configuration for sensitive regions",
    "TLS_VERSION: Validate TLS 1.2+ enforcement",
    "BOT_MANAGEMENT: Review bot management rules",
    "DDOS_PROTECTION: Confirm DDoS protection settings"
]

def create_security_agent(model_name: str, api_key: str) -> Agent:
    """Create an Security agent for security analysis"""
    if "gpt" in model_name.lower():
        model = OpenAIChat(api_key=api_key)
    elif "gemini" in model_name.lower():
        model = Gemini(api_key=api_key)
    else:
        raise ValueError(f"Unsupported model: {model_name}")
    
    return Agent(
        model=model,
        description="You are an expert security analyst specializing in Akamai configurations.",
        instructions=[
            "Analyze Akamai security configurations against provided security rules",
            "Provide detailed security assessments with clear recommendations",
            "Score configurations based on compliance with security rules",
            "Identify critical security gaps and vulnerabilities",
            "Suggest specific improvements for each security finding"
        ],
        markdown=True,
        reasoning=True
    )

def init_session_state():
    """Initialize Streamlit session state"""
    if "custom_rules" not in st.session_state:
        st.session_state.custom_rules = []

def render_sidebar() -> tuple:
    """Render sidebar with LLM selection and API key input"""
    with st.sidebar:
        st.header("🔧 Settings")
        model = st.selectbox(
            "Select Language Model",
            ["gpt-4", "gemini-pro"],
            help="Choose the AI model for security analysis"
        )
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Enter your API key for the selected model"
        )
        
        st.markdown("---")
        st.markdown("### 📖 About")
        st.info("AI-powered Akamai security configuration analyzer - Created by Shadab")
        
    return model, api_key

def render_rules_section():
    """Render security rules section"""
    st.subheader("🛡️ Security Rules")
    
    # Default rules display
    with st.expander("Default Security Rules", expanded=True):
        for rule in DEFAULT_RULES:
            st.write(f"✓ {rule}")
    
    # Custom rules input
    st.subheader("➕ Evaluate the configuration against a Custom Rule")
    col1, col2 = st.columns([3, 1])
    with col1:
        new_rule = st.text_input(
            "",
            placeholder="Enter a new security rule",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("Add", use_container_width=True) and new_rule:
            st.session_state.custom_rules.append(new_rule)
            st.success("Rule added!")
    
    # Display custom rules
    if st.session_state.custom_rules:
        with st.expander("Custom Rules", expanded=True):
            for i, rule in enumerate(st.session_state.custom_rules):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"🔹 {rule}")
                with col2:
                    if st.button("Remove", key=f"remove_{i}", use_container_width=True):
                        st.session_state.custom_rules.pop(i)
                        st.rerun()

def analyze_config(agent: Agent, config: Dict, custom_rules: List[str]) -> str:
    """Analyze configuration using Security agent"""
    rules = DEFAULT_RULES + custom_rules
    
    prompt = f"""Analyze this Akamai security configuration against the following rules:
    
Rules to check:
{chr(10).join(f'- {rule}' for rule in rules)}

Configuration:
```json
{json.dumps(config, indent=2)}
```

Provide a detailed security analysis with:
1. Overall security score
2. Rule-by-rule assessment
3. Critical findings
4. Recommendations
"""
    return agent.run(prompt).content

def main():
    st.set_page_config(
        page_title="Akamai Security Analyzer",
        page_icon="🔒",
        layout="wide"
    )
    
    init_session_state()
    model, api_key = render_sidebar()
    
    st.title("🔒 Akamai Security Configuration Analyzer")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Upload Akamai Configuration (JSON)",
        type=["json"],
        help="Drag and drop or click to upload your Akamai configuration file"
    )
    
    render_rules_section()
    
    # Analysis section
    if uploaded_file and api_key:
        if st.button("🔍 Analyze Configuration", use_container_width=True):
            with st.spinner("Analyzing security configuration..."):
                try:
                    config_data = json.load(uploaded_file)
                    agent = create_security_agent(model, api_key)
                    analysis = analyze_config(
                        agent,
                        config_data,
                        st.session_state.custom_rules
                    )
                    
                    st.markdown("### 📊 Security Analysis Report")
                    st.markdown(analysis)
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
    elif not api_key:
        st.warning("⚠️ Please enter your API key in the sidebar")
    elif not uploaded_file:
        st.info("📁 Please upload an Akamai configuration file")

if __name__ == "__main__":
    main()