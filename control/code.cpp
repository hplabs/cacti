
Ntwl/Ndwl - Number of horizontal partitions in a tag or data array i.e., the number of segments that a
single wordline is partitioned into.
• Ntbl/Ndbl - Number of vertical partitions in a tag or data array i.e., the number of segments that a single
bitline is partitioned into.
• Ntspd/Nspd - Number of sets stored in each row of a sub-array. For a given Ndwl and Ndbl values, Nspd
decides the aspect ratio of the sub-array.
• Ntcm/Ndcm - Degree of bitline multiplexing.
• Ntsam/Ndsam - Degree of sense-ampliﬁer multiplexing



DynamicParameter(
    bool is_tag_,
    int pure_ram_,
    int pure_cam_,
    double Nspd_,
    unsigned int Ndwl_,
    unsigned int Ndbl_,
    unsigned int Ndcm_,
    unsigned int Ndsam_lev_1_,
    unsigned int Ndsam_lev_2_,
    Wire_type wt,
    bool is_main_mem_):
  is_tag(is_tag_), pure_ram(pure_ram_), pure_cam(pure_cam_), tagbits(0), Nspd(Nspd_), Ndwl(Ndwl_), Ndbl(Ndbl_),Ndcm(Ndcm_),
  Ndsam_lev_1(Ndsam_lev_1_), Ndsam_lev_2(Ndsam_lev_2_),wtype(wt),
  number_way_select_signals_mat(0), V_b_sense(0), use_inp_params(0),
  is_main_mem(is_main_mem_), cell(), is_valid(false)
  
power.readOp.dynamic += mat.power.readOp.dynamic * dp.num_act_mats_hor_dir; 
    power.readOp.dynamic += r_predec->power.readOp.dynamic +
                          b_mux_predec->power.readOp.dynamic +
                          sa_mux_lev_1_predec->power.readOp.dynamic +
                          sa_mux_lev_2_predec->power.readOp.dynamic;
        r_predec            = new Predec(r_predec_blk_drv1, r_predec_blk_drv2);
        PredecBlkDrv * r_predec_blk_drv1 = new PredecBlkDrv(0, r_predec_blk1, is_dram);
        PredecBlkDrv * r_predec_blk_drv2 = new PredecBlkDrv(0, r_predec_blk2, is_dram);
        PredecBlk * r_predec_blk1 = new PredecBlk(
          num_dec_signals,  
          /*
          int    num_dec_signals  = subarray.num_rows; 

          num_rows(dp.num_r_subarray), num_cols(dp.num_c_subarray)
          
          num_cols +=(g_ip->add_ecc_b_ ? (int)ceil(num_cols / num_bits_per_ecc_b_) : 0); // -Add ECC cache parameter, num_bits_per_ecc_b_ =8.0
          num_r_subarray = (int)ceil(capacity_per_die / (g_ip->nbanks * g_ip->block_sz * g_ip->data_assoc * Ndbl * Nspd));
          num_c_subarray = (int)ceil((8 * g_ip->block_sz * g_ip->data_assoc * Nspd / Ndwl));// block_sz -block size (bytes);
          */
          row_dec,
         /*
         row_dec = new Decoder(
          num_dec_signals,
          false,
          subarray.C_wl,
                C_wl = (gate_C_pass(g_tp.sram.cell_a_w, (g_tp.sram.b_w-2*g_tp.sram.cell_a_w)/2.0, false, true)*2 +
				        c_w_metal) * num_cols;
                cell_a_w = -Wmemcella tech parameter 
                area_cell = -area cell tech parameter 
                asp_ratio_cell = -asp_ratio_cell tech parameter 
                area_cell *= (g_ip->F_sz_um* g_ip->F_sz_um); 
                    F_sz_um = technology size
                b_w = sqrt(area_cell / (asp_ratio_cell));
          R_wire_wl_drv_out, 
                subarray.num_cols * cell.w * g_tp.wire_local.R_per_um;
                      R_per_um = tech parameter 
                      cell.w = g_tp.sram.b_w + 2 * wire_local.pitch * (g_ip->num_rw_ports - 1 +
                      (g_ip->num_rd_ports - g_ip->num_se_rd_ports) +
                       g_ip->num_wr_ports) + g_tp.wire_local.pitch * g_ip->num_se_rd_ports;
                            wire_local.pitch = tech parameter 
                            num_rw_ports = cache input
                            num_wr_ports = cache 
                            num_se_rd_ports = cache
                            num_rd_ports = cache 
              
          false,
          is_dram,
          true,
          camFlag? cam_cell:cell);
          */
          C_wire_predec_blk_out,
            /*
            C_wire_predec_blk_out  = num_subarrays_per_row * subarray.num_rows * g_tp.wire_inside_mat.C_per_um * cell.h;
                C_per_um = tech param
                cell.h = g_tp.sram.b_h + 2 * wire_local.pitch * (g_ip->num_wr_ports +g_ip->num_rw_ports-1 + g_ip->num_rd_ports)
                + 2 * wire_local.pitch*(g_ip->num_search_ports-1);
                num_subarrays_per_row = dp.Ndwl/dp.num_mats_h_dir
            */
          R_wire_predec_blk_out,
            /*
            R_wire_predec_blk_out  = num_subarrays_per_row * subarray.num_rows * g_tp.wire_inside_mat.R_per_um * cell.h;
            */
          num_subarrays_per_mat,
            /*
            dp.num_subarrays/dp.num_mats
            */
          is_dram,
          true);
        PredecBlk * r_predec_blk2 = new PredecBlk(
          num_dec_signals,
          row_dec,
          C_wire_predec_blk_out,
          R_wire_predec_blk_out,
          num_subarrays_per_mat,
          is_dram,
          false);

    num_act_mats_hor_dir = num_do_b_subbank / num_do_b_mat;
        num_mats_h_dir = MAX(Ndwl / 2, 1);
        num_mats_v_dir = MAX(Ndbl / 2, 1);
        num_mats       = num_mats_h_dir * num_mats_v_dir;
        num_do_b_mat   = MAX((num_subarrays/num_mats) * num_c_subarray / (deg_bl_muxing * Ndsam_lev_1 * Ndsam_lev_2), 1);
        
        num_di_b_mat = num_do_b_mat;

        num_do_b_subbank = g_ip->int_prefetch_w * g_ip->out_w; // -internal prefetch width  * -output/input bus width 
        
        num_subarrays = Ndwl * Nd

        num_r_subarray = (int)ceil(capacity_per_die / (g_ip->nbanks * g_ip->block_sz * g_ip->data_assoc * Ndbl * Nspd));
        num_c_subarray = (int)ceil((8 * g_ip->block_sz * g_ip->data_assoc * Nspd / Ndwl));// block_sz -block size (bytes);
        
    //data_assoc = -associativity 
    

