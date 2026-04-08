import gradio as gr
import json
from inference import extract_actions  # reuse your existing function

def process_transcript(transcript):
    if not transcript.strip():
        return "Please paste a meeting transcript above.", ""
    
    try:
        result = extract_actions(transcript)
        actions = result if isinstance(result, list) else result.get("tasks", [])
        
        # Build readable markdown table
        if not actions:
            return "No action items found.", json.dumps([], indent=2)
        
        md = "| # | Action | Owner | Deadline | Status |\n"
        md += "|---|--------|-------|----------|--------|\n"
        for i, a in enumerate(actions, 1):
            deadline = a.get("deadline") or "—"
            owner = a.get("owner") or "—"
            md += f"| {i} | {a['description']} | {owner} | {deadline} | {a.get('status','pending')} |\n"
        
        return md, json.dumps(actions, indent=2)
    except Exception as e:
        return f"Error: {str(e)}", ""

EXAMPLES = [
    ["Alice: Bob, please prepare the Q1 budget by March 15th. Design team, get wireframes done by end of week."],
    ["We need to optimize API endpoints before sprint ends March 14. John follow up customer feedback EOW."],
    ["The login issue needs to be resolved by whoever is on engineering. Marketing knows about the launch deck situation."]
]

with gr.Blocks(title="Meeting Transcript Extractor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Meeting Transcript Action Extractor
    **Meta x Hugging Face Hackathon** — AI-powered action item detection from meeting transcripts.
    Paste any meeting transcript and get structured action items with owners and deadlines.
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            transcript_input = gr.Textbox(
                label="Meeting Transcript",
                placeholder="Paste your meeting transcript here...",
                lines=8
            )
            gr.Examples(examples=EXAMPLES, inputs=transcript_input)
            submit_btn = gr.Button("Extract Action Items", variant="primary")
        
        with gr.Column(scale=3):
            table_output = gr.Markdown(label="Extracted Actions")
            json_output = gr.Code(label="Raw JSON", language="json", visible=False)
            show_json = gr.Checkbox(label="Show raw JSON")
    
    show_json.change(lambda x: gr.update(visible=x), inputs=show_json, outputs=json_output)
    submit_btn.click(process_transcript, inputs=transcript_input, outputs=[table_output, json_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)