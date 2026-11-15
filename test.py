from runner import run_tex, score

code = r'''Hello, World\let\eject!0123456789\def~{\argv\fam\advance\fam1~ }~'''

bytes_count, chars_count = score(code)
ok, out = run_tex(code, args=['foo', 'bar'])

print(f'Bytes: {bytes_count}, Chars: {chars_count}')
print(out)
