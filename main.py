import os
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import arabic_reshaper
from bidi.algorithm import get_display

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def generate_chapter(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "أنت كاتب محترف وخبير. اكتب بأسلوب ممتع ومفصل باللغة العربية."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def build_pdf(title, chapters, filename="generated_book.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, spaceAfter=20, alignment=1)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=18, spaceAfter=12, alignment=2)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=12, leading=16, spaceAfter=10, alignment=2)

    story = []
    story.append(Paragraph(fix_arabic(title), title_style))
    story.append(Spacer(1, 20))

    for i, content in enumerate(chapters, 1):
        story.append(Paragraph(fix_arabic(f"الفصل {i}"), heading_style))
        for paragraph in content.split('\n\n'):
            if paragraph.strip():
                story.append(Paragraph(fix_arabic(paragraph), body_style))
        story.append(Spacer(1, 15))

    doc.build(story)
    print(f"تم إنشاء الكتاب بنجاح: {filename}")

if __name__ == "__main__":
    book_title = "دليل الذكاء الاصطناعي"
    topics = [
        "مقدمة عن الذكاء الاصطناعي",
        "كيف تعمل الشبكات العصبية",
        "مستقبل الذكاء الاصطناعي"
    ]
    
    chapters_content = []
    for topic in topics:
        print(f"جاري كتابة: {topic}...")
        text = generate_chapter(f"اكتب فصلاً كاملاً عن: {topic}")
        chapters_content.append(text)
        
    build_pdf(book_title, chapters_content)
