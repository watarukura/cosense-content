from sys import argv
import re


# https://github.com/matsushinDB11/Scrapbox_to_md/blob/master/Scrapbox_to_Notion.py
# 1ページ分リストで渡す
# Scrapboxページの記法をMarakdown形式に変換し、1ページ分を配列で返す。
def scrapbox_to_md(sbfile):
    with open(file=sbfile, mode="r", encoding="utf-8") as f:
        text_array = f.readlines()

    # 箇条書き
    indent_re = re.compile(r"^([ \t\u3000]+)(\S.*)$")
    ordered_list_re = re.compile(r"^\d+\.\s+")
    unordered_list_re = re.compile(r"^[-*+]\s+")
    # 見出し
    heading_re = re.compile(r"^\[(\*{1,6})\s*(.+?)\]$")
    # 太字
    bold_re = re.compile(r"\[\*(.+?)\]")
    # 消し線
    strike_re = re.compile(r"\[-\s*(.+?)\]")
    # ソースコード
    code_re = re.compile(r"^code:\s*(\S+)?")
    # URLのみハイパーリンク
    url_re = re.compile(r"https?://[^\s\]]+")
    # テキストのハイパーリンク
    text_hyperlink_re = re.compile(r"\[([^\]]+?)\s+(https?://[^\s\]]+)\]")
    # URL + タイトル
    url_title_re = re.compile(r"\[(https?://[^\s\]]+)\s+([^\]]+)\]")
    # URLのみの[]
    bracket_url_re = re.compile(r"\[(https?://[^\s\]]+)\](?!\()")
    # ページリンク
    bracket_page_re = re.compile(r"\[([^\]]+)\](?!\()")
    # Scrapboxのカードリンク
    double_bracket_link_re = re.compile(r"\[\[([^\s\]]+)(?:\s+[^\]]+)?\]\]")
    # Gyazo画像URL
    gyazo_link = re.compile(r"https?://(?:gyazo\.)[^\s\]]+")

    indent_unit = 4

    def indent_level(indent):
        width = 0
        for ch in indent:
            if ch == "\t":
                width += indent_unit
            elif ch == "\u3000":
                width += indent_unit
            else:
                width += 1
        if width <= 1:
            return 0
        return width // indent_unit

    def strip_url_options(url):
        last_slash = url.rfind("/")
        if last_slash == -1:
            return url
        colon_after_path = url.find(":", last_slash + 1)
        if colon_after_path == -1:
            return url
        return url[:colon_after_path]

    def linkify_tag_line(text):
        stripped = text.strip()
        if not stripped.startswith("#") or stripped.startswith("# "):
            return text
        parts = stripped.split()
        linked_parts = []
        for part in parts:
            if part.startswith("#") and len(part) > 1:
                linked_parts.append(f"[{part}]({part.replace('#', '')})")
            else:
                linked_parts.append(part)
        return " ".join(linked_parts)

    def format_inline(text):
        def replace_double_bracket(match):
            raw = match.group(1)
            if not raw.startswith(("http://", "https://")):
                return match.group(0)
            clean = strip_url_options(raw)
            return f"[{clean}]({clean})"

        def replace_text_link(match):
            label = match.group(1)
            raw = match.group(2)
            clean = strip_url_options(raw)
            return f"[{label}]({clean})"

        def replace_url_title(match):
            raw = match.group(1)
            label = match.group(2)
            clean = strip_url_options(raw)
            return f"[{label}]({clean})"

        def replace_bracket_url(match):
            raw = match.group(1)
            clean = strip_url_options(raw)
            return f"[{clean}]({clean})"

        text = double_bracket_link_re.sub(replace_double_bracket, text)
        text = text_hyperlink_re.sub(replace_text_link, text)
        text = url_title_re.sub(replace_url_title, text)
        text = bracket_url_re.sub(replace_bracket_url, text)
        text = strike_re.sub(r"~~\1~~", text)
        text = bold_re.sub(r"**\1**", text)
        def replace_page_link(match):
            label = match.group(1).strip()
            if not label:
                return ""
            if label.startswith(("http://", "https://", "*", "-")):
                return match.group(0)
            return f"[{label}]({label})"

        text = bracket_page_re.sub(replace_page_link, text)
        return text

    md_array = []
    is_this_text_code = False
    is_this_text_title = True

    prev_blank = True
    prev_list = False

    def add_line(value, is_list=False):
        nonlocal prev_blank, prev_list
        if is_list and not prev_blank and not prev_list:
            md_array.append("")
        md_array.append(value)
        prev_blank = (value == "")
        prev_list = is_list

    for text in text_array:
        line = text.rstrip("\n")
        if is_this_text_title:
            add_line("# " + line.strip())
            is_this_text_title = False
            continue

        if is_this_text_code:
            if line.strip() == "":
                add_line("")
                continue
            if line[:1] in (" ", "\t"):
                add_line(line[1:])
                continue
            add_line("```")
            is_this_text_code = False

        if line.strip() == "":
            add_line("")
            continue

        stripped = line.strip()
        if result_code := code_re.match(stripped):
            lang = result_code.group(1) or ""
            add_line("```" + lang)
            is_this_text_code = True
            continue

        if result_heading := heading_re.match(stripped):
            level = min(len(result_heading.group(1)), 6)
            add_line("#" * level + " " + result_heading.group(2))
            continue

        if result_indent := indent_re.match(line):
            indent, content = result_indent.group(1), result_indent.group(2)
            prefix = " " * indent_unit * indent_level(indent)
            if result := gyazo_link.fullmatch(content):
                item = f"![]({strip_url_options(result.group(0))})"
            elif result := url_re.fullmatch(content):
                url = strip_url_options(result.group(0))
                item = f"[{url}]({url})"
            else:
                item = format_inline(linkify_tag_line(content))
            if ordered_list_re.match(item) or unordered_list_re.match(item):
                add_line(prefix + item, is_list=True)
            else:
                add_line(prefix + "- " + item, is_list=True)
        else:
            tag_line = linkify_tag_line(stripped)
            if tag_line != stripped:
                add_line(tag_line)
                continue
            if result := gyazo_link.fullmatch(stripped):
                url = strip_url_options(result.group(0))
                add_line(f"![]({url})")
                continue
            if result := url_re.fullmatch(stripped):
                url = strip_url_options(result.group(0))
                add_line(f"[{url}]({url})")
                continue
            add_line(format_inline(line))

    if is_this_text_code:
        add_line("```")
    print("\n".join(md_array))


def main():
    sbfile = argv[1]
    scrapbox_to_md(sbfile)


if __name__ == "__main__":
    main()
