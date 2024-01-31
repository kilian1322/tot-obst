import subprocess

command = '''python run.py --task obst --task_start_index {start_index} --task_end_index {end_index} --naive_run --prompt_sample cot --n_generate_sample 5'''

for i in range(20):
    print("cot starting tree " + str(i))
    subprocess.run(command.format(start_index=i, end_index=i+1), shell=True)
    print("cot ending tree " + str(i))
    print("\n***********************************************************\n")

