from flask import Flask
from endpoints import api_bp


app = Flask(__name__)


app.register_blueprint(api_bp)


@app.get("/")
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Template Desenvolvimto</title>
        <link rel="icon" type="image/svg+xml" href="/favicon.ico">
        <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;500;700&family=Playfair+Display:wght@500;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --ink: #121212;
                --cream: #f7f4ef;
                --clay: #d8c5a6;
                --sage: #5c6b5c;
                --sun: #f3b562;
                --line: rgba(18, 18, 18, 0.12);
            }
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: "Manrope", "Helvetica Neue", Arial, sans-serif;
                color: var(--ink);
                background: radial-gradient(1200px 800px at 10% 10%, #fff7e8 0%, #f8efe1 40%, #f4ede4 100%);
                min-height: 100vh;
                display: flex;
                align-items: stretch;
                justify-content: center;
            }
            .page {
                width: min(1100px, 100%);
                padding: 3.5rem 2.5rem 4rem;
                display: grid;
                gap: 2.5rem;
                position: relative;
            }
            .halo {
                position: absolute;
                inset: -120px 10% auto auto;
                width: 320px;
                height: 320px;
                background: radial-gradient(circle at 30% 30%, rgba(243, 181, 98, 0.8), rgba(243, 181, 98, 0));
                filter: blur(2px);
                z-index: 0;
                animation: float 8s ease-in-out infinite;
            }
            header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid var(--line);
                padding-bottom: 1.5rem;
                position: relative;
                z-index: 1;
            }
            .mark {
                font-family: "Playfair Display", "Times New Roman", serif;
                font-size: 1.25rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }
            .badge {
                border: 1px solid var(--line);
                padding: 0.4rem 0.9rem;
                border-radius: 999px;
                font-size: 0.8rem;
                background: rgba(255, 255, 255, 0.6);
            }
            main {
                display: grid;
                gap: 2rem;
                align-items: center;
                position: relative;
                z-index: 1;
            }
            .hero {
                display: grid;
                gap: 1rem;
                animation: fade-in 0.9s ease-out both;
            }
            h1 {
                font-family: "Playfair Display", "Times New Roman", serif;
                font-size: clamp(2.4rem, 4vw, 3.8rem);
                line-height: 1.05;
            }
            .byline {
                font-size: 1.05rem;
                color: var(--sage);
                letter-spacing: 0.02em;
            }
            .panel {
                border: 1px solid var(--line);
                background: rgba(255, 255, 255, 0.7);
                border-radius: 20px;
                padding: 1.5rem 1.75rem;
                display: grid;
                gap: 0.75rem;
                box-shadow: 0 24px 50px rgba(18, 18, 18, 0.08);
                animation: rise 0.9s ease-out 0.2s both;
            }
            .panel-title {
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.8rem;
                letter-spacing: 0.2em;
                color: var(--sage);
            }
            .panel-text {
                font-size: 1rem;
                max-width: 36ch;
            }
            .cta-row {
                display: flex;
                gap: 1rem;
                flex-wrap: wrap;
                align-items: center;
            }
            .cta {
                border: 1px solid var(--ink);
                padding: 0.7rem 1.2rem;
                border-radius: 999px;
                text-decoration: none;
                color: var(--ink);
                font-weight: 600;
                background: linear-gradient(120deg, #fff 0%, #f3e6d6 100%);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .cta:hover {
                transform: translateY(-2px);
                box-shadow: 0 16px 24px rgba(18, 18, 18, 0.12);
            }
            .stamp {
                display: inline-flex;
                align-items: center;
                gap: 0.6rem;
                font-size: 0.9rem;
                color: var(--sage);
            }
            .stamp::before {
                content: "";
                width: 36px;
                height: 1px;
                background: var(--sage);
                opacity: 0.4;
            }
            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(12px); }
            }
            @keyframes fade-in {
                from { opacity: 0; transform: translateY(16px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes rise {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @media (max-width: 768px) {
                .page { padding: 2.5rem 1.5rem 3rem; }
                header { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
                .panel { padding: 1.25rem; }
            }
        </style>
    </head>
    <body>
        <div class="page">
            <div class="halo"></div>
            <header>
                <div class="mark">Template</div>
                <div class="badge">responsive + elegante</div>
            </header>
            <main>
                <section class="hero">
                    <h1>template desenvolvimto</h1>
                    <p class="byline">by Diogo Caldas.</p>
                </section>
                <section class="panel">
                    <div class="panel-title">Presenca digital</div>
                    <p class="panel-text">Uma composicao minimalista com tipografia expressiva e detalhes suaves para valorizar seu conteudo.</p>
                    <div class="cta-row">
                        <a class="cta" href="/api/data">Explorar API</a>
                        <span class="stamp">Feito com cuidado</span>
                    </div>
                </section>
            </main>
        </div>
    </body>
    </html>
    """
