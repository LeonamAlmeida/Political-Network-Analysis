import subprocess

def run_test(year, p_party, threshold_idx):
    cmd = f'python main.py'
    input_data = f'{year}\n{p_party}\n{threshold_idx}\n'
    
    result = subprocess.run(cmd, input=input_data, text=True, shell=True, capture_output=True)
    
    print(result.stdout)
    print(result.stderr)

# Caso for rodar todos os anos
# for i in range(2002, 2023):
#     test_cases = [
#     (i, '', '0.9'),
# ]
  
test_cases = [
    ('2023', 'PSOL PT', '0.9'),
    ('2023', 'PT PL', '0.9'),
    ('2023', 'PSD PT', '0.9'),
    ('2023', 'MDB PT', '0.9'),
    ('2023', '', '0.9'), 
]

if __name__ == '__main__':
    for year, p_party, threshold_idx in test_cases:
        print(f"Running test with year={year}, p_party={p_party}, threshold_idx={threshold_idx}")
        run_test(year, p_party, threshold_idx)
