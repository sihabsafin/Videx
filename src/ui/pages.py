"""
Main page UI component
"""

import streamlit as st
from src.ui.theme import render_header, render_info_box
from src.orchestrator import ContentOrchestrator
from src.utils.session import reset_content_state, add_processed_url
from src.ui.export import render_export_section

def render_main_page():
    """Render main content area"""
    
    # Header
    render_header()
    
    # URL Input Section
    render_input_section()
    
    # Main Content Tabs (only show if content is processed)
    if st.session_state.current_content:
        render_content_tabs()

def render_input_section():
    """Render URL input and processing section"""
    
    st.markdown("### 🔗 Input Source")
    
    # Tab for single vs multiple URLs
    input_mode = st.radio(
        "Mode",
        ["Single URL", "Compare Multiple URLs"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if input_mode == "Single URL":
        render_single_url_input()
    else:
        render_multi_url_input()

def render_single_url_input():
    """Render single URL input"""
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        url = st.text_input(
            "Enter YouTube URL or Website URL",
            placeholder="https://youtube.com/watch?v=... or https://example.com/article",
            label_visibility="collapsed"
        )
    
    with col2:
        analyze_button = st.button("🔍 Analyze", use_container_width=True, type="primary")
    
    # Example URLs
    with st.expander("📝 Example URLs"):
        st.code("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.code("https://www.example.com/article")
    
    # Process URL
    if analyze_button and url:
        process_single_url(url)

def render_multi_url_input():
    """Render multiple URL input for comparison"""
    
    st.markdown("**Add URLs to compare (max 5)**")
    
    # URL input
    url = st.text_input(
        "Enter URL",
        placeholder="https://...",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("➕ Add URL", use_container_width=True):
            if url and url not in st.session_state.comparison_urls:
                if len(st.session_state.comparison_urls) < 5:
                    st.session_state.comparison_urls.append(url)
                    st.rerun()
                else:
                    st.error("Maximum 5 URLs allowed")
    
    with col2:
        if st.button("🔄 Clear All", use_container_width=True):
            st.session_state.comparison_urls = []
            st.session_state.comparison_result = None
            st.rerun()
    
    # Display added URLs
    if st.session_state.comparison_urls:
        st.markdown("**URLs to compare:**")
        for i, u in enumerate(st.session_state.comparison_urls, 1):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.text(f"{i}. {u[:60]}...")
            with col2:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.comparison_urls.remove(u)
                    st.rerun()
        
        # Compare button
        if st.button("🔍 Compare All", use_container_width=True, type="primary"):
            process_comparison()

def process_single_url(url: str):
    """Process a single URL"""
    
    # Reset state
    reset_content_state()
    
    # Show progress
    with st.spinner("🔄 Processing URL..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize orchestrator
        orchestrator = ContentOrchestrator(
            processing_mode=st.session_state.processing_mode
        )
        
        # Extract content
        status_text.text("📥 Extracting content...")
        progress_bar.progress(25)
        
        result = orchestrator.process_url(url)
        
        if not result['success']:
            st.error(f"❌ Error: {result['error']}")
            return
        
        progress_bar.progress(50)
        
        # Generate summary
        status_text.text("✨ Generating summary...")
        summary = orchestrator.generate_summary(
            content=result['content'],
            depth=st.session_state.summary_depth,
            style=st.session_state.summary_style,
            source_type=result['source_type']
        )
        
        progress_bar.progress(75)
        
        # Store in session
        st.session_state.current_content = result
        st.session_state.current_summary = summary
        add_processed_url(url)
        
        status_text.text("✅ Complete!")
        progress_bar.progress(100)
        
        st.success("✅ Content processed successfully!")
        st.rerun()

def process_comparison():
    """Process multiple URLs for comparison"""
    
    if len(st.session_state.comparison_urls) < 2:
        st.error("Add at least 2 URLs to compare")
        return
    
    with st.spinner("🔄 Processing and comparing URLs..."):
        orchestrator = ContentOrchestrator(
            processing_mode=st.session_state.processing_mode
        )
        
        comparison = orchestrator.compare_urls(st.session_state.comparison_urls)
        st.session_state.comparison_result = comparison
        
        st.success("✅ Comparison complete!")
        st.rerun()

def render_content_tabs():
    """Render main content tabs"""
    
    content = st.session_state.current_content
    
    # Display metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Source Type", content['source_type'].upper())
    with col2:
        st.metric("Tokens", f"{content['metadata']['token_count']:,}")
    with col3:
        if content['source_type'] == 'youtube':
            st.metric("Sections", len(content['metadata'].get('sections', [])))
        else:
            st.metric("Status", "✓ Ready")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Summary",
        "💡 Insights", 
        "❓ Questions",
        "🔄 Transform",
        "📤 Export"
    ])
    
    with tab1:
        render_summary_tab()
    
    with tab2:
        render_insights_tab()
    
    with tab3:
        render_questions_tab()
    
    with tab4:
        render_transform_tab()
    
    with tab5:
        render_export_section()
    
    # Comparison results (if any)
    if st.session_state.comparison_result:
        st.markdown("---")
        st.markdown("### 🔄 Comparison Results")
        st.markdown(st.session_state.comparison_result)

def render_summary_tab():
    """Render summary tab"""
    
    if st.session_state.current_summary:
        st.markdown("### 📝 Summary")
        st.markdown(st.session_state.current_summary)
        
        # Show original content in expander
        with st.expander("📄 View Original Content"):
            content = st.session_state.current_content['content']
            st.text_area(
                "Original",
                content,
                height=300,
                label_visibility="collapsed"
            )
    
    # Regenerate option
    if st.button("🔄 Regenerate Summary"):
        with st.spinner("Regenerating..."):
            orchestrator = ContentOrchestrator(
                processing_mode=st.session_state.processing_mode
            )
            summary = orchestrator.generate_summary(
                content=st.session_state.current_content['content'],
                depth=st.session_state.summary_depth,
                style=st.session_state.summary_style,
                source_type=st.session_state.current_content['source_type']
            )
            st.session_state.current_summary = summary
            st.rerun()

def render_insights_tab():
    """Render insights tab"""
    
    if not st.session_state.current_insights:
        if st.button("🔍 Generate Insights", type="primary"):
            with st.spinner("Extracting insights..."):
                orchestrator = ContentOrchestrator(
                    processing_mode=st.session_state.processing_mode
                )
                insights = orchestrator.generate_insights(
                    st.session_state.current_content['content']
                )
                st.session_state.current_insights = insights
                st.rerun()
    else:
        st.markdown("### 💡 Key Insights")
        st.markdown(st.session_state.current_insights)
        
        if st.button("🔄 Regenerate"):
            st.session_state.current_insights = None
            st.rerun()

def render_questions_tab():
    """Render questions tab"""
    
    question_type = st.selectbox(
        "Question Type",
        ["study", "discussion", "interview", "mcq"]
    )
    
    if not st.session_state.current_questions or st.button("🔍 Generate Questions", type="primary"):
        with st.spinner("Generating questions..."):
            orchestrator = ContentOrchestrator(
                processing_mode=st.session_state.processing_mode
            )
            questions = orchestrator.generate_questions(
                st.session_state.current_content['content'],
                question_type
            )
            st.session_state.current_questions = questions
            st.rerun()
    
    if st.session_state.current_questions:
        st.markdown("### ❓ Generated Questions")
        st.markdown(st.session_state.current_questions)

def render_transform_tab():
    """Render transformation tab"""
    
    transform_type = st.selectbox(
        "Transform to",
        ["blog", "linkedin", "email", "meeting_notes", "notion"]
    )
    
    if st.button("🔄 Transform", type="primary"):
        with st.spinner("Transforming content..."):
            orchestrator = ContentOrchestrator(
                processing_mode=st.session_state.processing_mode
            )
            transformed = orchestrator.transform_content(
                st.session_state.current_content['content'],
                transform_type
            )
            st.session_state.current_transformation = transformed
            st.rerun()
    
    if st.session_state.current_transformation:
        st.markdown("### 🔄 Transformed Content")
        st.markdown(st.session_state.current_transformation)
