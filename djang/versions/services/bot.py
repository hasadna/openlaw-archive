from djang import settings
import subprocess

bot_dir = settings.OPENLAW_BOT_DIR


def exec(filename, inp):
    path = f"{bot_dir}/{filename}"
    sub = subprocess.Popen(
        path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    out, err = sub.communicate(input=inp)
    exit_code = sub.wait()

    if exit_code:
        raise Exception(f"process {filename} exited with {exit_code}. stderr: {err}")

    return out


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
