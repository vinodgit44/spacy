from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from .processor import analyze

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SpaCy NLP Analyzer is running!"}

@app.post("/analyze")
def analyze_api(text: str):
    return analyze(text)

@app.get("/ui", response_class=HTMLResponse)
def ui_page():
    html = """
    <html>
    <head>
        <title>SpaCy NLP Analyzer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

        <style>
            body {
                background: linear-gradient(to right, #eef2f3, #8e9eab);
                min-height: 100vh;
            }
            .header {
                background: #0d6efd;
                color: white;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 25px;
            }
            .card {
                border-radius: 15px !important;
            }
        </style>
    </head>

    <body>
        <div class="container py-5">

            <div class="header shadow">
                <h1 class="fw-bold">SpaCy NLP Analyzer</h1>
                <p class="mb-0">Tokenization • POS • NER • Dependencies • Lemmatization • Stopwords</p>
            </div>

            <div class="card p-4 shadow">
                <h4 class="text-center mb-4">Enter Your Text</h4>

                <form method="post" action="/ui_analyze">
                    <textarea name="text" class="form-control" rows="5"
                        placeholder="Type text here... (e.g., Elon Musk founded SpaceX in California)"
                        required></textarea>

                    <br>
                    <button class="btn btn-primary w-100 py-2">Analyze Text</button>
                </form>
            </div>

        </div>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.post("/ui_analyze", response_class=HTMLResponse)
def ui_analyze(text: str = Form(...)):
    result = analyze(text)

    def list_block(title, items):
        return f"""
            <div class="mt-4">
                <h5 class="fw-bold">{title}</h5>
                <div class="p-3 bg-light border rounded">{items}</div>
            </div>
        """

    html = f"""
    <html>
    <head>
        <title>NLP Result</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background: #f0f2f5;
            }}
            .entity-badge {{
                display: inline-block;
                padding: 4px 8px;
                margin: 3px;
                border-radius: 5px;
                background: #d1ecf1;
                color: #055160;
                font-size: 0.9rem;
            }}
        </style>
    </head>

    <body>
        <div class="container py-5">

            <div class="card p-4 shadow-lg">

                <h2 class="fw-bold">Analysis Result</h2>
                <p class="text-muted">Text you provided:</p>
                <div class="alert alert-secondary">{text}</div>

                <hr>

                {list_block("Tokens", result["tokens"])}
                {list_block("POS Tags", result["pos_tags"])}

                <div class="mt-4">
                    <h5 class="fw-bold">Named Entities (NER)</h5>
                    <div class="p-3 bg-light border rounded">
                        {''.join([f"<span class='entity-badge'>{ent[0]} → {ent[1]}</span>" for ent in result['ner']])}
                    </div>
                </div>

                {list_block("Dependency Parsing", result["dependencies"])}
                {list_block("Lemmas", result["lemmas"])}
                {list_block("Without Stopwords", result["without_stopwords"])}

                <br>
                <a href="/ui" class="btn btn-primary mt-3">Analyze Another Sentence</a>

            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html)
