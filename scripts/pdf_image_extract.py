"""
PDF 图片提取脚本 - 自动去重版本
用法: python pdf_image_extract.py <PDF路径> <输出目录>
依赖: pip install pymupdf
"""
import sys
import fitz
import os
import hashlib

def extract_images(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    seen = set()

    for page_num in range(len(doc)):
        page = doc[page_num]
        for idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base = doc.extract_image(xref)
            img_bytes = base["image"]
            ext = base["ext"]
            h = hashlib.md5(img_bytes).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            fname = f"p{page_num+1:03d}_{idx+1:02d}.{ext}"
            with open(os.path.join(output_dir, fname), "wb") as f:
                f.write(img_bytes)
            print(f"Saved: {fname} ({len(img_bytes)} bytes)")

    print(f"\nDone. Total unique images: {len(seen)}")
    print(f"Output: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python pdf_image_extract.py <PDF路径> <输出目录>")
        sys.exit(1)
    extract_images(sys.argv[1], sys.argv[2])
