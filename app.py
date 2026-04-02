from flask import Flask, render_template, request, jsonify, stream_with_context, Response
from openai import OpenAI
import json
import os

app = Flask(__name__)

# ── OpenAI client (replace with your actual key) ──────────────────────────
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def refine_prompt(raw_prompt, student_class, student_subject):
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are an expert at converting vague student questions into detailed, "
                    f"specific prompts for an AI tutor. "
                    f"The student is in Class {student_class} studying {student_subject}. "
                    f"Take their raw question and rewrite it as a clear, detailed prompt "
                    f"that will get the best educational answer. "
                    f"Return ONLY the refined prompt, nothing else."
                )
            },
            {"role": "user", "content": raw_prompt}
        ]
    )
    return response.choices[0].message.content


def generate_answer(refined_prompt, student_class, student_subject):
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a Class {student_class} {student_subject} textbook. "
                    f"Answer the question strictly based on the standard curriculum of NCERT. "
                    f"Be accurate, complete, and educational. "
                    f"Do not go beyond what a textbook would cover."
                )
            },
            {"role": "user", "content": refined_prompt}
        ]
    )
    return response.choices[0].message.content


def make_it_fun(answer, student_class, student_subject):
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are the user's older brother or best friend who is very good at studies. "
                    f"You're explaining a Class {student_class} {student_subject} concept to your younger sibling or bestie. "
                    f"Your tone is: casual, warm, slightly teasing but never mean, encouraging, and very desi. "
                    f"Speak in Hinglish (Hindi + English mixed, Roman script only, no Devanagari). "
                    f"Use phrases like: 'sun yaar', 'ek kaam kar', 'dekh bhai', 'simple si baat hai', "
                    f"'tu ghabra mat', 'chal main samjhata hun', 'teri life mein ek baar kaam aayega ye'. "
                    f"Use funny relatable desi examples — like comparing concepts to cricket, chai, "
                    f"Bollywood, school life, mom's anger, or street food. "
                    f"End with a small encouragement like a big brother would — short, genuine, not cringe. "
                    f"Never sound like a textbook. Never sound like a teacher. Sound like family."
                )
            },
            {"role": "user", "content": answer}
        ]
    )
    return response.choices[0].message.content


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    student_class = data.get("student_class", "").strip()
    student_subject = data.get("student_subject", "").strip()
    raw_prompt = data.get("doubt", "").strip()

    if not all([student_class, student_subject, raw_prompt]):
        return jsonify({"error": "Please fill all fields."}), 400

    def generate():
        try:
            # Step 1: Refine
            yield f"data: {json.dumps({'step': 1, 'status': 'Refining your question...'})}\n\n"
            refined = refine_prompt(raw_prompt, student_class, student_subject)
            yield f"data: {json.dumps({'step': 1, 'done': True, 'refined': refined})}\n\n"

            # Step 2: Answer
            yield f"data: {json.dumps({'step': 2, 'status': 'Fetching NCERT knowledge...'})}\n\n"
            answer = generate_answer(refined, student_class, student_subject)
            yield f"data: {json.dumps({'step': 2, 'done': True})}\n\n"

            # Step 3: Fun
            yield f"data: {json.dumps({'step': 3, 'status': 'Your bhai is cooking the explanation...'})}\n\n"
            fun_answer = make_it_fun(answer, student_class, student_subject)
            yield f"data: {json.dumps({'step': 3, 'done': True, 'final': fun_answer})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
