import os
import re
import subprocess

DIR = os.path.dirname(os.path.abspath(__file__))
D2T = os.path.join(DIR, "dvi-to-text.exe" if os.name == "nt" else "dvi-to-text")
TRIMMER = re.compile(r"[\t\x0B\f\r ]+(?:\n|$)")


def run_tex(code, args=None, timeout=10):
    header = "\\font\\octet=octet\n\\octet\\footline={}\\parindent=0pt\\hsize=16000pt\\vsize=16000pt\\relax"

    if not args:
        arg_def = "\\def\\argc{0}\\global\\def\\argv#1{}"
    else:
        cat_setup = (
            "{\\catcode1=1\\catcode2=2\\catcode3=7\\catcode5=0\\catcode6=6\\catcode4=10\\catcode7=14"
            "\\catcode`$=12\\catcode`&=12\\catcode`^=12\\catcode`_=12\\catcode37=12"
            "\\catcode`~=12\\catcode`#=12\\catcode`{=12\\catcode`}=12\\catcode9=12\\catcode32=12"
            "\\catcode10=12\\catcode12=12\\catcode13=13\\catcode92=12"
        )
        c1, c2, c3, c4, c5, c6 = chr(1), chr(2), chr(3), chr(4), chr(5), chr(6)
        sanitized = [a.replace("\n", f"{c3}{c3}M") for a in args]
        first = sanitized[0]
        rest = "".join(f"{a}{c5}or{c4}" for a in sanitized[1:])
        body = f"{c5}global{c5}def{c5}argv{c6}1{c1}{c5}ifnum{c6}1=0{c4}{first}{c5}else{c5}ifcase{c6}1{c5}or{c4}{rest}{c5}fi{c5}fi{c2}{c2}"
        arg_def = f"\\def\\argc{{{len(args)}}}{cat_setup}{body}"

    full = f"{header}\n{arg_def}\n{code}\n\\bye\n"
    tex_file = os.path.join(DIR, "tmp.tex")
    dvi_file = os.path.join(DIR, "tmp.dvi")

    if os.path.exists(dvi_file):
        os.remove(dvi_file)

    with open(tex_file, "wb") as f:
        f.write(full.encode("utf-8"))

    res = subprocess.run(
        ["tex", "-interaction=nonstopmode", "tmp.tex"],
        cwd=DIR,
        capture_output=True,
        timeout=timeout,
    )
    if not os.path.exists(dvi_file):
        return False, "Compilation error:\n" + res.stdout.decode("latin1", errors="replace")[-400:]

    d2t = subprocess.run([D2T, dvi_file], cwd=DIR, capture_output=True)
    out = d2t.stdout.decode("utf-8", errors="replace")
    return True, TRIMMER.sub("\n", out).rstrip("\n")


def score(code):
    return len(code.encode("utf-8")), len(code)
