from __future__ import annotations

import argparse
import re
from pathlib import Path


SCENE_FILES = {
    1: "s00_roadmap.txt",
    2: "s01_forward_ou_wiener.txt",
    3: "s02_markov.txt",
    4: "s03_reverse_chain.txt",
    5: "s04_score_compass.txt",
    6: "s05_local_linear.txt",
    7: "s06_mse_conditional_mean.txt",
    8: "s07_training_loop.txt",
    9: "s08_sde_drift_diffusion.txt",
    10: "s09_probability_flow_ode.txt",
    11: "s10_fokker_planck_score.txt",
    12: "s11_reverse_distribution.txt",
    13: "s12_runge_kutta_solver.txt",
    14: "s13_finale_failure.txt",
}

EQUATION_SPEECH = {
    r"X_t = \alpha_t X_{t-1} + \sqrt{\beta_t}G.": (
        "X t equals alpha t times X t minus one,\n\n"
        "plus square root beta t times G."
    ),
    r"X_t = \bar{\alpha}_t X_0 + \sqrt{\bar{\beta}_t}G.": (
        "X t equals alpha bar t times X zero,\n\n"
        "plus square root beta bar t times G."
    ),
    r"""p(x_t \mid x_0, x_1, \ldots, x_{t-1})
=====================================

p(x_t \mid x_{t-1}).""": (
        "p of x t, given x zero through x t minus one,\n\n"
        "equals p of x t, given x t minus one."
    ),
    r"""p(x_{0:T})
==========

p(x_0)
\prod_{t=1}^{T}
p(x_t \mid x_{t-1}).""": (
        "p of x zero to T,\n\n"
        "equals p of x zero,\n\n"
        "times the product from t equals one to T,\n\n"
        "of p of x t given x t minus one."
    ),
    r"q(x_{t-1}\mid x_t)": "q of x t minus one, given x t.",
    r"""q(x_{0:T})
==========

q(x_T)
\prod_{t=1}^{T}
q(x_{t-1}\mid x_t).""": (
        "q of x zero to T,\n\n"
        "equals q of x T,\n\n"
        "times the product from t equals one to T,\n\n"
        "of q of x t minus one, given x t."
    ),
    r"\nabla \log p_X(y)": "nabla log p X of y.",
    r"""\mu(X\mid y)
\approx
y + \beta \nabla \log p_X(y).""": (
        "mu of X given y,\n\n"
        "is approximately y plus beta times nabla log p X of y."
    ),
    r"\mathbb{E}[X\mid Y=y].": "the expected value of X, given Y equals y.",
    r"""L(f_\theta)
===========

\mathbb{E}
\left[
|f_\theta(y)-x|^2
\right].""": (
        "L of f theta,\n\n"
        "equals the expected squared distance between f theta of y and x."
    ),
    r"f^*(y)=\mathbb{E}[X\mid Y=y].": (
        "f star of y equals the expected value of X, given Y equals y."
    ),
    r"\mu_\theta(y,t).": "mu theta of y and t.",
    r"\mu_\theta(y,t),": "mu theta of y and t,",
    r"dW.": "d W.",
    r"dX = \sqrt{\beta(t)},dW.": "d X equals square root beta of t, times d W.",
    r"dX = \alpha(x,t),dt.": "d X equals alpha of x and t, times d t.",
    r"dX = \alpha(x,t),dt + \sqrt{\beta(t)},dW.": (
        "d X equals alpha of x and t times d t,\n\n"
        "plus square root beta of t times d W."
    ),
    r"""\frac{\partial p}{\partial t}
=============================

-\operatorname{div}(pv).""": (
        "partial p over partial t,\n\n"
        "equals negative divergence of p times v."
    ),
    r"""v(x,t)
======

## \alpha(x,t)

\frac{\beta(t)}{2}
\nabla \log p(x,t).""": (
        "v of x and t,\n\n"
        "equals alpha of x and t,\n\n"
        "minus beta of t over two,\n\n"
        "times nabla log p of x and t."
    ),
    r"\nabla \log p(x,t).": "nabla log p of x and t.",
    r"y_{n+1}=y_n+h f(t_n,y_n).": (
        "y n plus one equals y n,\n\n"
        "plus h times f of t n and y n."
    ),
    r"""y_{n+1}
=======

y_n+
\frac{h}{6}
(k_1+2k_2+2k_3+k_4).""": (
        "y n plus one,\n\n"
        "equals y n plus h over six,\n\n"
        "times k one plus two k two plus two k three plus k four."
    ),
}

INLINE_REPLACEMENTS = [
    ("(X_t)", "X t"),
    ("(t)", "t"),
    ("(X_{t-1})", "X t minus one"),
    ("(X_{t-2})", "X t minus two"),
    ("(X_0)", "X zero"),
    ("(x_{t-1})", "x t minus one"),
    ("(x_t)", "x t"),
    ("(x_T)", "x T"),
    ("(x_0)", "x zero"),
    ("(x_{0:T})", "x zero to T"),
    ("(q(x_{t-1}))", "q of x t minus one"),
    ("(q(x_1))", "q of x one"),
    ("(q(x_2))", "q of x two"),
    ("(y)", "y"),
    ("(x)", "x"),
    (r"(\beta)", "beta"),
    (r"(\alpha_t)", "alpha t"),
    (r"(\alpha_t X_{t-1})", "alpha t times X t minus one"),
    (r"(\sqrt{\beta_t}G)", "square root beta t times G"),
    ("(G)", "G"),
    (r"(\beta_t)", "beta t"),
    (r"(\sqrt{\beta_t})", "square root beta t"),
    (r"(\bar{\alpha}_t)", "alpha bar t"),
    (r"(\mu(X\mid y))", "mu of X given y"),
    (r"(\nabla \log p_X(y))", "nabla log p X of y"),
    (r"\nabla \log p_X(y)", "nabla log p X of y"),
    (r"(f_\theta(y))", "f theta of y"),
    (r"(f^*(y)=\mathbb{E}[X\mid Y=y])", "f star of y equals E of X given Y equals y"),
    (r"(\mu_\theta(y,t))", "mu theta of y and t"),
    ("(y=x_t)", "y equals x t"),
    ("(Delta t -> 0)", "delta t goes to zero"),
    (r"(\Delta t -> 0)", "delta t goes to zero"),
    ("(dW)", "d W"),
    ("(v)", "v"),
    ("(k_1)", "k one"),
    ("(k_2)", "k two"),
    ("(k_3)", "k three"),
    ("(k_4)", "k four"),
]

