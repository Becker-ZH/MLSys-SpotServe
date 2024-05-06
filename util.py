# Adopted from SpotServe origin paper.
# This function is used to estimate an approximate latency based on parallelization strategy.
# tp: Tensor Parallel, pp: Model-pipeline Parallel, bsz: Batch Size
def get_approx_latency(self, tp, pp, pp_init_comm, bsz, M1, M2, layer_num, final_fix_factor, embed, init, incr, output_seq_len=100):
        factor = (layer_num + pp - 1) // pp

        t1 = init * factor * (pp + M1 - 1) / M1
        t1 += pp_init_comm / M1 * (pp - 1)
        t2 = incr * factor * (pp + M2 - 1)
        t2 += pp_init_comm / M2 * (pp - 1)

        lat = t1 + t2 * output_seq_len + 2 * embed[int(bsz).bit_length()-1]
        lat *= final_fix_factor
        return lat

# Adopted from SpotServe origin paper.
# This function is used to estimate the migration time, with approximately 20% error.
def estimate_last_switch_transfer_time(self):
        inter_node_bd = 50000 # Mbps
        intra_node_bd = 50000
        factor = 1
        max_inter_node = max(map(lambda x: x[0], self.ip2comm.values()))
        max_intra_node = max(map(lambda x: x[1], self.ip2comm.values()))
        t1 = max_inter_node / inter_node_bd
        t2 = max_intra_node / intra_node_bd
        return (t1 + t2) * factor