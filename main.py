import os
from google import genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import arabic_reshaper
from bidi.algorithm import get_display

api_key = os.environ.get("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=api_key)

def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def generate_chapter(prompt):
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents=prompt,
    )
    return response.text

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

    topics = ["مقدمة عن الذكاء الاصطناعي", "تاريخ الذكاء الاصطناعي", "مستقبل الذكاء الاصطناعي"]
    
    for topic in topics:
        print(f"...جاري كتابة: {topic}")
        raw_text = generate_chapter(f"اكتب فصلاً كاملاً عن {topic}")
        reshaped = reshape_text(raw_text)
        story.append(Paragraph(reshaped, arabic_style))
        story.append(Spacer(1, 12))

    doc.build(story)
    print("تم إنشاء الكتاب بنجاح!")

if __name__ == "__main__":
    build_pdf()
