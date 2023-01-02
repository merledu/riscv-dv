def rem_csr_insts(csv_in, csv_out):
    with open(csv_in, 'r', encoding='UTF-8') as f:
        csv = f.readlines()

    with open(csv_out, 'w', encoding='UTF-8') as f:
        f.write(csv[0])
        for i in range(1, len(csv)):
            if 'csr' not in csv[i]:
                f.write(csv[i])
