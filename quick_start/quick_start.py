import os, argparse, sys

SCRIPTS = os.getcwd()
DV_ROOT = os.path.dirname(SCRIPTS)
DV_SCRIPTS = os.path.join(DV_ROOT, 'scripts')
sys.path.insert(0, DV_SCRIPTS)

from core_log_to_trace_csv import process_core_log
from spike_log_to_trace_csv import process_spike_sim_log
from instr_trace_compare import compare_trace_csv


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


def generate_disassembly(objfile_path, test, dump_path):
    os.system('riscv64-unknown-elf-objdump -d {0}_0.o > {1}'.format(
        os.path.join(objfile_path, 'asm_test', test),
        os.path.join(dump_path, 'test.s')
    ))
    return


def run_core(core_path):
    os.chdir(
        os.path.join(core_path, 'tools/trace')
    )
    os.system('./logGen.sh test.s')
    return


def logs_to_csv(core_log, core_csv, iss_log, iss_csv):
    os.chdir(SCRIPTS)
    process_core_log(core_log, core_csv, False)
    process_spike_sim_log(iss_log, iss_csv, False)
    return


def compare_csvs(
    core_csv,      iss_csv, core, iss, log,
    mismatch_limit
):
    compare_trace_csv(
        core_csv, iss_csv, core, iss,            log,
        1,        1,       1,    mismatch_limit, 0
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='ISA: rv32i, rv32im, rv32imc', type=str)
    parser.add_argument('--test', help='Name of DV test', type=str)
    parser.add_argument('--iterations', help='Iterations of the test', type=str, default=1)
    parser.add_argument('--out', help='Output directory', type=str)
    parser.add_argument('--core', help='Core directory path', type=str)
    args = parser.parse_args()

    run_dv(DV_ROOT, args.target, args.test, args.iterations, args.out)
    generate_disassembly(args.out, args.test, os.path.join(args.core, 'tools/trace/asm'))
    run_core(args.core)
    logs_to_csv(
        os.path.join(args.core, 'tools/trace/logs/nrv.log'),
        os.path.join(args.out, 'nrv.csv'),
        os.path.join(args.out, 'spike_sim/{0}.0.log'.format(args.test)),
        os.path.join(args.out, 'iss.csv')
    )
    compare_csvs(
        os.path.join(args.out, 'nrv.csv'),
        os.path.join(args.out, 'iss.csv'),
        'nucleusrv', 'iss',
        os.path.join(args.out, 'compare_result'),
        50
    )


if __name__ == '__main__':
    main()
