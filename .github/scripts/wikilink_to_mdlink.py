import os
import re

# .mdファイルを再帰的に走査
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.md'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            # [[filename]] → [filename](filename.md) に変換
            new_text = re.sub(r'\[\[([^\[\]|]+)\]\]', r'[\1](\1.md)', text)
            if new_text != text:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_text)
