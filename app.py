from fastapi import FastAPI
import gradio as gr
import json

from inference import extract_actions_from_text

# -------------------------
# FASTAPI APP (FOR OPENENV)
# -------------------------
app = FastAPI()

@app.post("/openenv/reset")
def reset():
    return {"status": "ok"}

@app.get("/openenv/health")
def health():
    return {"status": "healthy"}

@app.post("/run")
def run_api(data: dict):
    transcript = data.get("transcript", "")
    actions = extract_actions_from_text(transcript)

    return {
        "items_found": len(actions),
        "actions": actions
    }

# -------------------------
# GRADIO UI
# -------------------------
def process_transcript(transcript):
    if not transcript.strip():
        return "Please paste a meeting transcript.", ""

    actions = extract_actions_from_text(transcript)

    if not actions:
        return "No action items found.", "[]"

    md = "| # | Action | Owner | Deadline |\n"
    md += "|---|--------|-------|----------|\n"

    for i, a in enumerate(actions, 1):
        md += f"| {i} | {a['description']} | {a['owner']} | {a.get('deadline') or '—'} |\n"

    return md, json.dumps(actions, indent=2)

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI Meeting Extractor")

    inp = gr.Textbox(label="Transcript", lines=6)
    btn = gr.Button("Extract")

    out1 = gr.Markdown()
    out2 = gr.Code(language="json")

    btn.click(process_transcript, inputs=inp, outputs=[out1, out2])

# 🔥 MOUNT GRADIO INTO FASTAPI
app = gr.mount_gradio_app(app, demo, path="/")