power.readOp.leakage += mat.power.readOp.leakage * dp.num_mats;
    num_mats       = num_mats_h_dir * num_mats_v_dir;

power.readOp.gate_leakage += mat.power.readOp.gate_leakage * dp.num_mats;

power.readOp.dynamic += htree_in_add->power.readOp.dynamic;
    new Htree2 (dp.wtype/*g_ip->wt*/,(double) mat.area.w, (double)mat.area.h,
      total_addrbits, datainbits, 0,dataoutbits,0, num_mats_ver_dir*2, num_mats_hor_dir*2, Add_htree);

    in_htree{}
        power.readOp.dynamic += wtemp1->power.readOp.dynamic;
        power.readOp.dynamic += wtemp2->power.readOp.dynamic
            wire stats 
            power.readOp.dynamic = global.power.readOp.dynamic * wire_length;
                wire_length = len_temp = (mat_width*ndwl/2 +
        ((add_bits + data_in_bits + data_out_bits + (search_data_in_bits + search_data_out_bits)) * g_tp.wire_outside_mat.pitch *
         2 * (1-pow(0.5,v))))/2; 
                          v = (int) _log2(ndbl/2);
                          add_bits = total_addrbits = (dp.number_addr_bits_mat + dp.number_subbanks_decode)*(RWP+ERP+EWP);
                                    number_addr_bits_mat = MAX((unsigned int) num_addr_b_row_dec,
			                              _log2(deg_bl_muxing) + _log2(deg_sa_mux_l1_non_assoc) + _log2(Ndsam_lev_2));
                                            num_addr_b_row_dec = _log2(mat.subarray.num_rows);
                                            


    datainbits   = dp.num_di_b_bank_per_port * (RWP + EWP);

power.readOp.dynamic += htree_out_data->power.readOp.dynamic; //final stage of calcualtion







UCA::UCA(const DynamicParameter & dyn_p)
 :dp(dyn_p), bank(dp), nbanks(g_ip->nbanks), refresh_power(0)

/*
num_di_b_bank_per_port = g_ip->out_w + g_ip->data_assoc; //-output/input bus width + 
num_do_b_bank_per_port = g_ip->out_w; // -output/input bus width
		  */
		  
num_di_b_bank   = dp.num_di_b_bank_per_port * (RWP + EWP);
  num_do_b_bank   = dp.num_do_b_bank_per_port * (RWP + ERP);
  num_si_b_bank   = dp.num_si_b_bank_per_port * SCHP;
  num_so_b_bank   = dp.num_so_b_bank_per_port * SCHP;
  
  int num_banks_ver_dir = 1 << ((bank.area.h > bank.area.w) ? _log2(nbanks)/2 : (_log2(nbanks) - _log2(nbanks)/2)); 
  //nbanks = -UCA bank count cache parameter
  int num_banks_hor_dir = nbanks/num_banks_ver_dir;
  
  num_addr_b_bank = (dp.number_addr_bits_mat + dp.number_subbanks_decode)*(RWP+ERP+EWP); 
  
    num_di_b_bank   = dp.num_di_b_bank_per_port * (RWP + EWP);
  num_do_b_bank   = dp.num_do_b_bank_per_port * (RWP + ERP);
  num_si_b_bank   = dp.num_si_b_bank_per_port * SCHP;
  num_so_b_bank   = dp.num_so_b_bank_per_port * SCHP;