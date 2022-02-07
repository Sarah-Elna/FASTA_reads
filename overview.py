# Overview for all the palm species

def get_descriptions(file_name):
    description_list = []
    f = open(file_name, 'r')
    lines = f.readlines()
    for line in lines:
        if line[0] == '>':
            description_list.append(line)
    return description_list

def description_to_list(description):
    gene = ''
    species = ''
    description_a = description.split(' ')
    for i in range(0, len(description_a)):
        if 'Dypsis' in description_a[i]:
            species = 'D.' + description_a[i+1]
        if 'Marojejya' in description_a[i]:
            species = 'Mr.' + description_a[i+1]
        if 'Masoala' in description_a[i]:
            species = 'Ms.' + description_a[i+1]
        if 'Lemurophoenix' in description_a[i]:
            species = 'L.' + description_a[i+1]
        if '(' in description_a[i]:
            length = len(description_a[i])
            if length > 4 and length < 9:
                gene = description_a[i][1:(length - 1)]
    if gene != '' and species != '' and 'sp.' not in species:
        result = [gene, species]
        return result
    else:
        return None

def descriptions_to_complete_list(description_list):
    result_list = []
    for item in description_list:
        single_result = description_to_list(item)
        if single_result != None:
            result_list.append(single_result)
    return result_list

def get_sp_lst(result_list):
    sp_lst = []
    for result in result_list:
        if result[1] not in sp_lst:
            sp_lst.append(result[1])
    return sp_lst

def get_gen_lst(result_list):
    gen_lst = []
    for result in result_list:
        if result[0] not in gen_lst:
            gen_lst.append(result[0])
    return gen_lst

def get_empty_genbank_dict(sp_lst, gen_lst):
    empty_genbank_dict = {}
    for g in gen_lst:
        empty_genbank_dict[g] = 0
    return empty_genbank_dict

def fill_empty_dict(result_list):
    sp_lst = get_sp_lst(result_list)
    gen_lst = get_gen_lst(result_list)
    genbank_dict = get_empty_genbank_dict(sp_lst, gen_lst)
    for g in gen_lst:
        g_sp_lst = []
        g_count = 0
        for result in result_list:
            if g == result[0]:
                if result[1] not in g_sp_lst:
                    g_count += 1
                    g_sp_lst.append(result[1])
        genbank_dict[g] = '{} / {}'.format(g_count, len(sp_lst))
    return genbank_dict

def gen_sp_count(file_name):
    description = get_descriptions(file_name)
    description_list = descriptions_to_complete_list(description)
    genbank_dict = fill_empty_dict(description_list)
    return genbank_dict

def pretty_print(file_name):
    genbank_dict = gen_sp_count(file_name)
    genes = genbank_dict.keys()
    print( 'OUTPUT:', '\n', 30 * '-')
    print('gene : nr. sp. / total sp.')
    for g in genes:
        print('{} :'.format(g), genbank_dict[g])
    return 30 * '-'

def outgroup_match(ingroup_file, outgroup_file):
    o_dict_sp = {}
    o_dict_count = {}
    sp_list = []
    i_description = get_descriptions(ingroup_file)
    i_result_list = descriptions_to_complete_list(i_description)
    gene_list = get_gen_lst(i_result_list)
    o_descriptions = get_descriptions(outgroup_file)
    for g in gene_list:
        o_dict_sp[g] = []
        o_dict_count[g] = {}
        g_count = 0
        g_sp_lst = []
        gene = '({})'.format(g)
        for line in o_descriptions:
            new_line = line.split(' ')
            i = new_line.index('Areca')
            species = 'A. ' + new_line[i+1]
            if species != 'A. sp.' and species not in sp_list:
                sp_list.append(species)                    
            if gene in line and species not in g_sp_lst and species != 'A. sp.':
                g_sp_lst.append(species)
                g_count += 1
        o_dict_sp[g] = g_sp_lst
        o_dict_count[g] = '{} / {}'.format(g_count, len(sp_list))
    print( 'outgroup species list:', '\n', sp_list, '\n', 30*'-', '\n', 'gene: nr. sp / total sp.', '\n', o_dict_count)
    return (30 * '-')

## Test center
#my_i_file = 'all_palm_gb.fasta' # i for ingroup
#my_o_file = 'outgroup_palm.fasta' # o for outgroup
#print(pretty_print(my_i_file))
#description_list = get_descriptions(my_i_file)
#result_list = descriptions_to_complete_list(description_list)
#sp_list = get_sp_lst(result_list)
#gene_list = get_gen_lst(result_list)
#print('Ingroup species list:', '\n', sp_list, '\n', 30 * '-', '\n', 'Ingroup gene list:', '\n', gene_list, '\n', 30*'-', '\n')
#print(outgroup_match(my_i_file, my_o_file))
