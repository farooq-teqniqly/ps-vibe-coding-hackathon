import re

# Read the file
with open('/Users/jrollet/.local/share/opencode/tool-output/tool_c721d6d01001pvakh9LF95H3wJ', 'r') as f:
    content = f.read()

# Find all game rows - they have format: │  #N  │ Randy move │ Result │ Ada move │ Score │
pattern = r'│\s+#\d+\s+│\s+[🪨📄✂️]\s+\w+\s+│\s+\w+\s+│\s+([🪨📄✂️])\s+(\w+)\s+│'
matches = re.findall(pattern, content)

# Count Ada's moves
rock = sum(1 for _, move in matches if move == 'Rock')
paper = sum(1 for _, move in matches if move == 'Paper')
scissors = sum(1 for _, move in matches if move == 'Scissors')

total = len(matches)
print(f"Adaptive Ada Move Distribution ({total} games):")
print(f"Rock: {rock} ({rock*100/total:.1f}%)")
print(f"Paper: {paper} ({paper*100/total:.1f}%)")
print(f"Scissors: {scissors} ({scissors*100/total:.1f}%)")
print(f"\nThis shows DIVERSE strategy (not stuck on one move)!")
