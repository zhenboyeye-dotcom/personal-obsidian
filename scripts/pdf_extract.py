#!/usr/bin/env python3
"""
pdf_extract.py - Datasheet PDF 轻量切片工具
用法: python pdf_extract.py --pdf <文件路径> --search <关键词> [--pages <范围>]
示例: python pdf_extract.py --pdf USART.pdf --search "USART" --pages 1-30
"""

import sys
import argparse
import os

# 尝试导入 PDF 库
try:
    import fitz  # PyMuPDF
    PDF_LIB = "pymupdf"
except ImportError:
    try:
        from pypdf import PdfReader
        PDF_LIB = "pypdf"
    except ImportError:
        print("Error: 需要安装 PyMuPDF 或 pypdf")
        print("pip install pymupdf  # 推荐")
        sys.exit(1)


def extract_pdf(pdf_path, keywords=None, pages=None):
    """提取 PDF 内容"""
    if PDF_LIB == "pymupdf":
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        # 解析页码范围
        if pages:
            if '-' in pages:
                start, end = pages.split('-')
                start_page = max(1, int(start))
                end_page = min(int(end), total_pages)
            else:
                start_page = 1
                end_page = min(int(pages), total_pages)
        else:
            start_page = 1
            end_page = total_pages

        print(f"[INFO] PDF: {pdf_path}")
        print(f"[INFO] Pages: {start_page}-{end_page} / {total_pages}")
        print(f"[INFO] Keywords: {keywords or '全部'}")
        print("=" * 60)

        for page_num in range(start_page, end_page + 1):
            page = doc[page_num - 1]
            text = page.get_text()

            if keywords:
                # 关键词过滤（不区分大小写）
                lower_text = text.lower()
                if not any(kw.lower() in lower_text for kw in keywords):
                    continue

            print(f"\n--- 第 {page_num} 页 ---")
            print(text[:3000])  # 限制每页输出

            if len(text) > 3000:
                print(f"[... 截断，完整内容 {len(text)} 字符]")

        doc.close()

    else:
        # pypdf fallback
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"[INFO] PDF: {pdf_path}, 共 {total_pages} 页")
        print("[INFO] pypdf 模式: 全文输出（无关键词过滤）")
        print("=" * 60)

        for i, page in enumerate(reader.pages[:min(pages or 10, total_pages)]):
            text = page.extract_text()
            print(f"\n--- 第 {i+1} 页 ---")
            print(text[:3000])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Datasheet PDF 切片工具")
    parser.add_argument("--pdf", required=True, help="PDF 文件路径")
    parser.add_argument("--search", nargs='+', help="关键词列表（可选）")
    parser.add_argument("--pages", help="页码范围，如 1-30")

    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"Error: 文件不存在: {args.pdf}")
        sys.exit(1)

    extract_pdf(args.pdf, keywords=args.search, pages=args.pages)
