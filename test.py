from runner import run_tex, score

code = 'Hello, World\\let\x0c\\eject!\x0c0\x0c1\x0c2\x0c3\x0c4\x0c5\x0c6\x0c7\x0c8\x0c9\\def~{\x0c\\argv\\fam\\advance\\fam1~ }~'

bytes_count, chars_count = score(code)
ok, out = run_tex(code, args=['foo', 'bar'])

print(f'Bytes: {bytes_count}, Chars: {chars_count}')
print(out)
