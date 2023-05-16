from djang import settings
import subprocess

bot_dir = settings.OPENLAW_BOT_DIR


def exec(filename, inp):
    out = subprocess.check_output(f"{bot_dir}/{filename}", input=inp.encode())
    return out.decode()


def syntax_law(data):
    return exec("SyntaxLaw.pm", data)


def syntax_wiki(data: bytes):
    return exec("SyntaxWiki.pm", data)


def syntax_html(data: bytes):
    return exec("SyntaxHTML.pm", data)


def post_processing(raw_result, formatting):
    html = raw_result
    if formatting == "basic":
        return html

    html = syntax_law(html)
    if formatting == "law":
        return html

    html = syntax_wiki(html)
    if formatting == "wiki":
        return html

    html = syntax_html(html)
    if formatting == "html":
        return html

    raise Exception(f"Unknown formatting {formatting}")