PUNCTUATION_REPLACEMENTS = {
    "\u2014": " - ",
    "\u2013": "-",
    "\u201c": '"',
    "\u201d": '"',
    "\u2018": "'",
    "\u2019": "'",
    "\u2026": "...",
    "It\u00f4": "Ito",
    "Fokker\u2013Planck": "Fokker-Planck",
    "Runge\u2013Kutta": "Runge-Kutta",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split tts/scripts/voice.txt into per-scene TTS files.")
    parser.add_argument("--source", type=Path, default=Path("tts/scripts/voice.txt"))
    parser.add_argument("--output-dir", type=Path, default=Path("tts/scripts"))
    parser.add_argument("--overwrite-s00", action="store_true", help="Overwrite the hand-tuned s00_roadmap.txt too.")
    return parser.parse_args()


def normalize_punctuation(text: str) -> str:
    for old, new in PUNCTUATION_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def equation_to_speech(match: re.Match[str]) -> str:
    body = match.group(1).strip()
    return "\n\n" + EQUATION_SPEECH.get(body, body.replace("\\", "")) + "\n\n"


def replace_equations(text: str) -> str:
    return re.sub(r"\[\n(.*?)\n\]", equation_to_speech, text, flags=re.S)


def replace_inline_math(text: str) -> str:
    for literal, replacement in INLINE_REPLACEMENTS:
        text = text.replace(literal, replacement)
    text = re.sub(r"\(([^()\n]{1,40})\)", r"\1", text)
    text = text.replace(r"\nabla \log p_Xy", "nabla log p X of y")
    return text


def split_sentences(paragraph: str) -> list[str]:
    paragraph = paragraph.strip()
    if not paragraph:
        return []
    pieces = re.split(r"(?<=[.!?])\s+", paragraph)
    return [piece.strip() for piece in pieces if piece.strip()]


def rhythmize_sentence(sentence: str) -> list[str]:
    sentence = sentence.strip()
    if not sentence:
        return []

    replacements = [
        ("But now, let us", "But now...\n\nlet us"),
        ("Can we start from pure noise, and step by step,", "Can we start from pure noise...\n\nand step by step..."),
        ("Instead, can we learn a path from random noise toward", "Instead, can we learn a path from random noise...\n\ntoward"),
        ("Then, using probability, neural networks, and a surprising amount of beautiful mathematics,", "Then, using probability, neural networks, and a surprising amount of beautiful mathematics..."),
        ("This is the key shift:", "This is the key shift:"),
        ("The score.", "The score."),
        ("And there it is again.", "And there it is again."),
        ("How do we learn it?", "How do we learn it?"),
    ]
    for old, new in replacements:
        sentence = sentence.replace(old, new)

    if "\n\n" in sentence:
        return [part.strip() for part in sentence.split("\n\n") if part.strip()]

    if len(sentence) <= 115:
        return [sentence]

    comma_parts = re.split(r"(?<=,)\s+", sentence)
    if len(comma_parts) > 1:
        chunks: list[str] = []
        current = ""
        for part in comma_parts:
            candidate = f"{current} {part}".strip()
            if current and len(candidate) > 115:
                chunks.append(current)
                current = part
            else:
                current = candidate
        if current:
            chunks.append(current)
        return chunks

    return [sentence]


def clean_scene_body(body: str) -> str:
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        if stripped.startswith("### Target time:"):
            continue
        if stripped == "---":
            continue
        lines.append(stripped)

    text = "\n".join(lines)
    text = replace_equations(text)
    text = replace_inline_math(text)
    text = normalize_punctuation(text)

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    output: list[str] = []
    for paragraph in paragraphs:
        for sentence in split_sentences(paragraph):
            output.extend(rhythmize_sentence(sentence))

    text = "\n\n".join(output)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +", " ", text)
    return text.strip() + "\n"


def extract_scene_blocks(text: str) -> dict[int, str]:
    pattern = re.compile(r"^## Scene (\d+) .*$", flags=re.M)
    matches = list(pattern.finditer(text))
    blocks: dict[int, str] = {}
    for index, match in enumerate(matches):
        scene_number = int(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks[scene_number] = text[start:end]
    return blocks


def main() -> int:
    args = parse_args()
    text = args.source.read_text(encoding="utf-8")
    blocks = extract_scene_blocks(text)
    if len(blocks) != 14:
        raise RuntimeError(f"Expected 14 scenes, found {len(blocks)}.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for scene_number in range(1, 15):
        out_path = args.output_dir / SCENE_FILES[scene_number]
        if scene_number == 1 and out_path.exists() and not args.overwrite_s00:
            print(f"keep tuned file: {out_path}")
            continue
        out_path.write_text(clean_scene_body(blocks[scene_number]), encoding="utf-8", newline="\n")
        print(f"wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
