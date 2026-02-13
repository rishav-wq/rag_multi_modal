import streamlit as st
from pathlib import Path
from typing import List, Dict, Any

from rag.config import ensure_data_dir
from rag.ingest import ingest_documents
from rag.llm import generate_answer
from rag.retriever import Retriever

# Page config
st.set_page_config(
    page_title="Construction RAG Assistant",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .context-chunk {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid #1f77b4;
    }
    .source-badge {
        background-color: #e1e4e8;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'retriever' not in st.session_state:
    st.session_state.retriever = Retriever(top_k=5)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Mode selection
    mode = st.radio(
        "LLM Mode",
        ["online", "offline"],
        format_func=lambda x: "🌐 Online (Groq)" if x == "online" else "💻 Offline (Ollama)",
        help="Online uses Groq API (fast), Offline uses local Ollama"
    )
    
    st.markdown("---")
    
    # Index management
    st.markdown("### 📚 Index Management")
    if st.button("🔄 Build Index", use_container_width=True):
        with st.spinner("Building index... This may take a minute..."):
            try:
                ensure_data_dir()
                ingest_documents()
                st.success("✅ Index built successfully!")
            except Exception as e:
                st.error(f"Error building index: {e}")
    
    st.markdown("---")
    
    # Quick prompts
    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "What factors affect construction project delays?",
        "What are the payment terms?",
        "How do I handle change orders?",
        "What safety requirements must be followed?",
        "What are the quality standards?"
    ]
    
    for q in sample_questions:
        if st.button(q, key=f"sample_{q[:20]}", use_container_width=True):
            st.session_state.current_question = q
    
    st.markdown("---")
    st.markdown("### 📖 About")
    st.markdown("""
    This RAG system uses:
    - **FAISS** for vector search
    - **Sentence Transformers** for embeddings
    - **Groq/Ollama** for LLM responses
    """)

# Main content
st.markdown('<p class="main-header">🏗️ Construction Marketplace Assistant</p>', unsafe_allow_html=True)
st.markdown("Ask questions about construction policies, FAQs, and specifications")

# Chat interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Show contexts for assistant messages
        if msg["role"] == "assistant" and "contexts" in msg:
            with st.expander("📄 View Retrieved Context"):
                for i, ctx in enumerate(msg["contexts"], 1):
                    st.markdown(f"""
                    <div class="context-chunk">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span class="source-badge">📄 {ctx.get('source', 'Unknown')}</span>
                            <span class="source-badge">Score: {ctx.get('score', 0):.3f}</span>
                        </div>
                        <div style="font-size: 0.9rem;">{ctx.get('text', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

# Handle sample question from sidebar
if 'current_question' in st.session_state:
    question = st.session_state.current_question
    del st.session_state.current_question
    
    # Add to messages and process
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Retrieve contexts
                contexts = st.session_state.retriever.retrieve(question)
                
                # Generate answer
                answer = generate_answer(question, contexts, mode=mode)
                
                # Display answer
                st.markdown(answer)
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "contexts": contexts
                })
                
                # Show contexts
                with st.expander("📄 View Retrieved Context"):
                    for i, ctx in enumerate(contexts, 1):
                        st.markdown(f"""
                        <div class="context-chunk">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span class="source-badge">📄 {ctx.get('source', 'Unknown')}</span>
                                <span class="source-badge">Score: {ctx.get('score', 0):.3f}</span>
                            </div>
                            <div style="font-size: 0.9rem;">{ctx.get('text', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Retrieve contexts
                contexts = st.session_state.retriever.retrieve(prompt)
                
                # Generate answer
                answer = generate_answer(prompt, contexts, mode=mode)
                
                # Display answer
                st.markdown(answer)
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "contexts": contexts
                })
                
                # Show contexts
                with st.expander("📄 View Retrieved Context"):
                    for i, ctx in enumerate(contexts, 1):
                        st.markdown(f"""
                        <div class="context-chunk">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span class="source-badge">📄 {ctx.get('source', 'Unknown')}</span>
                                <span class="source-badge">Score: {ctx.get('score', 0):.3f}</span>
                            </div>
                            <div style="font-size: 0.9rem;">{ctx.get('text', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
