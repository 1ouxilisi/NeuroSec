"""
NeuroSec Web Demo
==================
AI安全检测Web界面，启动后浏览器访问 http://localhost:8000

Usage:
    pip install fastapi uvicorn
    python web/app.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from pentestai.modules.ai_security.prompt_injection_detector import PromptInjectionDetector
from pentestai.modules.ai_security.data_leakage_detector import DataLeakageDetector

app = FastAPI(title="NeuroSec AI Security Demo", version="48.2")
injector = PromptInjectionDetector()
leak_detector = DataLeakageDetector()

class DetectRequest(BaseModel):
    text: str

HTML_PAGE = """
<!DOCTYPE html>
<html><head><title>NeuroSec AI Security</title>
<style>
body{{font-family:system-ui;max-width:800px;margin:50px auto;padding:20px;background:#0d1117;color:#c9d1d9}}
h1{{color:#58a6ff}}
.box{{background:#161b22;padding:20px;border-radius:8px;margin:10px 0}}
input,textarea{{width:100%;padding:10px;background:#0d1117;border:1px solid #30363d;color:#c9d1d9;border-radius:6px;font-size:14px}}
button{{background:#238636;color:white;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;margin:5px}}
.result{{margin-top:15px;padding:15px;border-radius:6px}}
.safe{{background:#0d2818;border-left:4px solid #3fb950}}
.danger{{background:#2d0d0d;border-left:4px solid #f85149}}
.tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:12px;margin:2px}}
</style></head><body>
<h1>NeuroSec AI Security Scanner</h1>
<p>测试LLM输入安全性 - 提示词注入检测 + 数据泄露检测</p>
<div class="box">
<h3>输入文本</h3>
<textarea id="input" rows="4" placeholder="输入要检测的文本..."></textarea>
<br><br>
<button onclick="detect()">检测注入</button>
<button onclick="leak()">检测泄露</button>
</div>
<div id="result"></div>
<script>
async function detect(){{
  const text = document.getElementById('input').value;
  const r = await fetch('/api/detect',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{text}})}});
  const d = await r.json();
  const el = document.getElementById('result');
  el.innerHTML = '<div class="result '+(d.is_injection?'danger':'safe')+'">'+
    '<b>风险等级:</b> '+d.risk_level+'<br>'+
    '<b>置信度:</b> '+(d.confidence*100).toFixed(1)+'%<br>'+
    '<b>类型:</b> '+(d.injection_types||[]).join(', ')+
  '</div>';
}}
async function leak(){{
  const text = document.getElementById('input').value;
  const r = await fetch('/api/leak',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{text}})}});
  const d = await r.json();
  document.getElementById('result').innerHTML = '<div class="result '+(d.count>0?'danger':'safe')+'">'+
    '<b>发现泄露:</b> '+d.count+' 处<br>'+
    (d.findings||[]).map(f=>'<div class="tag">['+f.severity+'] '+f.type+'</div>').join('')+
  '</div>';
}}
</script></body></html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_PAGE

@app.post("/api/detect")
def detect(req: DetectRequest):
    result = injector.detect(req.text)
    return JSONResponse({
        "is_injection": result.is_injection,
        "risk_level": result.risk_level.value,
        "confidence": result.confidence,
        "injection_types": [t.value for t in result.injection_types],
        "matched_patterns": result.matched_patterns[:10]
    })

@app.post("/api/leak")
def leak(req: DetectRequest):
    findings = leak_detector.scan(req.text)
    return JSONResponse({
        "count": len(findings),
        "findings": [{"type": f.leakage_type.value, "severity": f.severity, "desc": f.description} for f in findings]
    })

if __name__ == "__main__":
    print("NeuroSec Web Demo starting at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
