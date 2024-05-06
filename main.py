# estimated migration time as constant
def estimate_migration_time(flag):
    if flag:
        return 1
    else:
        return 0

# estimated latency overhead due to reduced instances
def estimate_node_reduction_latency(n):
    return 1.0 / n

def get_action_space(prior, curr):
    action_space = []
    if curr == 'a':
        if prior == 'a':
            action_space = [('a', 'a'), ('-', 'aa')]
        elif prior == 'r':
            action_space = [('r', 'a')]
        else:
            return []
    elif curr == 'r':
        if prior == 'a':
            action_space = [('a', 'r'), ('ar', '-'), ('-', 'ar')]
        elif prior == 'r':
            action_space = [('r', 'r'), ('rr', '-')]
        else:
            return []          
    else:
        return []
    
    return action_space

def get_optimal_latency(action_space, curr_num, num_change):
    min_latency = float('inf')
    opt_action = None
    num_node = None
    pri_flag, curr_flag = 1, 1

    for x in action_space:
        if x[0] == '-':
            pri_flag = 0
        if x[1] == '-':
            curr_flag = 0
        
        if x[1] == 'a':
            curr_num += num_change
        if x[1] == 'r':
            curr_num -= num_change

        curr_latency = estimate_migration_time(pri_flag) +  estimate_migration_time(curr_flag) +  estimate_node_reduction_latency(curr_num)
        if curr_latency < min_latency:
            opt_action, num_node = x, curr_num
            min_latency = curr_latency
    
    return min_latency, opt_action, num_node

def opt_strategy_gp(trace):
    total_latency_gp = []
    action_gp = []
    for gp_i in trace:
        l_i, a_i = optimal_migration_trigger(gp_i)
        total_latency_gp.append(l_i)
        action_gp.append(a_i)
    total_latency = sum(total_latency_gp)
    return total_latency, action_gp

def optimal_migration_trigger(gp_i):
    l_i = [] 
    # list, l_i[j] = the most updated latency for events up to step j at iter j
    a_i = [] 
    # list, action of i: a_i[j] = the most updated optimal action seq for events up to step j at iter j
    # each element is a tuple (action_seq, number of nodes)
    curr_node = 0
    
    for i, e in enumerate(gp_i):
        if i == 0: 
            a_i.append((None, e[1]))
            continue
        if i == 1:
            # Get valid action space for e
            first_event = gp_i[0]
            action_space = get_action_space(first_event[0], e[0])
            if first_event[0] == 'a':
                curr_node += first_event[1]

            # Find optimal action for e at iter i: min(latency(e))
            latency, opt_action, num_node = get_optimal_latency(action_space, curr_node, e[1])
            # update l_i
            l_i.append(latency)
            # update a_i
            a_i.append((opt_action, num_node))
            curr_node = num_node
        else:
            # Retrieve a_i[i-1] from a_i 
            # Each a_i is calculated based on a_i[i-1]: pai_star = J(pai_minus_1_star)
            prior_action, prior_num_node = a_i[i - 1][0], a_i[i - 1][1]
            last_step_prior_action = prior_action[1] if prior_action[1] != '-' else prior_action[0]

            # Get valid action space for e based on a_i[i-1]
            action_space = get_action_space(last_step_prior_action[-1], e[0])

            # Find optimal action for e at iter i: min(latency(e))
            latency, opt_action, num_node = get_optimal_latency(action_space, prior_num_node, e[1])
            # update l_i 
            l_i.append(latency)
            # update a_i 
            a_i.append((opt_action, num_node))
    return l_i[-1], a_i

def main():
    opt_total_latency = float('inf')
    opt_action_gp = [] # len(opt_action_gp) = T, # of grace periods\

    trace = [[('a', 5), ('r', 2), ('a', 1)], [('a', 2), ('a', 3), ('r', 1), ('r', 1)]]

    opt_total_latency, opt_action_gp = opt_strategy_gp(trace)
    print(opt_total_latency, opt_action_gp)

if __name__ == '__main__':
    main()