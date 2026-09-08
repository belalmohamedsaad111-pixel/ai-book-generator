import os
import json
import urllib.request
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import arabic_reshaper
from bidi.algorithm import get_display

api_key = os.environ.get("GEMINI_API_KEY", "").strip()

def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def generate_chapter(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['candidates'][0]['content']['parts'][0]['text']

def build_pdf():
    pdf_filename = "generated_book.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    arabic_style = ParagraphStyle(
        'ArabicStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        alignment=2
    )

    topics = ["مقدمة عن الذكاء الاصطناعي", "تاريخ الذكاء الاصطناعي"]
    
    for topic in topics:
        print(f"...جاري كتابة: {topic}")
        raw_text = generate_chapter(f"اكتب ملخصاً قصيراً عن {topic}")
        reshaped = reshape_text(raw_text)
        story.append(Paragraph(reshaped, arabic_style))
        story.append(Spacer(1, 12))

    doc.build(story)
    print("تم إنشاء الكتاب بنجاح!")

if __name__ == "__main__":
    build_pdf()
