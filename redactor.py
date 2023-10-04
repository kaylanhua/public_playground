import fitz

doc = fitz.open("pink.pdf")

for page in doc:
    annotations = page.annots()
    for annot in annotations:
        if annot.type[0] == 8:
            rect = annot.rect
            redact_annot = page.add_redact_annot(rect).set_colors(stroke=(0,0,0), fill=(0,0,0))
            page.apply_redactions()


doc.save("real_redacted.pdf")
doc.close()

 