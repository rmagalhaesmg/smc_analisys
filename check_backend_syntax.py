import py_compile
import os

# Find all Python files in backend
python_files = []
for root, dirs, files in os.walk('backend'):
    if 'venv' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            python_files.append(os.path.join(root, file))

errors = []
for f in python_files:
    try:
        py_compile.compile(f, doraise=True)
        print(f'OK: {f}')
    except Exception as e:
        errors.append((f, str(e)))
        print(f'ERROR: {f} - {e}')

print(f'\n=== Total: {len(python_files)} files, Errors: {len(errors)} ===')
for f, e in errors:
    print(f'{f}: {e}')
