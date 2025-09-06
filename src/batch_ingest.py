import json, os, time, hashlib
from pathlib import Path
from .parse_pdf import pdf_to_text
from .config import OPENAI_MODEL_MAIN, OPENAI_API_KEY
from openai import OpenAI

def _chunks(text: str, min_len=200, max_len=2500):
    for ch in [c.strip() for c in (text or "").split("\n\n") if c.strip()]:
        if min_len <= len(ch) <= max_len:
            yield ch

def _as_chat_completion_jsonl(blocks):
    schema = { "type":"json_schema", "json_schema": { "name":"dish", "strict":True, "schema": {
        "type":"object","properties":{
          "name":{"type":"string"},"meal_type":{"type":"string"},
          "cuisine":{"type":"string"},"tags":{"type":"array","items":{"type":"string"}},
          "cook_minutes":{"type":"integer"},"difficulty":{"type":"integer"},
          "ingredients":{"type":"array","items":{"type":"object","properties":{"item":{"type":"string"},"qty":{"type":"number"},"unit":{"type":"string"}},"required":["item"],"additionalProperties":False}},
          "steps":{"type":"array","items":{"type":"string"}},"notes":{"type":"string"},"jain_ok":{"type":"boolean"},"substitutions":{"type":"array","items":{"type":"string"}}},
        "required":["name","meal_type","ingredients","steps"],"additionalProperties": False } } }
    for i, ch in enumerate(blocks):
        yield {
          "custom_id": f"cookbook_{i}",
          "method": "POST",
          "url": "/v1/chat/completions",
          "body": {
            "model": OPENAI_MODEL_MAIN,
            "messages": [
              {"role":"system","content":"You are Nigela, a vegetarian/Jain chef-assistant. Return ONLY JSON matching the schema; if non-Jain, suggest substitutions."},
              {"role":"user","content": ch}
            ],
            "response_format": schema,
            "temperature": 0.2
          }
        }

def _write_jsonl(path: str, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def make_jsonl(manifest: str, out_path: str):
    books = json.loads(Path(manifest).read_text())
    blocks=[]
    for b in books:
        p = b.get("path"); 
        if not p or not Path(p).exists(): continue
        txt = pdf_to_text(p)
        blocks.extend(list(_chunks(txt)))
    _write_jsonl(out_path, _as_chat_completion_jsonl(blocks))
    print(f"Wrote {out_path} with {len(blocks)} chunks")

def submit(jsonl_path: str):
    client = OpenAI(api_key=OPENAI_API_KEY)
    up = client.files.create(file=open(jsonl_path,"rb"), purpose="batch")
    batch = client.batches.create(input_file_id=up.id, endpoint="/v1/chat/completions", completion_window="24h")
    print(f"BATCH_ID={batch.id}")

def collect(batch_id: str):
    client = OpenAI(api_key=OPENAI_API_KEY)
    bat = client.batches.retrieve(batch_id)
    if not bat.output_file_id:
        print(f"Status: {bat.status}"); return
    content = client.files.content(bat.output_file_id).text
    # You can parse and map results into dishes.xlsx here if desired.
    Path("batch_output.jsonl").write_text(content)
    print("Saved batch_output.jsonl")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser("batch")
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("make-jsonl"); m.add_argument("--manifest", required=True); m.add_argument("--out", required=True)
    s = sub.add_parser("submit"); s.add_argument("--jsonl", required=True)
    c = sub.add_parser("collect"); c.add_argument("--batch-id", required=True)
    args = ap.parse_args()
    if args.cmd == "make-jsonl": make_jsonl(args.manifest, args.out)
    elif args.cmd == "submit": submit(args.jsonl)
    elif args.cmd == "collect": collect(args.batch_id)
