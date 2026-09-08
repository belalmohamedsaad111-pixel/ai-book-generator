const fs = require('fs');
const PDFDocument = require('pdfkit');
const axios = require('axios');

const apiKey = process.env.GEMINI_API_KEY;

async function generateChapter(prompt) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
  const response = await axios.post(url, {
    contents: [{ parts: [{ text: prompt }] }]
  });
  return response.data.candidates[0].content.parts[0].text;
}

async function buildPDF() {
  const doc = new PDFDocument();
  doc.pipe(fs.createWriteStream('generated_book.pdf'));

  const topics = ["مقدمة عن الذكاء الاصطناعي", "مستقبل الذكاء الاصطناعي"];

  for (const topic of topics) {
    console.log(`Writing: ${topic}`);
    const content = await generateChapter(`اكتب فصلاً قصيراً عن ${topic}`);
    doc.fontSize(16).text(topic, { align: 'right' });
    doc.moveDown();
    doc.fontSize(12).text(content, { align: 'right' });
    doc.addPage();
  }

  doc.end();
  console.log("PDF created successfully!");
}

buildPDF().catch(err => {
  console.error(err);
  process.exit(1);
});
