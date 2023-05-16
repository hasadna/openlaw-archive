from djang import settings
import subprocess

bot_dir = settings.OPENLAW_BOT_DIR

# TODO not done


def exec(filename, inp):
    out = subprocess.check_output(f"{bot_dir}/{filename}", input=inp.encode())
    return out.decode()


def syntax_law(data):
    return exec("SyntaxLaw.pm", data)


def syntax_wiki(data: bytes):
    return exec("SyntaxWiki.pm", data)


def syntax_html(data: bytes):
    return exec("SyntaxHTML.pm", data)


# unfinished

# views/versions.py
# helpers/openlaw_bot.py


def post_processing(raw_result, formatting):
    if formatting == "basic":
        html = raw_result
        html = html.replace("\n", "<br />\n")
        return html
    elif formatting == "law":
        html = syntax_law(raw_result)
        html = html.replace("\n", "<br />\n")
        return html
    elif formatting == "wiki":
        html = syntax_law(raw_result)
        html = syntax_wiki(html)
        html = html.replace("\n", "<br />\n")
        return html
    elif formatting == "html":
        html = syntax_law(raw_result)
        html = syntax_wiki(raw_result)
        html = syntax_html(html)
        html = html_escape(html)
        html = html.replace("\n", "<br />\n")
        return html
    else:
        raise Exception(f"Unknown formatting {formatting}")
