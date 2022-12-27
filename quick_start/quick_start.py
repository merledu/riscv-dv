import os, argparse


SCRIPTS = os.getcwd()
DV_ROOT = os.path.dirname(SCRIPTS)


def run_dv(path, target, test, iterations, output_path):
    os.chdir(DV_ROOT)
    os.system(
        'python3 run.py'
        ' --target {1}'
        ' -si pyflow'
        ' --iss spike'
        ' -v'
        ' --test {2}'
        ' --iterations {3}'
        ' --output {4}'.format(
            path, target, test, iterations, output_path
        )
    )
    return


#def run_core(core_path):
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='ISA: rv32i, rv32im, rv32imc', type=str)
    parser.add_argument('--test', help='Name of DV test', type=str)
    parser.add_argument('--iterations', help='Iterations of the test', type=str, default=1)
    parser.add_argument('--out', help='Output directory', type=str)
    args = parser.parse_args()

    run_dv(DV_ROOT, args.target, args.test, args.iterations, args.out)


if __name__ == '__main__':
    main()
