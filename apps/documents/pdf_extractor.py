"""
JanSetu PDF Layout & Text Extractor
Uses PyMuPDF (fitz) to extract text, calculate font metrics, detect small font,
and identify layout positions (footnotes, middle pages, final pages).
"""

import fitz  # PyMuPDF
import re
from collections import Counter

class PDFExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = fitz.open(file_path)
        self.total_pages = len(self.doc)
        self.body_font_size = self._calculate_body_font_size()

    def _calculate_body_font_size(self):
        """Calculates the document's standard body font size (most common font size for paragraphs)."""
        font_sizes = []
        for page_idx in range(min(5, self.total_pages)):
            page = self.doc[page_idx]
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:  # text block
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            text = span.get("text", "").strip()
                            if len(text) > 15:
                                font_sizes.append(round(span.get("size", 10.0), 1))
        
        if not font_sizes:
            return 10.0
        
        # Most frequent font size among substantive sentences
        counts = Counter(font_sizes)
        body_size = counts.most_common(1)[0][0]
        return body_size

    def extract_full_text_by_pages(self):
        """Extracts plain text per page."""
        pages_text = []
        for idx in range(self.total_pages):
            page = self.doc[idx]
            pages_text.append({
                "page_number": idx + 1,
                "text": page.get_text("text").strip()
            })
        return pages_text

    def extract_layout_elements(self):
        """
        Extracts structured paragraphs with font size, small font flag,
        position category, page number, and nearest section heading.
        """
        elements = []
        current_heading = "General"

        for page_idx in range(self.total_pages):
            page_num = page_idx + 1
            page = self.doc[page_idx]
            page_height = page.rect.height
            text_dict = page.get_text("dict")

            # Determine page position category
            if self.total_pages <= 2:
                page_pos = "final_pages" if page_num == self.total_pages else "middle"
            else:
                if page_num >= int(self.total_pages * 0.75):
                    page_pos = "final_pages"
                elif page_num == 1:
                    page_pos = "top"
                else:
                    page_pos = "middle"

            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:  # text block
                    block_bbox = block.get("bbox", [0, 0, 0, 0])
                    block_y1 = block_bbox[3]
                    is_footnote_pos = block_y1 > (page_height * 0.88)

                    block_text_pieces = []
                    span_sizes = []

                    for line in block.get("lines", []):
                        line_text = ""
                        for span in line.get("spans", []):
                            span_text = span.get("text", "")
                            line_text += span_text
                            if span_text.strip():
                                span_sizes.append(round(span.get("size", 10.0), 1))
                        block_text_pieces.append(line_text)

                    full_block_text = " ".join([p.strip() for p in block_text_pieces if p.strip()])
                    if not full_block_text or len(full_block_text) < 10:
                        continue

                    avg_span_size = (sum(span_sizes) / len(span_sizes)) if span_sizes else self.body_font_size
                    is_small = avg_span_size < (self.body_font_size * 0.82)

                    # Check if this block looks like a section heading
                    if (avg_span_size > self.body_font_size * 1.1 or re.match(r'^(Section|Article|Clause|\d+\.|\b[A-Z\s]{4,}\b)', full_block_text)) and len(full_block_text) < 90:
                        current_heading = full_block_text.strip()
                        continue

                    # Position tag
                    if is_footnote_pos:
                        pos = "footnote"
                    elif page_pos == "final_pages":
                        pos = "final_pages"
                    elif page_pos == "middle":
                        pos = "middle"
                    else:
                        pos = "top"

                    elements.append({
                        "page_number": page_num,
                        "text": full_block_text,
                        "font_size": avg_span_size,
                        "body_font_size": self.body_font_size,
                        "is_small_font": is_small,
                        "document_position": pos,
                        "section_heading": current_heading,
                    })

        return elements

    def close(self):
        self.doc.close()
