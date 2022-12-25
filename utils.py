import difflib
def highlight_differences(a, b):
    diffs = difflib.ndiff(a, b)
    result = []
    for diff in diffs:
        if diff[0] == ' ':
            result.append(diff[-1])
        elif diff[0] == '-':
            result.append('<b>' + diff[-1] + '</b>')
    return ''.join(result)